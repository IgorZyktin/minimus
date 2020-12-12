# -*- coding: utf-8 -*-

"""Головной файл проекта.
"""
import sys

# from minimus.components.class_repository import Repository
# from minimus.utils.file_class_helpers import *
# from minimus.utils.filesystem import ensure_folder_exists
# from minimus.utils.output_processing import stdout
from functools import partial

from minimus import output
from minimus.config import Config
from minimus.utils import arguments, files_processing
from minimus.utils.output_processing import stdout


def main():
    """Точка входа.
    """
    config = Config()
    _stdout = partial(stdout, language=config.LANGUAGE)

    # обработка и сохранение аргументов запуска
    given_arguments = arguments.parse_command_line_arguments(sys.argv)
    arguments.apply_cli_args_to_config(config, given_arguments)
    output.describe_resulting_config(config, _stdout)

    # получение общих сведений о состоянии файловой системы
    summary = files_processing.get_summary(
        source_directory=config.SOURCE_DIRECTORY,
        language=config.LANGUAGE,
    )
    metainfo = files_processing.get_metainfo(
        source_directory=config.SOURCE_DIRECTORY,
        metafile_name=config.METAFILE_NAME,
    )

    if not summary:
        stdout('No source files found to work with', language=config.LANGUAGE)
        return

    print(1, summary)
    print(2, metainfo)
    # repository = Repository(metainfo)

    # ensure_folder_exists(config.TARGET_DIRECTORY, config.LANGUAGE)
    # ensure_folder_exists(config.README_DIRECTORY, config.LANGUAGE)

    # analyze_contents(repository.get_files())


#     run(repository)


# def run(config: Config, repository: Repository):
#     """Основная работа.
#     """
#     tags_to_files = map_tags_to_files(repository.get_files())
#
#     stdout('\nStage 1. Metafile generation')
#     ensure_each_tag_has_metafile(tags_to_files)
#
#     stdout('\nStage 2. Indexes generation')
#     ensure_index_exists(repository.get_files())
#     ensure_readme_exists(repository.get_files())
#
#     stdout('\nStage 3. Main files saving')
#     save_md_files_to_the_target(repository.get_files())
#
#     stdout('\nStage 4. Additional files saving')
#     save_non_md_files_to_the_target()


if __name__ == '__main__':
    main()  # pragma: no cover
