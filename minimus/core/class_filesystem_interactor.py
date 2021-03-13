# -*- coding: utf-8 -*-

"""Special class that works with filesystem.
"""
import os
import shutil
from pathlib import Path
from typing import Generator, Tuple, Dict

from colorama import Fore

from minimus.utils.output_processing import stdout, translate as _


class FilesystemInteractor:
    """Special class that works with filesystem.
    """

    @classmethod
    def get_stats_for_file(cls, path: str) -> Dict[str, int]:
        """Load actual meta information about file from disk."""
        try:
            raw_stats = os.stat(path)
            stats = {
                'created_at': raw_stats.st_ctime_ns,
                'modified_at': raw_stats.st_mtime_ns,
                'size': raw_stats.st_size,
            }
        except FileNotFoundError:
            stats = cls.get_default_stats()
        return stats

    @staticmethod
    def get_default_stats() -> Dict[str, int]:
        """Get default metarecord statistics for non existent file."""
        return {
            'created_at': -1,
            'modified_at': -1,
            'size': -1
        }

    @staticmethod
    def read_file(path: str) -> str:
        """Read textual file from disk."""
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = ''

        return content

    @staticmethod
    def write_file(path: str, content: str) -> None:
        """Write textual file to disk."""
        with open(path, mode='w', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def join(*args) -> str:
        """Join path for specific filesystem.
        """
        return os.path.join(*args)

    @classmethod
    def ensure_folder_exists(cls, path: str) -> bool:
        """Create all chain of folders at given path.

        Return True if creation is successful.
        Do not give path to files to this method!
        """
        path = Path(path)
        parts = list(path.parts)
        current_path = None
        actually_created = False

        for part in parts:
            if current_path is None:
                current_path = part
            else:
                current_path = cls.join(current_path, part)

            if not os.path.exists(current_path):
                os.mkdir(current_path)
                stdout(' New folder created: {folder}',
                       folder=current_path, color=Fore.MAGENTA)
                actually_created = True

        return actually_created

    @staticmethod
    def iterate_on_unique_filenames(source_path: str) \
            -> Generator[Tuple[str, str], None, None]:
        """Walk through folder and get unique filenames."""
        known_filenames = set()

        for directory, directories, filenames in os.walk(source_path):
            if directories:
                message = _('Current version of Minimus does '
                            'not support nested folders: {directories}')
                raise FileExistsError(message.format(directories=directories))

            for filename in filenames:
                if filename in known_filenames:
                    message = _('Filenames are supposed '
                                'to be unique: {filename}')
                    raise FileExistsError(message.format(filenams=filename))

                yield directory, filename
                known_filenames.add(filename)

    @staticmethod
    def copy_file(source: str, target: str) -> None:
        """Copy file from source to target."""
        shutil.copy(source, target)
