# -*- coding: utf-8 -*-

"""Starting file.
"""
import sys
import time

from colorama import init

from minimus import settings
from minimus.core.class_file_repository import FileRepository
from minimus.core.class_filesystem_interactor import FilesystemInteractor
from minimus.core.class_markdown import Markdown
from minimus.core.class_path_converter import PathConverter
from minimus.core.class_stats import Stats
from minimus.utils import arguments, output, utils_auto

init(autoreset=True)


def main():
    """Entry point.
    """
    start_time = time.monotonic()
    output.show_greeting_message()

    # 1. create components
    interactor = FilesystemInteractor()
    converter = PathConverter(interactor,
                              settings.BASE_PATH,
                              settings.SOURCE_DIRECTORY,
                              settings.TARGET_DIRECTORY,
                              settings.README_DIRECTORY)
    markdown = Markdown()
    stats = Stats()
    repository = FileRepository(converter, interactor)

    # 2. initiate settings
    given_arguments = arguments.parse_command_line_arguments(sys.argv)
    arguments.apply_cli_args_to_settings(given_arguments)

    if any([interactor.ensure_folder_exists(settings.SOURCE_DIRECTORY),
            interactor.ensure_folder_exists(settings.TARGET_DIRECTORY),
            interactor.ensure_folder_exists(settings.README_DIRECTORY)]):
        output.show_separation_line()

    output.show_resulting_settings()
    output.show_separation_line()

    # 3. handle user files
    repository.load_files()
    repository.update_files(stats, markdown)
    repository.save_files()

    # 4. handle automatically created files
    utils_auto.make_files_for_tags(converter, interactor, stats, markdown)
    utils_auto.make_index_file(converter, interactor, stats, markdown)
    utils_auto.make_readme_file(converter, interactor, stats, markdown)

    output.show_final_message(time.monotonic() - start_time)


if __name__ == '__main__':
    main()  # pragma: no cover
