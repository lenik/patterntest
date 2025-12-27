"""Tar mode implementation"""

import os
import subprocess
from typing import Tuple, Optional
from .base import BaseMode


class TarMode(BaseMode):
    """Test patterns using tar"""
    
    def test_pattern(self, pattern: str) -> Tuple[list, Optional[str]]:
        """Test pattern with tar"""
        try:
            tar_file = os.path.join(self.temp_dir, 'test.tar')
            
            if pattern.startswith('!'):
                # Exclude pattern - tar supports --exclude
                exclude_pattern = pattern[1:]
                cmd = [self.program_path, 'cf', tar_file, '-C', self.src_dir, '--exclude', exclude_pattern, '.']
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    error_msg = result.stderr.strip() if result.stderr else "Program exited with non-zero code"
                    if not error_msg:
                        error_msg = f"Program exited abnormally with code {result.returncode}"
                    return [], error_msg
            else:
                # Include pattern - tar doesn't have --include
                # Use find to match files, then tar them
                # This tests tar's ability to handle the pattern-matched files
                import fnmatch
                from ..utils import get_all_files
                
                all_files = get_all_files(self.src_dir)
                matched_files = []
                
                for f in all_files:
                    # Try full path match
                    if fnmatch.fnmatch(f, pattern):
                        matched_files.append(f)
                    # Try basename match
                    elif fnmatch.fnmatch(os.path.basename(f), pattern):
                        matched_files.append(f)
                    # Try pattern as substring in path
                    elif '/' in pattern and pattern in f:
                        matched_files.append(f)
                
                if not matched_files:
                    # No matches, create empty tar
                    cmd = [self.program_path, 'cf', tar_file, '-C', self.src_dir, '--files-from', '/dev/null']
                else:
                    # Create tar with matched files
                    cmd = [self.program_path, 'cf', tar_file, '-C', self.src_dir]
                    cmd.extend(matched_files)
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    error_msg = result.stderr.strip() if result.stderr else "Program exited with non-zero code"
                    if not error_msg:
                        error_msg = f"Program exited abnormally with code {result.returncode}"
                    return [], error_msg
            
            # List files in tar
            list_cmd = [self.program_path, 'tf', tar_file]
            list_result = subprocess.run(
                list_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if list_result.returncode != 0:
                error_msg = list_result.stderr.strip() if list_result.stderr else "Program exited with non-zero code"
                if not error_msg:
                    error_msg = f"Program exited abnormally with code {list_result.returncode}"
                return [], error_msg
            
            matched = [line.strip() for line in list_result.stdout.strip().split('\n') if line.strip()]
            return matched, None
            
        except subprocess.TimeoutExpired:
            return [], "Program execution timed out"
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else f"Program exited abnormally with code {e.returncode}"
            return [], error_msg
        except Exception as e:
            return [], f"Error: {str(e)}"

