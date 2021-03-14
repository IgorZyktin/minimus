# -*- coding: utf-8 -*-

"""Representation of a single file on a disk.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class File:
    """Representation of a single file on a disk.
    """
    directory: str
    filename: str
    content: Optional[str]
    is_markdown: bool
    is_new: bool
