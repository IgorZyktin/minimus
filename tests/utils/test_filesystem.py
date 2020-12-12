# -*- coding: utf-8 -*-

"""Тесты.
"""
import os
import tempfile
from unittest.mock import patch

from minimus.utils.filesystem import find_shortest_common_path, get_ext, join, \
    ensure_folder_exists


def test_shortest_common_path_normal():
    current_folder = 'C:\\users\\vasya\\documents\\other'
    target_folder = 'C:\\users\\vasya\\documents\\pictures\\new'
    result = find_shortest_common_path(current_folder, target_folder)
    assert result == '..\\pictures\\new'


def test_shortest_common_path_diff():
    current_folder = 'C:\\users\\vasya'
    target_folder = 'D:\\users\\vasya'
    result = find_shortest_common_path(current_folder, target_folder)
    assert result == 'D:\\users\\vasya'


def test_shortest_common_path_short():
    current_folder = 'C:\\users\\vasya'
    target_folder = 'C:\\users\\vasya\\documents\\pictures\\new'
    result = find_shortest_common_path(current_folder, target_folder)
    assert result == '.\\documents\\pictures\\new'


def test_shortest_common_path_same_size():
    current_folder = 'C:\\users\\user_1'
    target_folder = 'C:\\users\\user_2'
    result = find_shortest_common_path(current_folder, target_folder)
    assert result == '..\\user_2'


def test_shortest_common_path_same():
    current_folder = 'C:\\users\\user_1'
    target_folder = 'C:\\users\\user_1'
    result = find_shortest_common_path(current_folder, target_folder)
    assert result == '.'


def test_get_ext():
    assert get_ext('somefile.txt') == 'txt'
    assert get_ext('OTHER.HTML') == 'html'


def test_join():
    assert join('folder_a', 'folder_b') == os.path.join('folder_a', 'folder_b')


def test_ensure_folder_exists_one_level():
    with tempfile.TemporaryDirectory() as tmp_dir, \
            patch('minimus.utils.filesystem.stdout'):
        path = join(tmp_dir, 'folder')
        assert not os.path.exists(path)
        ensure_folder_exists(path, language='EN')
        assert os.path.exists(path)
