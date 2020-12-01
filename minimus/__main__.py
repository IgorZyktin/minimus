# -*- coding: utf-8 -*-

"""Головной файл проекта.
"""
import sys

from minimus import arguments, settings
from minimus.components.class_repository import Repository
from minimus.utils.file_class_helpers import *
from minimus.utils.files_processing import make_metainfo, ensure_folder_exists
from minimus.utils.output_processing import stdout


def main():
    """Точка входа.
    """
    given_arguments = arguments.parse_command_line_arguments(sys.argv)
    arguments.apply_to_settings(given_arguments)
    arguments.describe_resulting_settings()
    ensure_folder_exists(settings.TARGET_DIRECTORY)

    metainfo = make_metainfo(settings.SOURCE_DIRECTORY)
    repository = Repository(metainfo)

    if not repository:
        stdout('No source files found to work with')
        sys.exit(1)

    analyze_contents(repository.get_files())

    run(repository)


def run(repository: Repository):
    """Основная работа.
    """
    tags_to_files = map_tags_to_files(repository.get_files())

    stdout('\nStage 1. Metafile generation')
    ensure_each_tag_has_metafile(tags_to_files)

    stdout('\nStage 2. Indexes generation')
    ensure_index_exists(repository.get_files())
    ensure_readme_exists(repository.get_files())

    stdout('\nStage 3. Main files saving')
    save_md_files_to_the_target(repository.get_files())

    stdout('\nStage 4. Additional files saving')
    save_non_md_files_to_the_target()


if __name__ == '__main__':
    main()  # pragma: no cover
