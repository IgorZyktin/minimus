# -*- coding: utf-8 -*-

"""Starting file.
"""
import sys
import time

from colorama import init

from minimus import settings
from minimus.core.class_file_repository import FileRepository
from minimus.core.class_filesystem import Filesystem
from minimus.core.class_markdown import Markdown
from minimus.core.class_stats import Stats
from minimus.utils import arguments, output, utils_auto

init(autoreset=True)


def main():
    """Entry point.
    """
    start_time = time.monotonic()
    output.show_greeting_message()

    # 1. initiate settings
    given_arguments = arguments.parse_command_line_arguments(sys.argv)
    arguments.apply_cli_args_to_settings(given_arguments)

    # 2. create components
    filesystem = Filesystem(settings.SOURCE_DIRECTORY,
                            settings.TARGET_DIRECTORY,
                            settings.README_DIRECTORY)
    repository = FileRepository(filesystem)
    renderer = Markdown()
    stats = Stats()

    if any([filesystem.ensure_folder_exists(filesystem.source_directory),
            filesystem.ensure_folder_exists(filesystem.target_directory),
            filesystem.ensure_folder_exists(filesystem.readme_directory)]):
        output.show_separation_line()

    output.show_resulting_settings()
    output.show_separation_line()

    # 3. handle user files
    output.show_user_files_rendering()
    repository.load_files()
    repository.update_files(stats, renderer)
    repository.save_files()

    # 4. handle automatically created files
    output.show_auto_files_rendering()
    utils_auto.make_files_for_tags(filesystem, stats, renderer)

    # 5. handle indexes
    output.show_index_files_rendering()
    utils_auto.make_index_file(filesystem, stats, renderer)
    utils_auto.make_readme_file(filesystem, stats, renderer)

    output.show_final_message(time.monotonic() - start_time)


if __name__ == '__main__':
    main()  # pragma: no cover
