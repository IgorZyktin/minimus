# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest

from minimus.documents import (
    HypertextIndexDocument, HypertextDocument, HypertextMetaDocument
)


class TestHypertextDocument(unittest.TestCase):
    # noinspection PyTypeChecker
    def test_corresponding_filename(self):
        document = HypertextDocument(None, 'Нечто', [])
        self.assertEqual(document.corresponding_filename, 'nechto.html')
        self.assertEqual(document.title, 'Нечто')

        document = HypertextMetaDocument(None, 'Нечто', [])
        self.assertEqual(document.corresponding_filename, 'meta_nechto.html')

        document = HypertextIndexDocument(None, '', [])
        self.assertEqual(document.corresponding_filename, 'index.html')
