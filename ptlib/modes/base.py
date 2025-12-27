"""Base class for test mode implementations"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional


class BaseMode(ABC):
    """Abstract base class for pattern testing modes"""
    
    def __init__(self, program_path: str, src_dir: str, temp_dir: str):
        self.program_path = program_path
        self.src_dir = src_dir
        self.temp_dir = temp_dir
    
    @abstractmethod
    def test_pattern(self, pattern: str) -> Tuple[list, Optional[str]]:
        """
        Test a pattern and return matched files
        
        Args:
            pattern: Pattern to test
            
        Returns:
            Tuple of (matched_files, error_message)
        """
        pass

