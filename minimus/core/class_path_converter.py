# -*- coding: utf-8 -*-

"""Special class that converts filesystem paths.
"""


class PathConverter:
    """Special class that converts filesystem paths.
    """

    def __init__(self, source_path: str, target_path: str) -> None:
        """Initialize instance."""
        self.source_path = source_path
        self.target_path = target_path
