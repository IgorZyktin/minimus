# -*- coding: utf-8 -*-

"""Utils for handling automatically created files.
"""


def make_files_for_tags(router, interactor, stats, markdown):
    print('make_files_for_tags')
    for tag, corresponding_files in stats.tags_to_files.items():
        print(tag, corresponding_files)


def make_index_file(router, interactor, stats, markdown):
    print('make_index_file')


def make_readme_file(router, interactor, stats, markdown):
    print('make_readme_file')
