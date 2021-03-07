# -*- coding: utf-8 -*-

"""Single file statistics.
"""
from dataclasses import dataclass


@dataclass
class FileStats:
    """Single file statistics.
    """
    original_filename: str
    original_path: str
    created_at: int
    modified_at: int
    size: int
