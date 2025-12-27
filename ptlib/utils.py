"""Utility functions for pattern testing"""

import os
import tempfile
from typing import List


def create_test_directory(example_dir_file: str, temp_dir: str) -> str:
    """Create test directory structure from example.dir file"""
    src_dir = os.path.join(temp_dir, 'src')
    os.makedirs(src_dir, exist_ok=True)
    
    # Parse example.dir and create structure
    with open(example_dir_file, 'r') as f:
        lines = f.readlines()
    
    stack = [(-1, src_dir)]  # (indent_level, current_path) - start with -1 for root
    
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
        
        # Calculate indent level
        indent = len(line) - len(line.lstrip())
        item = line.strip()
        
        if not item:
            continue
        
        # Pop stack until we find matching indent level
        while stack and stack[-1][0] >= indent:
            stack.pop()
        
        if not stack:
            # If stack is empty, reset to root
            stack = [(-1, src_dir)]
        
        _, parent_path = stack[-1]
        full_path = os.path.join(parent_path, item)
        
        if item.endswith('/'):
            # Directory
            os.makedirs(full_path, exist_ok=True)
            stack.append((indent, full_path))
        else:
            # File - create with 0 size (empty file)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            # Create empty file (0-sized)
            with open(full_path, 'w'):
                pass  # Create file with no content
    
    return src_dir


def get_all_files(base_dir: str) -> List[str]:
    """Get all files relative to base_dir"""
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, base_dir)
            files.append(rel_path)
    return sorted(files)

