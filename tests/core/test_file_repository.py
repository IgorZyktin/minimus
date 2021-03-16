# -*- coding: utf-8 -*-

"""Tests.
"""
import os
from unittest.mock import Mock, call, patch, ANY

from minimus.core.class_file_repository import FileRepository
from minimus.core.class_statistics import Statistics
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


def test_save_files_no_change(repository):
    """Must avoid saving changes on disk."""
    statistics = Statistics()
    repository.load_files()
    repository.update_files(statistics, FakeRenderer())
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
        call('\t{number}. No changes detected: {filename}', number='1 из 3',
             filename='somefile1.md'),
        call('\t{number}. No changes detected: {filename}', number='2 из 3',
             filename='somefile2.md'),
        call('\t{number}. No changes detected: {filename}', number='3 из 3',
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
        call('\t{number}. Copied file: {filename}', number='1 из 3',
             filename='somefile1.md', color=ANY),
        call('\t{number}. Saved changes: {filename}', number='2 из 3',
             filename='somefile2.md', color=ANY),
        call('\t{number}. Saved changes: {filename}', number='3 из 3',
             filename='somefile3.md', color=ANY)
    ])
