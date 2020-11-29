# -*- coding: utf-8 -*-

"""Головной файл проекта.
"""
import sys

from minimus import arguments, settings
from minimus.components.class_repository import Repository
from minimus.utils.files_processing import make_metainfo, ensure_folder_exists
from minimus.utils.file_class_helpers import analyze_contents, \
    map_tags_to_files, ensure_each_tag_has_metafile
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

    # Syntax.stdout('\nStage 2. Hyperlinks generation')
    # ensure_each_tag_has_link(files)
    #
    # Syntax.stdout('\nStage 3. Indexes generation')
    # ensure_index_exists(config, files)
    #
    # Syntax.stdout('\nStage 4. Main files saving')
    # for number, file in Syntax.numerate(files):
    #     name = config.target_directory / file.filename
    #     if FileSystem.write(name, file.content):
    #         Syntax.stdout('\t{number}. Saved changes to the file {filename}',
    #                       number=number, filename=name.absolute())
    #
    # non_md = [
    #     x for x in config.source_directory.iterdir()
    #     if x.suffix.lower() != '.md' and not x.name.startswith('.')
    # ]
    # Syntax.stdout('\nStage 5. Additional files saving')
    # for number, file in Syntax.numerate(non_md):
    #     FileSystem.copy(
    #         file.absolute(),
    #         config.target_directory.absolute() / file.name,
    #     )
    #     Syntax.stdout('\t{number} File has been copied: {filename}',
    #                   number=number, filename=file.absolute())


def run(repository: Repository):
    """Основная работа.
    """
    tags_to_files = map_tags_to_files(repository.get_files())

    print(tags_to_files)

    stdout('\nStage 1. Metafile generation')
    ensure_each_tag_has_metafile(tags_to_files)


if __name__ == '__main__':
    main()  # pragma: no cover
