# -*- coding: utf-8 -*-

"""Тесты.
"""
import os
import unittest

from minimus.utils.files_processing import make_metainfo, shortest_common_path


class TestFilesProcessing(unittest.TestCase):
    def test_metainfo(self):
        res = make_metainfo('.')
        self.assertEqual(len(res), 4)

    def test_metainfo_unknown(self):
        res = make_metainfo(os.path.join('.', 'nonexistent'))
        self.assertEqual(len(res), 0)

    def test_shortest_common_path_normal(self):
        inp1 = 'C:\\users\\vasya\\documents\\other'
        inp2 = 'C:\\users\\vasya\\documents\\pictures\\new'
        res = shortest_common_path(inp1, inp2)
        self.assertEqual('..\\pictures\\new', res)

    def test_shortest_common_path_diff(self):
        inp1 = 'C:\\users\\vasya'
        inp2 = 'D:\\users\\vasya'
        res = shortest_common_path(inp1, inp2)
        self.assertEqual('D:\\users\\vasya', res)

    def test_shortest_common_path_short(self):
        inp1 = 'C:\\users\\vasya'
        inp2 = 'C:\\users\\vasya\\documents\\pictures\\new'
        res = shortest_common_path(inp1, inp2)
        self.assertEqual('.\\documents\\pictures\\new', res)

    def test_shortest_common_path_same_size(self):
        inp1 = 'C:\\users\\user_1'
        inp2 = 'C:\\users\\user_2'
        res = shortest_common_path(inp1, inp2)
        self.assertEqual('..\\user_2', res)
