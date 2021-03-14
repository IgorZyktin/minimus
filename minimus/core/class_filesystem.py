# -*- coding: utf-8 -*-

"""Special class that works with filesystem.
"""
import os
import shutil
from pathlib import Path
from typing import Generator, Tuple, Dict

from colorama import Fore

from minimus.utils.output_processing import stdout, translate as _


class Filesystem:
    """Special class that works with filesystem.
    """

    def __init__(self, source_directory: str, target_directory: str,
                 readme_directory: str) -> None:
        """Initialize instance."""
        self.source_directory = source_directory
        self.target_directory = target_directory
        self.readme_directory = readme_directory

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

    def at_source(self, *args: str) -> str:
        # FIXME
        return self.join(self.source_directory, *args)

    def at_target(self, *args: str) -> str:
        # FIXME
        return self.join(self.target_directory, *args)

    def at_readme(self, *args: str) -> str:
        # FIXME
        return self.join(self.readme_directory, *args)

    @classmethod
    def find_shortest_common_path(cls,
                                  current_directory: str,
                                  target_directory: str) -> str:
        """Build shortest common path from two paths.

        >>> current = r"C:\\usr\\va"
        >>> target = r"C:\\usr\\va\\bg\\doc\\pictures\\ew"
        >>> Filesystem.find_shortest_common_path(current, target)
        '.\\bg\\doc\\pictures\\ew'
        """
        if current_directory == target_directory:
            return '.'

        head_parts = list(Path(current_directory).parts)
        tail_parts = list(Path(target_directory).parts)

        common_elements = 0

        while head_parts and tail_parts:
            if head_parts[0] != tail_parts[0]:
                break

            head_parts.pop(0)
            tail_parts.pop(0)
            common_elements += 1

        if not common_elements:
            return target_directory

        resulting_path = ''

        if head_parts:
            for _ in head_parts:
                resulting_path = cls.join(resulting_path, '..')
        else:
            resulting_path = '.'

        for element in tail_parts:
            resulting_path = cls.join(resulting_path, element)

        return resulting_path
