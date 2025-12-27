"""Pattern test case definitions"""

from .wildcards import get_wildcard_tests
from .charset import get_charset_tests
from .path import get_path_tests
from .extglob import get_extglob_tests
from .regex import get_regex_tests

def get_all_tests():
    """Get all pattern test cases"""
    tests = []
    tests.extend(get_wildcard_tests())
    tests.extend(get_charset_tests())
    tests.extend(get_path_tests())
    tests.extend(get_extglob_tests())
    tests.extend(get_regex_tests())
    return tests

__all__ = ['get_all_tests', 'get_wildcard_tests', 'get_charset_tests', 
           'get_path_tests', 'get_extglob_tests', 'get_regex_tests']

