"""Path pattern test cases"""

from ..models import TestCase


def get_path_tests():
    """Get path pattern test cases"""
    return [
        TestCase(
            "match_subdir",
            "some subdir/*",
            "Matches all files in 'some subdir' directory",
            ["dir1/some subdir/file2", "dir1/some subdir/file2.txt", "dir1/some subdir/file3", "dir1/some subdir/file3.log", "dir1/some subdir/nested/deepfile", "dir1/some subdir/nested/deepfile.txt"],
            "path"
        ),
        TestCase(
            "match_globstar",
            "**/*.txt",
            "Matches .txt files in any directory recursively",
            ["dir1/file1.txt", "dir1/file.txt", "dir1/.hidden.txt", "dir1/some subdir/file2.txt", "dir1/some subdir/nested/deepfile.txt", "dir2/file4.txt", "dir2/subdir2/file5.txt", "file_root.txt"],
            "path"
        ),
        TestCase(
            "match_globstar_dir",
            "**/",
            "Matches all directories recursively",
            [],
            "path"
        ),
        TestCase(
            "match_globstar_start",
            "**/file.txt",
            "Matches file.txt in any directory recursively",
            ["dir1/file.txt"],
            "path"
        ),
        TestCase(
            "match_globstar_middle",
            "dir1/**/file3",
            "Matches file3 in dir1 or any subdirectory",
            ["dir1/file3", "dir1/some subdir/file3"],
            "path"
        ),
        TestCase(
            "match_begin",
            "^dir1",
            "Matches paths starting with dir1",
            ["dir1/file1"],
            "path"
        ),
        TestCase(
            "match_end",
            "*.txt$",
            "Matches paths ending with .txt",
            ["dir1/file1.txt"],
            "path"
        ),
        TestCase(
            "match_rootdir",
            "/*.txt",
            "Matches .txt files in root directory only",
            ["file_root.txt"],
            "path"
        ),
        TestCase(
            "match_is_dir",
            "*/",
            "Matches all directories",
            [],
            "path"
        ),
    ]

