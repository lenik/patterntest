"""Main pattern tester class"""

import os
import tempfile
from typing import List, Optional
from .models import TestMode, TestCase, TestResult
from .utils import create_test_directory, get_all_files
from .modes import TarMode, RsyncMode, FindMode, GlobMode
from logger import log_info, log_mesg, log_mesg_ecr, log_error, log_log, log_debug, log_warn


class PatternTester:
    """Main class for testing patterns with various tools"""
    
    def __init__(self, program_path: str, mode: Optional[TestMode] = None):
        self.program_path = program_path
        self.program_name = os.path.basename(program_path)
        
        # Auto-detect mode if not specified
        if mode is None:
            mode = self._detect_mode()
        self.mode = mode
        
        # Temporary directories
        self.temp_dir = None
        self.src_dir = None
        self.dest_dir = None
        
        # Mode implementation
        self.mode_impl = None
        
        # Test results
        self.results: List[TestResult] = []
        
    def _detect_mode(self) -> TestMode:
        """Detect test mode from program name"""
        name = self.program_name.lower()
        if 'tar' in name:
            return TestMode.TAR
        elif 'rsync' in name:
            return TestMode.RSYNC
        elif 'find' in name:
            return TestMode.FIND
        else:
            return TestMode.GLOB
    
    def _create_mode_impl(self):
        """Create the appropriate mode implementation"""
        if self.mode == TestMode.TAR:
            return TarMode(self.program_path, self.src_dir, self.temp_dir)
        elif self.mode == TestMode.RSYNC:
            return RsyncMode(self.program_path, self.src_dir, self.temp_dir)
        elif self.mode == TestMode.FIND:
            return FindMode(self.program_path, self.src_dir, self.temp_dir)
        else:
            return GlobMode(self.program_path, self.src_dir, self.temp_dir)
    
    def create_test_directory(self, example_dir_file: str) -> str:
        """Create test directory structure from example.dir file"""
        self.temp_dir = tempfile.mkdtemp(prefix='patterntest_')
        self.src_dir = create_test_directory(example_dir_file, self.temp_dir)
        self.mode_impl = self._create_mode_impl()
        return self.src_dir
    
    def get_all_files(self, base_dir: str) -> List[str]:
        """Get all files relative to base_dir"""
        return get_all_files(base_dir)
    
    def test_pattern(self, pattern: str):
        """Test pattern with the configured tool"""
        if self.mode_impl is None:
            raise RuntimeError("Test directory not created yet. Call create_test_directory first.")
        return self.mode_impl.test_pattern(pattern)
    
    def run_tests(self, example_dir_file: str, test_cases: List[TestCase]):
        """Run all tests"""
        log_mesg(f"Creating test directory from {example_dir_file}...")
        self.create_test_directory(example_dir_file)
        
        log_mesg(f"Testing with {self.program_name} (mode: {self.mode.value})...")
        log_debug(f"Source directory: {self.src_dir}")
        
        all_files = self.get_all_files(self.src_dir)
        log_debug(f"Total files in test directory: {len(all_files)}")
        log_mesg("")
        
        for i, test_case in enumerate(test_cases, 1):
            log_mesg_ecr(f"[{i}/{len(test_cases)}] Testing: {test_case.name}")
            log_info(f"  Pattern: {test_case.pattern}")
            log_info(f"  Description: {test_case.description}")
            
            matched, error = self.test_pattern(test_case.pattern)
            
            # Determine success: no error AND matched files match expected files
            if error is not None:
                success = False
                partial = False
            else:
                # Normalize paths for comparison (sort and convert to sets)
                matched_set = set(sorted(matched))
                expected_set = set(sorted(test_case.expected_files))
                # Success if matched files exactly match expected files
                success = matched_set == expected_set
                # Partial success if some files matched but not all expected
                # Partial means: has matches, is subset of expected, but not complete
                partial = (not success and 
                          len(matched_set) > 0 and 
                          len(expected_set) > 0 and
                          matched_set.issubset(expected_set) and 
                          len(matched_set) < len(expected_set))
            
            result = TestResult(
                test_case=test_case,
                matched_files=matched,
                success=success,
                partial=partial,
                error=error
            )
            
            self.results.append(result)
            
            if error:
                log_error(f"  ERROR: {error}")
            else:
                log_log(f"  Matched {len(matched)} files")
                if len(matched) <= 10:
                    for f in matched:
                        log_log(f"    - {f}")
                else:
                    for f in matched[:5]:
                        log_log(f"    - {f}")
                    log_log(f"    ... and {len(matched) - 5} more")
                
                # Log unmatched files (expected but not matched)
                matched_set = set(sorted(matched))
                expected_set = set(sorted(test_case.expected_files))
                unmatched = expected_set - matched_set
                if unmatched:
                    log_warn(f"  Unmatched (expected but not found): {len(unmatched)} files")
                    if len(unmatched) <= 10:
                        for f in sorted(unmatched):
                            log_warn(f"    - {f}")
                    else:
                        for f in sorted(list(unmatched))[:5]:
                            log_warn(f"    - {f}")
                        log_warn(f"    ... and {len(unmatched) - 5} more")
            log_info("")
    
    def cleanup(self):
        """Clean up temporary directories"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            log_debug(f"Cleaned up temporary directory: {self.temp_dir}")

