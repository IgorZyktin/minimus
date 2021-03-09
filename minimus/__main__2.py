# -*- coding: utf-8 -*-

"""Starting file.
"""
import sys

from colorama import init

from minimus import settings
from minimus.core.class_file_proxy import FileProxy
from minimus.core.class_file_repository import FileRepository
from minimus.core.class_filesystem_interactor import FilesystemInteractor
from minimus.core.class_path_converter import PathConverter
from minimus.utils import arguments

init(autoreset=True)


def main():
    """Entry point.
    """
    # add command line arguments to settings
    given_arguments = arguments.parse_command_line_arguments(sys.argv)
    arguments.apply_cli_args_to_settings(given_arguments)

    converter = PathConverter(source_path=settings.SOURCE_DIRECTORY,
                              target_path=settings.TARGET_DIRECTORY)

    interactor = FilesystemInteractor()

    # 1. get all paths
    repository = get_file_repository(converter, interactor,
                                     settings.METAFILE_NAME)

    # 2. save all side files
    save_all_side_files(converter)



    print(repository, len(repository))
    # get filesystem state
    # metainfo = files_processing.get_metainfo()
    # stored_metainfo = files_processing.get_stored_metainfo()

#     if not metainfo:
#         stdout('No source files found to work with', color=Fore.RED)
#         return
#
#     repository = Repository(
#         renderer_type=Renderer,
#         metainfo=metainfo,
#         stored_metainfo=stored_metainfo,
#     )
#     repository.create_files()
#     repository.read_contents_from_disk()
#
#     run(repository)
#
#
# def run(repository: Repository):
#     """Основная работа.
#     """
#     timestamp = time.monotonic()
#
#     output.start()
#     output.resulting_settings()
#
#     ensure_folder_exists(settings.TARGET_DIRECTORY)
#     ensure_folder_exists(settings.README_DIRECTORY)
#
#     output.line()
#
#     analyze_files(repository)
#     tags_to_files, associated_tags = map_tags_to_files(repository)
#
#     _stdout = partial(stdout, color=Fore.CYAN)
#     _stdout('Stage 1. Metafile generation')
#     ensure_each_tag_has_metafile(tags_to_files, associated_tags)
#     output.newline()
#
#     _stdout('Stage 2. Indexes generation')
#     ensure_index_exists(repository)
#     ensure_readme_exists(repository)
#     output.newline()
#
#     _stdout('Stage 3. Main files saving')
#     save_main_files(repository)
#     output.newline()
#
#     _stdout('Stage 4. Additional files saving')
#     save_additional_files(repository)
#     output.newline()
#
#     output.line()
#     files_processing.dump_metainfo(repository.metainfo)
#     output.complete(time.monotonic() - timestamp)


def get_file_repository(converter, interactor,
                        metafile_name) -> FileRepository:
    """Load source data from disk."""
    existing_stats = interactor \
        .get_existing_stats(converter.source_path, metafile_name)

    repository = FileRepository()

    for path, filename in interactor \
            .iterate_on_unique_filenames(converter.source_path):
        stats = interactor.get_stats_for_file(path, filename)
        is_changed = existing_stats.get(filename) == stats
        proxy = FileProxy(path, filename, stats, is_changed)
        repository.add_proxy(proxy)

    return repository


def save_all_side_files(converter, interactor, repository):
    for proxy in repository:
        if not proxy.filename.endswith('.md'):
            interactor.copy(
                interactor.join(proxy.path, proxy.filename),
            )


if __name__ == '__main__':
    main()  # pragma: no cover
