# -*- coding: utf-8 -*-

"""Головной файл проекта.
"""
import sys
from functools import partial

from colorama import init, Fore

from minimus import output
from minimus.components.class_repository import Repository
from minimus.config import Config
from minimus.utils import arguments, files_processing
from minimus.utils.file_class_helpers import save_main_files, \
    save_additional_files
from minimus.utils.filesystem import ensure_folder_exists
from minimus.utils.output_processing import stdout

init(autoreset=True)


def main():
    """Точка входа.
    """
    config = Config()
    _stdout = partial(stdout, language=config.LANGUAGE, color=Fore.CYAN)

    # обработка и сохранение аргументов запуска
    given_arguments = arguments.parse_command_line_arguments(sys.argv)
    arguments.apply_cli_args_to_config(config, given_arguments)
    output.describe_resulting_config(config, _stdout)

    # получение общих сведений о состоянии файловой системы
    metainfo = files_processing.get_metainfo(
        source_directory=config.SOURCE_DIRECTORY,
        language=config.LANGUAGE,
    )
    stored_metainfo = files_processing.get_stored_metainfo(
        source_directory=config.SOURCE_DIRECTORY,
        metafile_name=config.METAFILE_NAME,
    )

    if not metainfo:
        stdout('No source files found to work with',
               language=config.LANGUAGE, color=Fore.RED)
        return

    ensure_folder_exists(config.TARGET_DIRECTORY, config.LANGUAGE)
    ensure_folder_exists(config.README_DIRECTORY, config.LANGUAGE)

    repository = Repository(metainfo, stored_metainfo)
    repository.create_files()
    repository.read_contents_from_disk()

    run(config, repository)

    files_processing.dump_metainfo(
        directory=config.SOURCE_DIRECTORY,
        filename=config.METAFILE_NAME,
        metainfo=metainfo,
        language=config.LANGUAGE,
    )


def run(config: Config, repository: Repository):
    """Основная работа.
    """
    _stdout = partial(stdout, language=config.LANGUAGE, color=Fore.CYAN)
    # tags_to_files = map_tags_to_files(repository.get_files())

    _stdout('\nStage 1. Metafile generation')
    #     ensure_each_tag_has_metafile(tags_to_files)

    _stdout('\nStage 2. Indexes generation')
    #     ensure_index_exists(repository.get_files())
    #     ensure_readme_exists(repository.get_files())

    _stdout('\nStage 3. Main files saving')
    save_main_files(target_directory=config.TARGET_DIRECTORY,
                    repository=repository,
                    language=config.LANGUAGE)

    _stdout('\nStage 4. Additional files saving')
    save_additional_files(target_directory=config.TARGET_DIRECTORY,
                          repository=repository,
                          language=config.LANGUAGE)


if __name__ == '__main__':
    main()  # pragma: no cover
