# -*- coding: utf-8 -*-

"""Utils for handling automatically created files.
"""
from colorama import Fore

from minimus.utils.output_processing import stdout
from minimus.utils.text_processing import numerate


def make_files_for_tags(converter, interactor, stats, renderer):
    generator = numerate(stats.tags_to_files.items())
    for number, (tag, corresponding_files) in generator:
        associations = stats.associated_tags.get(tag)
        filename, body = renderer.render_metafile(tag,
                                                  corresponding_files,
                                                  associations)
        path = interactor.join(converter.target_directory, filename)
        interactor.write_file(path, body)
        stdout('\t{number}. File created: {filename}',
               number=number, filename=filename, color=Fore.YELLOW)


def make_index_file(converter, interactor, stats, renderer):
    filename = 'index.md'
    path = interactor.join(converter.target_directory, filename)
    body = renderer.render_index(stats.category_to_files)
    interactor.write_file(path, body)
    stdout('\tFile created: {filename}',
           filename=path, color=Fore.YELLOW)


def make_readme_file(converter, interactor, stats, renderer):
    filename = 'README.md'
    path = interactor.join(converter.readme_directory, filename)
    body = renderer.render_index(stats.category_to_files)
    interactor.write_file(path, body)
    stdout('\tFile created: {filename}',
           filename=path, color=Fore.YELLOW)
