# -*- coding: utf-8 -*-

"""Filesystem snapshot.

Gives information about filesystem state.
"""
import os
from typing import TypeVar, Generic, Generator, Tuple

from minimus.core.class_file_proxy import FileProxy
from minimus.utils.output_processing import stdout

T = TypeVar('T')


def iterate_on_unique_filenames(directory: str)\
        -> Generator[Tuple[str, str], None, None]:
    """Walk through folder and get unique names.
    """
    known_filenames = set()

    for path, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename in known_filenames:
                stdout(
                    'Filenames are supposed to be unique: {filename}',
                    filename=filename,
                )
                raise FileExistsError()

            yield path, filename
            known_filenames.add(filename)


class Snapshot(Generic[T]):
    """Filesystem snapshot.
    """

    def __init__(self, **proxies: FileProxy) -> None:
        """Initialize instance.
        """
        self._storage = dict(proxies)

    def __len__(self) -> int:
        """Return amount of files in snapshot.
        """
        return len(self._storage)

    @classmethod
    def from_directory(cls, directory: str) -> T:
        """Make snapshot of specific directory.
        """
        instance = cls()

        if not os.path.exists(directory):
            return instance

        for path, filenames in iterate_on_unique_filenames(directory):

                full_path = os.path.join(path, filename)
                stat = os.stat(full_path)
                meta = Meta(
                    original_filename=filename,
                    original_path=directory,
                    statistic=Statistic(
                        created_at=stat.st_ctime_ns,
                        modified_at=stat.st_mtime_ns,
                        size=stat.st_size,
                    ),
                )
                metainfo[meta.original_filename] = meta
                known_filenames.add(filename)

        return instance
