# -*- coding: utf-8 -*-

"""Tests.
"""
import os
from unittest.mock import Mock, call, patch, ANY

from minimus.core.class_file_repository import FileRepository
from minimus.core.class_statistics import Statistics
from minimus.core.simple_structures import File
from tests.conftest import FakeRenderer


def test_get_meta_path(repository_real_fs):
    """Must return path to metafile."""
    assert repository_real_fs.get_meta_path() \
           == os.sep.join(['source', 'meta.json'])


def test_get_existing_meta():
    """Must load metainfo from disk."""
    fake_filesystem = Mock()
    fake_filesystem.read_file.return_value = '{"test": 1}'
    repository = FileRepository(fake_filesystem)
    assert repository.get_existing_meta() == {'test': 1}


def test_load_files(repository, ref_files_in_repo):
    """Must create map of File instances."""
    repository.load_files()
    assert list(repository) == ref_files_in_repo


def test_update_files(repository, ref_upd_files_in_repo):
    """Must update contents of all files."""
    statistics = Statistics()
    repository.load_files()
    repository.update_files(statistics, FakeRenderer())
    assert list(repository) == ref_upd_files_in_repo


def test_update_files_not_markdown():
    """Must ignore not markdown files."""
    fake_filesystem = Mock()
    fake_filesystem.read_file.return_value = '{}'
    fake_filesystem.get_stats_for_file.return_value = {}
    fake_filesystem.at_source.return_value = 'src'

    fake_filesystem.iterate_on_unique_filenames.return_value = [
        ('folder1', 'meta.json'),
        ('folder1', 'somefile1.txt'),
        ('folder1', 'somefile2.md'),
        ('folder1', 'somefile3.md'),
    ]
    repository = FileRepository(fake_filesystem)
    statistics = Statistics()
    repository.load_files()
    repository._storage['somefile2.md'].content = None
    repository.update_files(statistics, FakeRenderer())
    assert list(repository) == [
        File(directory='folder1', filename='somefile1.txt', content='',
             is_markdown=False, is_new=True),
        File(directory='folder1', filename='somefile2.md', content=None,
             is_markdown=True, is_new=True),
        File(directory='folder1', filename='somefile3.md', content='wtf',
             is_markdown=True, is_new=True),
    ]


def test_save_files_no_change(repository):
    """Must avoid saving changes on disk."""
    statistics = Statistics()
    repository.load_files()
    repository.update_files(statistics, FakeRenderer())

    for file in repository:
        file.is_new = False

    with patch('minimus.utils.utils_locale.settings') as fake_settings:
        fake_settings.LANGUAGE = 'EN'
        with patch('minimus.core.class_file_repository.stdout') as fake_stdout:
            repository.save_files()

    repository._filesystem.write_file.assert_has_calls([
        call('src',
             '{\n'
             '    "somefile1.md": {},\n'
             '    "somefile2.md": {},\n'
             '    "somefile3.md": {}\n'
             '}')
    ])

    fake_stdout.assert_has_calls([
        call('\t{number}. No changes detected: {filename}', number='1 of 3',
             filename='somefile1.md'),
        call('\t{number}. No changes detected: {filename}', number='2 of 3',
             filename='somefile2.md'),
        call('\t{number}. No changes detected: {filename}', number='3 of 3',
             filename='somefile3.md')
    ])


def test_save_files(repository):
    """Must save changes on disk."""
    statistics = Statistics()
    repository.load_files()
    repository.update_files(statistics, FakeRenderer())

    for file in repository:
        file.is_new = True
        if file.filename == 'somefile1.md':
            file.is_markdown = False

    with patch('minimus.utils.utils_locale.settings') as fake_settings:
        fake_settings.LANGUAGE = 'EN'
        with patch('minimus.core.class_file_repository.stdout') as fake_stdout:
            repository.save_files()

    repository._filesystem.write_file.assert_has_calls([
        call('src',
             '{\n'
             '    "somefile1.md": {},\n'
             '    "somefile2.md": {},\n'
             '    "somefile3.md": {}\n'
             '}')
    ])

    fake_stdout.assert_has_calls([
        call('\t{number}. Copied file: {filename}', number='1 of 3',
             filename='somefile1.md', color=ANY),
        call('\t{number}. Saved changes: {filename}', number='2 of 3',
             filename='somefile2.md', color=ANY),
        call('\t{number}. Saved changes: {filename}', number='3 of 3',
             filename='somefile3.md', color=ANY)
    ])
