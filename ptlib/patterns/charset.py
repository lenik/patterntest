"""Character set pattern test cases"""

from ..models import TestCase


def get_charset_tests():
    """Get character set pattern test cases"""
    return [
        TestCase(
            "match_char_range",
            "file[a-z]",
            "Matches files with lowercase letter after 'file'",
            ["dir1/file1", "dir1/file3", "dir1/some subdir/file2", "dir1/some subdir/file3", "dir2/file4", "dir2/subdir2/file5"],
            "charset"
        ),
        TestCase(
            "match_char_set",
            "[abc]_file",
            "Matches files starting with a, b, or c followed by '_file'",
            ["dir3/a_file", "dir3/b_file", "dir3/c_file"],
            "charset"
        ),
        TestCase(
            "match_char_not_in_set",
            "[^abc]_file",
            "Matches files not starting with a, b, or c followed by '_file'",
            ["dir3/z_file"],
            "charset"
        ),
        TestCase(
            "match_char_class_alnum",
            "[[:alnum:]]*",
            "Matches files starting with alphanumeric character",
            ["dir1/file1", "dir1/file1.txt", "dir1/file1.jpg", "dir1/file1.png", "dir1/file3", "dir1/config.sys", "dir1/file.txt", "dir1/file.txt~", "dir1/cat.png", "dir1/dog.png", "dir1/file.jpg", "dir1/file.png", "dir1/file.+(jpg|png)", "dir1/some subdir/file2", "dir1/some subdir/file2.txt", "dir1/some subdir/file3", "dir1/some subdir/file3.log", "dir1/some subdir/nested/deepfile", "dir1/some subdir/nested/deepfile.txt", "dir2/file4", "dir2/file4.txt", "dir2/subdir2/file5", "dir2/subdir2/file5.txt", "dir3/a_file", "dir3/b_file", "dir3/c_file", "dir3/z_file", "dir3/file_1", "dir3/file_2", "dir3/file_3", "dir3/test123", "dir3/test456", "dir3/test789", "rootfile", "file_root.txt"],
            "charset"
        ),
    ]

