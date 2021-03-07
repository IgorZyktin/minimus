# -*- coding: utf-8 -*-

"""Representation of a single file on a disk.
"""
from minimus.core.class_file_stats import FileStats


class FileProxy:
    """Representation of a single file on a disk.
    """

    def __init__(self, path: str, filename: str,
                 actual_stats: FileStats, historical_stats: FileStats) -> None:
        """Initialize instance.
        """
        self.path = path
        self.filename = filename
        self.actual_stats = actual_stats
        self.historical_stats = historical_stats
