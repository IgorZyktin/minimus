# -*- coding: utf-8 -*-

"""Тесты.
"""
import os
import unittest

from minimus.utils.files_processing import make_metainfo


class TestFilesProcessing(unittest.TestCase):
    def test_metainfo(self):
        res = make_metainfo('.')
        self.assertEqual(len(res), 4)

    def test_metainfo_unknown(self):
        res = make_metainfo(os.path.join('.', 'nonexistent'))
        self.assertEqual(len(res), 0)
