"""Rsync mode implementation"""

import os
import subprocess
import shutil
from typing import Tuple, Optional
from .base import BaseMode
from ..utils import get_all_files


class RsyncMode(BaseMode):
    """Test patterns using rsync"""
    
    def test_pattern(self, pattern: str) -> Tuple[list, Optional[str]]:
        """Test pattern with rsync"""
        try:
            # Create a fresh dest directory for this test
            dest_dir = os.path.join(self.temp_dir, 'dest')
            # Clean up previous dest directory if it exists
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            os.makedirs(dest_dir, exist_ok=True)
            
            # Build rsync command - actually copy files (no --dry-run)
            cmd = [self.program_path, '-av', '--quiet']
            
            if pattern.startswith('!'):
                cmd.extend(['--exclude', pattern[1:]])
            else:
                # For include patterns, rsync needs special handling
                # If pattern doesn't contain /, it's a basename pattern - need to match recursively
                if '/' not in pattern and '*' in pattern:
                    # Basename pattern like *.txt - need to include directories and then the pattern
                    cmd.extend(['--include', '*/'])  # Include all directories
                    cmd.extend(['--include', pattern])  # Include matching files
                    cmd.extend(['--exclude', '*'])  # Exclude everything else
                elif '**' in pattern:
                    # Globstar pattern - rsync 3.x supports **
                    cmd.extend(['--include', pattern])
                    cmd.extend(['--exclude', '*'])
                else:
                    # Path pattern
                    cmd.extend(['--include', pattern])
                    cmd.extend(['--exclude', '*'])  # Exclude everything else
            
            cmd.extend([self.src_dir + '/', dest_dir + '/'])
            
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
            
            # Get all files from dest directory and make them relative to src_dir
            # This gives us the files that rsync actually copied
            dest_files = get_all_files(dest_dir)
            
            # Convert dest paths to relative paths matching src_dir structure
            matched = []
            for dest_file in dest_files:
                # The dest_file is relative to dest_dir
                # We want it relative to src_dir for comparison
                matched.append(dest_file)
            
            return matched, None
            
        except subprocess.TimeoutExpired:
            return [], "Program execution timed out"
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else f"Program exited abnormally with code {e.returncode}"
            return [], error_msg
        except Exception as e:
            return [], f"Error: {str(e)}"

