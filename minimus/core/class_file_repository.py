# -*- coding: utf-8 -*-

"""Storage for files.
"""
import json
from typing import Dict, Iterable

from minimus.core.class_file_model import FileModel
from minimus.core.class_filesystem_interactor import FilesystemInteractor
from minimus.core.class_path_converter import PathConverter


class FileRepository:
    """Storage for files.
    """

    def __init__(self, converter: PathConverter,
                 interactor: FilesystemInteractor) -> None:
        """Initialize instance."""
        self.converter = converter
        self.interactor = interactor
        self._storage: Dict[str, FileModel] = {}
        self._meta: Dict[str, dict] = {}

    def __len__(self) -> int:
        """Return amount of files in repository.
        """
        return len(self._storage)

    def __iter__(self) -> Iterable[FileModel]:
        """Iterate on models in repository.
        """
        return iter(self._storage.values())

    def get_meta_path(self) -> str:
        """Return path to a metafile with previously saved files statistics."""
        return self.interactor.join(
            self.converter.source_directory, 'meta.json'
        )

    def get_existing_meta(self) -> dict:
        """Load statistic for previously saved files.
        """
        content = self.interactor.read_file(self.get_meta_path())

        if content:
            meta = json.loads(content)
        else:
            meta = {}

        return meta

    def load_files(self):
        """Load all user created files."""
        meta = self.get_existing_meta()
        self._meta.update(meta)

        folder = self.converter.source_directory
        generator = self.interactor.iterate_on_unique_filenames(folder)

        for directory, filename in generator:
            path = self.interactor.join(directory, filename)
            actual_stats = self.interactor.get_stats_for_file(path)

            new_instance = FileModel(
                directory=directory,
                filename=filename,
                content='',
                is_markdown=filename.lower().endswith('.md'),
                is_new=self._meta.get(filename) == actual_stats,
            )
            self._meta[filename] = actual_stats

            if new_instance.is_markdown:
                new_instance.content = self.interactor.read_file(path)

            self._storage[filename] = new_instance

    def update_files(self, stats, markdown):
        """Make output files from user created files."""
        for file in self:
            if file.is_markdown:
                document = markdown.parse(file.content)
                stats.add_document(file.filename, document)
                file.content = document.content

    def save_files(self):
        """Save output files."""
        meta_content = json.dumps(self._meta, indent=4, ensure_ascii=False)
        self.interactor.write_file(self.get_meta_path(), meta_content)

        # for file in self._storage.values():
        #     # if not file.is_new:
        #     #     continue
        #     path1 = self.interactor.join(file.directory, file.filename)
        #     print('path1 =', path1)
        #     path2 = self.interactor.find_shortest_common_path(
        #         self.converter.base_directory,
        #         path1,
        #     )
        #     print('path2 =', path2)
        # base_directory = self.interactor.find_shortest_common_path(
        #     self.converter.target_directory,
        #     self.converter.base_directory,
        # )
        #
        # target_directory = self.interactor.find_shortest_common_path(
        #     file.directory,
        #     base_directory,
        # )
        #
        # target_path = self.interactor.join(
        #     target_directory, file.filename
        # )
        #
        # print(file.directory, file.filename, '->>>', target_path)
        # if file.is_markdown:
        #     pass
        # else:
        #     pass
