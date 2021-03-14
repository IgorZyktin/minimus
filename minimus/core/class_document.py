# -*- coding: utf-8 -*-

"""Representation of a single document.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Document:
    """Representation of a single document.
    """
    header: str
    tags: List[str]
    content: str
    category: str
