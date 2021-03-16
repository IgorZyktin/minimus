# -*- coding: utf-8 -*-

"""Tests.
"""
from unittest.mock import Mock, patch, call, ANY

import pytest

from minimus.core.class_markdown import Markdown
from minimus.core.class_statistics import Statistics
from minimus.core.simple_structures import Document
from minimus.utils.utils_auto import (
    make_files_for_tags,
    make_index_file,
    make_readme_file,
)


@pytest.fixture()
def fake_fs():
    mock = Mock()
    mock.at_target.return_value = 'at'
    mock.at_readme.return_value = 'at/wtf'
    return mock


@pytest.fixture()
def fake_stats():
    statistics = Statistics()
    statistics.add_document('file1', Document(
        'header1', ['tag1', 'tag2'], '{{tag1}} and {{tag2}}', 'tag1'
    ))
    statistics.add_document('file2', Document(
        'header2', ['tag1', 'tag2'], '{{tag1}} and {{tag2}}', 'tag2'
    ))
    return statistics


def test_make_files_for_tags(fake_fs, fake_stats):
    """Must create metainfo files."""
    with patch('minimus.utils.utils_auto.stdout') as fake_stdout:
        with patch('minimus.utils.utils_locale.settings') as fake_settings:
            fake_settings.LANGUAGE = 'EN'
            make_files_for_tags(fake_fs, fake_stats, Markdown())

    fake_stdout.assert_has_calls([
        call('\t{number}. File created: {filename}', number='1 of 2',
             filename='meta_tag1.md', color=ANY),
        call('\t{number}. File created: {filename}', number='2 of 2',
             filename='meta_tag2.md', color=ANY)
    ])

    fake_fs.assert_has_calls([
        call.at_target('meta_tag1.md'),
        call.write_file(
            'at',
            '## All occurrences of the tag "tag1"\n\n\n'
            '1 of 2. [header1](./file1)\n\n'
            '2 of 2. [header2](./file2)\n\n\n\n'
            '### This tag occurs with\n\n\n'
            '1 of 1. [tag2](./meta_tag2.md)\n\n'
        ),
        call.at_target('meta_tag2.md'),
        call.write_file(
            'at',
            '## All occurrences of the tag "tag2"\n\n\n'
            '1 of 2. [header1](./file1)\n\n'
            '2 of 2. [header2](./file2)\n\n\n\n'
            '### This tag occurs with\n\n\n'
            '1 of 1. [tag1](./meta_tag1.md)\n\n'
        ),
    ])


def test_make_files_for_tags_no_associations(fake_fs):
    """Must create metainfo files."""
    statistics = Statistics()
    statistics.add_document('file1', Document(
        'header1', ['tag1'], '{{tag1}}', 'tag1'
    ))
    statistics.add_document('file2', Document(
        'header2', ['tag2'], '{{tag2}}', 'tag2'
    ))

    with patch('minimus.utils.utils_auto.stdout') as fake_stdout:
        with patch('minimus.utils.utils_locale.settings') as fake_settings:
            fake_settings.LANGUAGE = 'EN'
            make_files_for_tags(fake_fs, statistics, Markdown())

    fake_stdout.assert_has_calls([
        call('\t{number}. File created: {filename}', number='1 of 2',
             filename='meta_tag1.md', color=ANY),
        call('\t{number}. File created: {filename}', number='2 of 2',
             filename='meta_tag2.md', color=ANY)
    ])

    fake_fs.assert_has_calls([
        call.at_target('meta_tag1.md'),
        call.write_file(
            'at',
            '## All occurrences of the tag "tag1"\n\n\n'
            '1 of 1. [header1](./file1)\n\n'
        ),
        call.at_target('meta_tag2.md'),
        call.write_file(
            'at',
            '## All occurrences of the tag "tag2"\n\n\n'
            '1 of 1. [header2](./file2)\n\n'
        ),
    ])


def test_make_index_file(fake_fs, fake_stats):
    """Must create one index file."""
    with patch('minimus.utils.utils_auto.stdout') as fake_stdout:
        with patch('minimus.utils.utils_locale.settings') as fake_settings:
            fake_settings.LANGUAGE = 'EN'
            make_index_file(fake_fs, fake_stats, Markdown())

    fake_stdout.assert_has_calls([
        call('\tFile created: {filename}', filename='at', color=ANY)
    ])

    fake_fs.assert_has_calls([
        call.at_target('index.md'),
        call.write_file(
            'at',
            '# All entries\n\n\n'
            '1 of 2. [Tag1](./meta_tag1.md)\n\n'
            '* [header1](./file1)\n\n'
            '2 of 2. [Tag2](./meta_tag2.md)\n\n'
            '* [header2](./file2)\n\n'
        )
    ])


def test_make_readme_file(fake_fs, fake_stats):
    """Must create one readme file."""
    fake_fs.find_shortest_common_path.return_value = './some_folder/deeper'
    with patch('minimus.utils.utils_auto.stdout') as fake_stdout:
        with patch('minimus.utils.utils_locale.settings') as fake_settings:
            fake_settings.LANGUAGE = 'EN'
            make_readme_file(fake_fs, fake_stats, Markdown())

    fake_stdout.assert_has_calls([
        call('\tFile created: {filename}', filename='at/wtf', color=ANY)
    ])

    fake_fs.assert_has_calls([
        call.at_readme('README.md'),
        call.find_shortest_common_path(ANY, ANY),
        call.write_file(
            'at/wtf',
            '# All entries\n\n\n'
            '1 of 2. [Tag1](./some_folder/deeper/meta_tag1.md)\n\n'
            '* [header1](./some_folder/deeper/file1)\n\n'
            '2 of 2. [Tag2](./some_folder/deeper/meta_tag2.md)\n\n'
            '* [header2](./some_folder/deeper/file2)\n\n'
        )
    ])
