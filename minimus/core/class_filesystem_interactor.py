# -*- coding: utf-8 -*-

"""Special class that works with filesystem.
"""
import json
import os
from typing import Generator, Tuple, Dict


class FilesystemInteractor:
    """Special class that works with filesystem.
    """

    @staticmethod
    def iterate_on_unique_filenames(source_path: str) \
            -> Generator[Tuple[str, str], None, None]:
        """Walk through folder and get unique filenames."""
        known_filenames = set()

        for path, _, filenames in os.walk(source_path):
            for filename in filenames:
                if filename in known_filenames:
                    raise FileExistsError(
                        f'Filenames are supposed to be unique: {filename}'
                    )

                yield path, filename
                known_filenames.add(filename)

    @staticmethod
    def join(*args) -> str:
        """Join path for specific filesystem.
        """
        return os.path.join(*args)

    @classmethod
    def get_existing_stats(cls, directory: str, filename: str):
        full_path = cls.join(directory, filename)
        try:
            with open(full_path, mode='r', encoding='utf-8') as file:
                stats = json.load(file)
        except FileNotFoundError:
            stats = {}
        return stats

    @staticmethod
    def get_default_stats() -> Dict[str, int]:
        return {
            'created_at': -1,
            'modified_at': -1,
            'size': -1
        }

    @classmethod
    def get_stats_for_file(cls, directory: str,
                           filename: str) -> Dict[str, int]:
        full_path = cls.join(directory, filename)
        try:
            raw_stats = os.stat(full_path)
            stats = {
                'created_at': raw_stats.st_ctime_ns,
                'modified_at': raw_stats.st_mtime_ns,
                'size': raw_stats.st_size,
            }
        except FileNotFoundError:
            stats = cls.get_default_stats()
        return stats
