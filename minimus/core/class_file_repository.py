# -*- coding: utf-8 -*-

"""Storage for FileProxy.
"""

from minimus.core.class_file_proxy import FileProxy


class FileRepository:
    """Storage for FileProxy.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        self._storage = {}

    def __len__(self) -> int:
        """Return amount of files in snapshot.
        """
        return len(self._storage)

    def add_proxy(self, instance: FileProxy) -> None:
        self._storage[instance.filename] = instance

    def __iter__(self):
        return iter(self._storage.values())