"""Data models for pattern testing"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class TestMode(Enum):
    """Test mode enumeration"""
    TAR = "tar"
    RSYNC = "rsync"
    FIND = "find"
    GLOB = "glob"


@dataclass
class TestCase:
    """Represents a single pattern test case"""
    name: str
    pattern: str
    description: str
    expected_files: List[str]  # Relative paths that should match
    pattern_type: str  # "wildcard", "regex", "extglob", etc.


@dataclass
class TestResult:
    """Result of a pattern test"""
    test_case: TestCase
    matched_files: List[str]
    success: bool
    partial: bool = False  # True if some files matched but not all expected
    error: Optional[str] = None

