# -*- coding: utf-8 -*-

"""Representation of a single file on a disk.
"""
from typing import Dict


class FileProxy:
    """Representation of a single file on a disk."""

    def __init__(self, path: str, filename: str,
                 stats: Dict[str, int], is_changed: bool) -> None:
        """Initialize instance.
        """
        self.path = path
        self.filename = filename
        self.stats = stats
        self.is_changed = is_changed
