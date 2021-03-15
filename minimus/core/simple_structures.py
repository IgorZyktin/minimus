# -*- coding: utf-8 -*-

"""Set of simple dataclasses.

Created to simplify interaction between components.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Document:
    """Representation of a single document.

    Not tied to any actual file.
    """
    header: str
    tags: List[str]
    content: str
    category: str


@dataclass
class File:
    """Representation of a single file on a disk.
    """
    directory: str
    filename: str
    content: Optional[str]
    is_markdown: bool
    is_new: bool
