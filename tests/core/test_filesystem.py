# -*- coding: utf-8 -*-

"""Tests.
"""
import os
import re
import tempfile
from unittest.mock import patch, ANY

import pytest

from minimus.core.class_filesystem import Filesystem
from minimus.utils.utils_locale import translate


@pytest.fixture()
def inst():
    return Filesystem(
        source_directory='source',
        target_directory='target',
        readme_directory='readme',
    )


def test_shortest_common_path_normal(inst):
    current_folder = os.sep.join(['C', 'users', 'vasya', 'documents', 'other'])
    target_folder = os.sep.join(['C', 'users', 'vasya',
                                 'documents', 'pictures', 'new'])
    result = inst.find_shortest_common_path(current_folder, target_folder)
    assert result == os.sep.join(['..', 'pictures', 'new'])


def test_shortest_common_path_diff(inst):
    current_folder = os.sep.join(['C', 'users', 'vasya'])
    target_folder = os.sep.join(['D', 'users', 'vasya'])
    result = inst.find_shortest_common_path(current_folder, target_folder)
    assert result == os.sep.join(['D', 'users', 'vasya'])


def test_shortest_common_path_short(inst):
    current_folder = os.sep.join(['C', 'users', 'vasya'])
    target_folder = os.sep.join(['C', 'users', 'vasya', 'documents',
                                 'pictures', 'new'])
    result = inst.find_shortest_common_path(current_folder, target_folder)
    assert result == os.sep.join(['.', 'documents', 'pictures', 'new'])


def test_shortest_common_path_same_size(inst):
    current_folder = os.sep.join(['C', 'users', 'user_1'])
    target_folder = os.sep.join(['C', 'users', 'user_2'])
    result = inst.find_shortest_common_path(current_folder, target_folder)
    assert result == '..' + os.sep + 'user_2'


def test_shortest_common_path_same(inst):
    current_folder = os.sep.join(['C', 'users', 'user_1'])
    target_folder = os.sep.join(['C', 'users', 'user_1'])
    result = inst.find_shortest_common_path(current_folder, target_folder)
    assert result == '.'


def test_join(inst):
    assert inst.join('folder_a', 'folder_b') \
           == os.path.join('folder_a', 'folder_b')


def test_ensure_folder_exists_one_level(inst):
    with tempfile.TemporaryDirectory() as tmp_dir, \
            patch('minimus.core.class_filesystem.stdout') as fake_stdout:
        path = inst.join(tmp_dir, 'folder')
        assert not os.path.exists(path)
        inst.ensure_folder_exists(path)
        assert os.path.exists(path)

    fake_stdout.assert_called_once()
    assert not os.path.exists(path)


def test_ensure_folder_exists_deep(inst):
    with tempfile.TemporaryDirectory() as tmp_dir, \
            patch('minimus.core.class_filesystem.stdout') as fake_stdout:
        path = inst.join(tmp_dir, 'a', 'b', 'c', 'd', 'e')
        assert not os.path.exists(path)
        inst.ensure_folder_exists(path)
        assert os.path.exists(path)

    assert len(fake_stdout.mock_calls) == 5
    assert not os.path.exists(path)


def test_at(inst):
    assert inst.at_source('wtf') == 'source' + os.sep + 'wtf'
    assert inst.at_target('wtf') == 'target' + os.sep + 'wtf'
    assert inst.at_readme('wtf') == 'readme' + os.sep + 'wtf'


def test_get_default_stats(inst):
    stats = inst.get_default_stats()
    assert 'created_at' in stats
    assert 'modified_at' in stats
    assert 'size' in stats
    assert max(x for x in stats.values()) <= 0


def test_write_read_stats(inst):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = inst.join(tmp_dir, 'test.txt')
        inst.write_file(path, 'something')
        stats = inst.get_stats_for_file(path)
        content = inst.read_file(path)
        assert content == 'something'
        assert stats == {
            'created_at': ANY,
            'modified_at': ANY,
            'size': 9,
        }


def test_write_read_nonexistent(inst):
    path = 'somewhere'
    stats = inst.get_stats_for_file(path)
    assert stats == inst.get_default_stats()

    content = inst.read_file(path)
    assert content == ''


def test_copy(inst):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = inst.join(tmp_dir, 'test.txt')
        path2 = inst.join(tmp_dir, 'test2.txt')
        inst.write_file(path, 'something')
        inst.copy_file(path, path2)
        content = inst.read_file(path2)
        assert content == 'something'


def test_iterate_on_unique_filenames_normal(inst):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path1 = inst.join(tmp_dir, 'test1.txt')
        path2 = inst.join(tmp_dir, 'test2.txt')
        inst.write_file(path1, 'something')
        inst.write_file(path2, 'something')

        files = inst.iterate_on_unique_filenames(tmp_dir)
        assert list(files) == [
            (tmp_dir, 'test1.txt'),
            (tmp_dir, 'test2.txt'),
        ]


def test_iterate_on_unique_filenames_nothing(inst):
    with tempfile.TemporaryDirectory() as tmp_dir:
        files = inst.iterate_on_unique_filenames(tmp_dir)
        assert list(files) == []


def test_iterate_on_unique_filenames_sub_folders(inst):
    msg = translate('Current version of Minimus does '
                    'not support nested folders: {directories}').format(
        directories="['folder']")

    with tempfile.TemporaryDirectory() as tmp_dir, \
            patch('minimus.core.class_filesystem.stdout'):
        path1 = inst.join(tmp_dir, 'test1.txt')
        inst.ensure_folder_exists(inst.join(tmp_dir, 'folder'))
        inst.write_file(path1, 'something')

        with pytest.raises(FileExistsError, match=re.escape(msg)):
            list(inst.iterate_on_unique_filenames(tmp_dir))


def test_iterate_on_duplicate_filenames(inst):
    msg = translate('Filenames are supposed to be unique: {filename}').format(
        filename="0")
    with patch('minimus.core.class_filesystem.os') as fake_os:
        fake_os.walk.return_value = [('wtf', [], [x, x]) for x in range(3)]

        with pytest.raises(FileExistsError, match=re.escape(msg)):
            list(inst.iterate_on_unique_filenames('path'))
