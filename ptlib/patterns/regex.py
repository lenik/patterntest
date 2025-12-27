"""Regex pattern test cases"""

from ..models import TestCase


def get_regex_tests():
    """Get regex pattern test cases"""
    return [
        TestCase(
            "regex_dot",
            r"file\..*",
            "Matches file. followed by any characters",
            ["dir1/file1.txt", "dir1/file.txt"],
            "regex"
        ),
        TestCase(
            "regex_optional",
            r"file\.txt\?",
            "Matches file.txt with optional ? character",
            ["dir1/file.txt"],
            "regex"
        ),
        TestCase(
            "regex_zero_or_more",
            r"file.*",
            "Matches file followed by zero or more characters",
            ["dir1/file1", "dir1/file1.txt", "dir1/file1.jpg", "dir1/file1.png", "dir1/file3", "dir1/file.txt", "dir1/file.txt~", "dir1/file.jpg", "dir1/file.png", "dir1/file.+(jpg|png)", "dir1/some subdir/file2", "dir1/some subdir/file2.txt", "dir1/some subdir/file3", "dir1/some subdir/file3.log", "dir1/some subdir/nested/deepfile", "dir1/some subdir/nested/deepfile.txt", "dir2/file4", "dir2/file4.txt", "dir2/subdir2/file5", "dir2/subdir2/file5.txt", "dir3/file_1", "dir3/file_2", "dir3/file_3"],
            "regex"
        ),
        TestCase(
            "regex_one_or_more",
            r"file.+",
            "Matches file followed by one or more characters",
            ["dir1/file1", "dir1/file1.txt", "dir1/file1.jpg", "dir1/file1.png", "dir1/file3", "dir1/file.txt", "dir1/file.txt~", "dir1/file.jpg", "dir1/file.png", "dir1/file.+(jpg|png)", "dir1/some subdir/file2", "dir1/some subdir/file2.txt", "dir1/some subdir/file3", "dir1/some subdir/file3.log", "dir1/some subdir/nested/deepfile", "dir1/some subdir/nested/deepfile.txt", "dir2/file4", "dir2/file4.txt", "dir2/subdir2/file5", "dir2/subdir2/file5.txt", "dir3/file_1", "dir3/file_2", "dir3/file_3"],
            "regex"
        ),
        TestCase(
            "regex_group",
            r"file(_\d|\.txt)",
            "Matches file followed by _digit or .txt",
            ["dir1/file.txt", "dir3/file_1", "dir3/file_2", "dir3/file_3"],
            "regex"
        ),
        TestCase(
            "regex_digit",
            r"file_\d",
            "Matches file_ followed by a digit",
            ["dir3/file_1", "dir3/file_2", "dir3/file_3"],
            "regex"
        ),
        TestCase(
            "regex_word",
            r"\w+",
            "Matches one or more word characters",
            ["dir1/file1", "rootfile"],
            "regex"
        ),
        TestCase(
            "regex_word_boundary",
            r"\btest\d+\b",
            "Matches test followed by digits as whole word",
            ["dir3/test123", "dir3/test456", "dir3/test789"],
            "regex"
        ),
    ]

