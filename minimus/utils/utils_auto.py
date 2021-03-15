# -*- coding: utf-8 -*-

"""Utils for handling automatically created files.
"""
from colorama import Fore

from minimus.utils.utils_locale import stdout
from minimus.utils.utils_text import numerate


def make_files_for_tags(filesystem, statistics, renderer):
    """Generate file for each tag."""
    associated_tags = statistics.get_associated_tags()
    generator = numerate(statistics.get_tags_to_files().items())
    for number, (tag, corresponding_files) in generator:
        associations = associated_tags.get(tag)
        filename, body = renderer.render_metafile(tag,
                                                  corresponding_files,
                                                  associations)
        path = filesystem.at_target(filename)
        filesystem.write_file(path, body)
        stdout('\t{number}. File created: {filename}',
               number=number, filename=filename, color=Fore.YELLOW)


def make_index_file(filesystem, statistics, renderer):
    """Generate file for index.md."""
    make_index_base(filesystem, statistics, renderer, 'index.md')


def make_readme_file(filesystem, statistics, renderer):
    """Generate file for README.md."""
    make_index_base(filesystem, statistics, renderer, 'README.md')


def make_index_base(filesystem, statistics, renderer, filename: str) -> None:
    """Generate generic index file."""
    path = filesystem.at_readme(filename)
    categories = statistics.get_categories_to_files()
    body = renderer.render_index(categories)

    filesystem.write_file(path, body)
    stdout('\tFile created: {filename}',
           filename=path, color=Fore.YELLOW)
