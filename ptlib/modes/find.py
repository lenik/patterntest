"""Find mode implementation"""

import os
import subprocess
from typing import Tuple, Optional
from .base import BaseMode


class FindMode(BaseMode):
    """Test patterns using find"""
    
    def test_pattern(self, pattern: str) -> Tuple[list, Optional[str]]:
        """Test pattern with find"""
        try:
            # Convert pattern to find -name/-path format
            cmd = [self.program_path, self.src_dir]
            
            if '/' in pattern:
                cmd.extend(['-path', pattern])
            else:
                cmd.extend(['-name', pattern])
            
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
            
            matched = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    rel_path = os.path.relpath(line.strip(), self.src_dir)
                    matched.append(rel_path)
            
            return matched, None
            
        except subprocess.TimeoutExpired:
            return [], "Program execution timed out"
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else f"Program exited abnormally with code {e.returncode}"
            return [], error_msg
        except Exception as e:
            return [], f"Error: {str(e)}"

