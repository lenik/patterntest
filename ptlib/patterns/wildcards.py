"""Wildcard pattern test cases"""

from ..models import TestCase


def get_wildcard_tests():
    """Get wildcard pattern test cases"""
    return [
        TestCase(
            "match_any_star",
            "*",
            "Matches any file",
            ["dir1/file1", "dir1/file1.txt", "dir1/file1.jpg", "dir1/file1.png", "dir1/file3", "dir1/.hidden", "dir1/.hidden.txt", "dir1/config.sys", "dir1/file.txt", "dir1/file.txt~", "dir1/cat.png", "dir1/dog.png", "dir1/file.jpg", "dir1/file.png", "dir1/file.+(jpg|png)", "dir1/some subdir/file2", "dir1/some subdir/file2.txt", "dir1/some subdir/file3", "dir1/some subdir/file3.log", "dir1/some subdir/nested/deepfile", "dir1/some subdir/nested/deepfile.txt", "dir2/file4", "dir2/file4.txt", "dir2/.hidden2", "dir2/subdir2/file5", "dir2/subdir2/file5.txt", "dir3/a_file", "dir3/b_file", "dir3/c_file", "dir3/z_file", "dir3/file_1", "dir3/file_2", "dir3/file_3", "dir3/test123", "dir3/test456", "dir3/test789", "rootfile", ".hidden_root", "file_root.txt"],
            "wildcard"
        ),
        TestCase(
            "match_single_char",
            "file?",
            "Matches files with single character after 'file'",
            ["dir1/file1", "dir1/file3", "dir1/some subdir/file2", "dir1/some subdir/file3", "dir2/file4", "dir2/subdir2/file5"],
            "wildcard"
        ),
        TestCase(
            "match_txt_extension",
            "*.txt",
            "Matches files with .txt extension",
            ["dir1/file1.txt", "dir1/file.txt", "dir1/.hidden.txt", "dir1/some subdir/file2.txt", "dir1/some subdir/nested/deepfile.txt", "dir2/file4.txt", "dir2/subdir2/file5.txt", "file_root.txt"],
            "wildcard"
        ),
        TestCase(
            "match_hidden",
            ".*",
            "Matches hidden files",
            ["dir1/.hidden", "dir1/.hidden.txt", "dir2/.hidden2", ".hidden_root"],
            "wildcard"
        ),
    ]

