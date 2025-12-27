"""Glob mode implementation"""

import os
import fnmatch
from typing import Tuple, Optional
from .base import BaseMode
from ..utils import get_all_files


class GlobMode(BaseMode):
    """Test patterns using Python glob (for comparison)"""
    
    def test_pattern(self, pattern: str) -> Tuple[list, Optional[str]]:
        """Test pattern with Python glob"""
        try:
            all_files = get_all_files(self.src_dir)
            matched = []
            
            for file_path in all_files:
                # Try different matching strategies
                if fnmatch.fnmatch(file_path, pattern):
                    matched.append(file_path)
                elif fnmatch.fnmatch(os.path.basename(file_path), pattern):
                    matched.append(file_path)
            
            return matched, None
            
        except Exception as e:
            return [], str(e)

