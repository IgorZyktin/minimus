# -*- coding: utf-8 -*-

"""Головной файл проекта.
"""
import sys
import time
from functools import partial

from colorama import init, Fore

from minimus import output, settings
from minimus.components.class_renderer import Renderer
from minimus.components.class_repository import Repository
from minimus.utils import arguments, files_processing
from minimus.utils.file_class_helpers import *
from minimus.utils.file_class_helpers import analyze_files
from minimus.utils.filesystem import ensure_folder_exists
from minimus.utils.output_processing import stdout

init(autoreset=True)


def main():
    """Точка входа.
    """
    # обработка и сохранение аргументов запуска
    given_arguments = arguments.parse_command_line_arguments(sys.argv)
    arguments.apply_cli_args_to_settings(given_arguments)

    # получение общих сведений о состоянии файловой системы
    metainfo = files_processing.get_metainfo()
    stored_metainfo = files_processing.get_stored_metainfo()

    if not metainfo:
        stdout('No source files found to work with', color=Fore.RED)
        return

    repository = Repository(
        renderer_type=Renderer,
        metainfo=metainfo,
        stored_metainfo=stored_metainfo,
    )
    repository.create_files()
    repository.read_contents_from_disk()

    run(repository)


def run(repository: Repository):
    """Основная работа.
    """
    timestamp = time.monotonic()

    output.start()
    output.resulting_settings()

    ensure_folder_exists(settings.TARGET_DIRECTORY)
    ensure_folder_exists(settings.README_DIRECTORY)

    output.line()

    analyze_files(repository)
    tags_to_files, associated_tags = map_tags_to_files(repository)

    _stdout = partial(stdout, color=Fore.CYAN)
    _stdout('Stage 1. Metafile generation')
    ensure_each_tag_has_metafile(tags_to_files, associated_tags)
    output.newline()

    _stdout('Stage 2. Indexes generation')
    ensure_index_exists(repository)
    ensure_readme_exists(repository)
    output.newline()

    _stdout('Stage 3. Main files saving')
    save_main_files(repository)
    output.newline()

    _stdout('Stage 4. Additional files saving')
    save_additional_files(repository)
    output.newline()

    output.line()
    files_processing.dump_metainfo(repository.metainfo)
    output.complete(time.monotonic() - timestamp)


if __name__ == '__main__':
    main()  # pragma: no cover
