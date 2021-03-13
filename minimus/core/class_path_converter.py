# -*- coding: utf-8 -*-

"""Special class that converts filesystem paths.
"""
from pathlib import Path

from minimus.core.class_filesystem_interactor import FilesystemInteractor


class PathConverter:
    """Special class that converts filesystem paths.
    """

    def __init__(self,
                 interactor: FilesystemInteractor,
                 base_directory: str,
                 source_directory: str,
                 target_directory: str,
                 readme_directory: str) -> None:
        """Initialize instance."""
        self.interactor = interactor
        self.base_directory = base_directory
        self.source_directory = source_directory
        self.target_directory = target_directory
        self.readme_directory = readme_directory

    def find_shortest_common_path(self,
                                  current_directory: str,
                                  target_directory: str) -> str:
        """Build shortest common path from two paths.

        >>> current = r"C:\\usr\\va"
        >>> target = r"C:\\usr\\va\\bg\\doc\\pictures\\ew"
        >>> PathConverter.find_shortest_common_path(current, target)
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
                resulting_path = self.interactor.join(resulting_path, '..')
        else:
            resulting_path = '.'

        for element in tail_parts:
            resulting_path = self.interactor.join(resulting_path, element)

        return resulting_path
