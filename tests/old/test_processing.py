# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest

from minimus.old.processing import map_tags_to_files
from minimus.old.text_file import TextFile


class TestMapTagsToFiles(unittest.TestCase):
    def test_map_tags_to_files(self):
        file_1 = TextFile('a.txt', '# File 1\n\\#tag1\n\\#tag2')
        file_2 = TextFile('b.txt', '# File 1\n\\#tag2\n\\#tag3')
        file_3 = TextFile('c.txt', '# File 1\n\\#tag3\n\\#tag1')

        mapped = map_tags_to_files([file_1, file_2, file_3])

        ref = {
            'tag1': [file_1, file_3],
            'tag2': [file_1, file_2],
            'tag3': [file_2, file_3],
        }

        self.assertEqual(mapped, ref)

    def test_ensure_each_tag_has_metafile(self):
        pass
        # FIXME

    def test_ensure_each_tag_has_link(self):
        pass
        # FIXME

    def test_ensure_index_exists(self):
        pass
        # FIXME
