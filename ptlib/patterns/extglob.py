"""Extended glob pattern test cases"""

from ..models import TestCase


def get_extglob_tests():
    """Get extended glob pattern test cases"""
    return [
        TestCase(
            "extglob_optional",
            "file.txt?(~)",
            "Matches file.txt with optional ~ suffix",
            ["dir1/file.txt", "dir1/file.txt~"],
            "extglob"
        ),
        TestCase(
            "extglob_zero_or_more",
            "*(.txt)",
            "Matches files with zero or more .txt extensions",
            ["dir1/file.txt"],
            "extglob"
        ),
        TestCase(
            "extglob_one_or_more",
            "file.+(jpg|png)",
            "Matches file with one or more jpg or png extensions",
            ["dir1/file.jpg", "dir1/file.png"],
            "extglob"
        ),
        TestCase(
            "extglob_exactly_one",
            "@(cat|dog).png",
            "Matches exactly one of cat.png or dog.png",
            ["dir1/cat.png", "dir1/dog.png"],
            "extglob"
        ),
        TestCase(
            "extglob_not",
            "!(config.sys)",
            "Matches all files except config.sys",
            ["dir1/file1", "dir1/file1.txt"],
            "extglob"
        ),
        TestCase(
            "brace_operator",
            "file{a,b,c}",
            "Matches filea, fileb, or filec using brace expansion",
            [],
            "extglob"
        ),
    ]

