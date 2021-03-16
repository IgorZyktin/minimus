# -*- coding: utf-8 -*-

"""Storage for files.
"""
import json
from typing import Dict, Iterator

from colorama import Fore

from minimus.core.class_abstract_renderer import AbstractRenderer
from minimus.core.class_filesystem import Filesystem
from minimus.core.class_statistics import Statistics
from minimus.core.simple_structures import File
from minimus.utils.utils_locale import stdout
from minimus.utils.utils_text import numerate


class FileRepository:
    """Storage for files.
    """
    metafile_name = 'meta.json'

    def __init__(self, filesystem: Filesystem) -> None:
        """Initialize instance."""
        self._filesystem = filesystem
        self._storage: Dict[str, File] = {}
        self._meta: Dict[str, dict] = {}

    def __len__(self) -> int:
        """Return amount of files in repository.
        """
        return len(self._storage)

    def __iter__(self) -> Iterator[File]:
        """Iterate on models in repository.
        """
        return iter(self._storage.values())

    def get_meta_path(self) -> str:
        """Return path to a metafile with previously saved files statistics."""
        return self._filesystem.at_source(self.metafile_name)

    def get_existing_meta(self) -> dict:
        """Load statistic for previously saved files.
        """
        content = self._filesystem.read_file(self.get_meta_path())
        return json.loads(content) if content else {}

    def load_files(self):
        """Load all user created files."""
        existing_meta = self.get_existing_meta()
        self._meta.update(existing_meta)

        folder = self._filesystem.source_directory
        generator = self._filesystem.iterate_on_unique_filenames(folder)

        for directory, filename in generator:
            filename = filename.lower()
            self._process_single_file(directory, filename.lower())

    def _process_single_file(self, directory: str, filename: str) -> None:
        """Process single file during file loading stage.
        """
        if filename == self.metafile_name:
            return

        path = self._filesystem.join(directory, filename)
        actual_stats = self._filesystem.get_stats_for_file(path)
        is_markdown = filename.endswith('.md')
        is_new = self._meta.get(filename) == actual_stats

        new_instance = File(directory=directory,
                            filename=filename,
                            content='',
                            is_markdown=is_markdown,
                            is_new=is_new)
        self._meta[filename] = actual_stats

        if new_instance.is_markdown:
            new_instance.content = self._filesystem.read_file(path)

        self._storage[filename] = new_instance

    def update_files(self, statistics: Statistics,
                     renderer: AbstractRenderer) -> None:
        """Make output files from user created files."""
        for file in self:
            if file.is_markdown and file.content is not None:
                document = renderer.extract_features(file.content)
                statistics.add_document(file.filename, document)
                file.content = document.content

    def save_files(self) -> None:
        """Save output files."""
        meta_content = json.dumps(self._meta, indent=4, ensure_ascii=False)
        self._filesystem.write_file(self.get_meta_path(), meta_content)

        for number, file_model in numerate(self):
            if not file_model.is_new:
                stdout('\t{number}. No changes detected: {filename}',
                       number=number, filename=file_model.filename)
                continue

            target_path = self._filesystem.at_target(file_model.filename)

            if file_model.is_markdown and file_model.content is not None:
                self._filesystem.write_file(target_path, file_model.content)
                stdout('\t{number}. Saved changes: {filename}',
                       number=number, filename=file_model.filename,
                       color=Fore.YELLOW)
            else:
                source_path = self._filesystem.join(file_model.directory,
                                                    file_model.filename)
                self._filesystem.copy_file(source_path, target_path)
                stdout('\t{number}. Copied file: {filename}',
                       number=number, filename=file_model.filename,
                       color=Fore.MAGENTA)
