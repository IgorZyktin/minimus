# -*- coding: utf-8 -*-

"""Utils for handling automatically created files.
"""
from colorama import Fore

from minimus.core.class_abstract_renderer import AbstractRenderer
from minimus.core.class_filesystem import Filesystem
from minimus.core.class_statistics import Statistics
from minimus.utils.utils_locale import stdout
from minimus.utils.utils_text import numerate


def make_files_for_tags(filesystem: Filesystem, statistics: Statistics,
                        renderer: AbstractRenderer) -> None:
    """Generate file for each tag."""
    associated_tags = statistics.get_associated_tags()
    generator = numerate(statistics.get_tags_to_files().items())
    for number, (tag, corresponding_files) in generator:
        associations = sorted(associated_tags.get(tag, []))
        filename, body = renderer.render_metafile(tag,
                                                  corresponding_files,
                                                  associations)
        path = filesystem.at_target(filename)
        filesystem.write_file(path, body)
        stdout('\t{number}. File created: {filename}',
               number=number, filename=filename, color=Fore.YELLOW)


def make_index_file(filesystem: Filesystem, statistics: Statistics,
                    renderer: AbstractRenderer) -> None:
    """Generate file for index.md."""
    path = filesystem.at_target('index.md')
    make_index_base(filesystem, statistics, renderer, path)


def make_readme_file(filesystem: Filesystem, statistics: Statistics,
                     renderer: AbstractRenderer) -> None:
    """Generate file for README.md."""
    path = filesystem.at_readme('README.md')
    root = filesystem.find_shortest_common_path(filesystem.readme_directory,
                                                filesystem.target_directory)
    root = root.replace('\\', '/')
    make_index_base(filesystem, statistics, renderer, path, root)


def make_index_base(filesystem: Filesystem, statistics: Statistics,
                    renderer: AbstractRenderer, path: str, root: str = ''
                    ) -> None:
    """Generate generic index file."""
    categories = statistics.get_categories_to_files()
    body = renderer.render_index(categories, root)

    filesystem.write_file(path, body)
    stdout('\tFile created: {filename}',
           filename=path, color=Fore.YELLOW)
