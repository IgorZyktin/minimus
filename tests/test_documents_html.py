# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest
from unittest.mock import Mock

from minimus.documents_html import (
    HypertextMetaDocument, HypertextIndexDocument
)


class TestHypertextDocument(unittest.TestCase):
    def test_corresponding_filename(self):
        config = Mock()
        config.htmt_template = ''

        document = HypertextMetaDocument(config, 'Нечто', [])
        self.assertEqual(document.corresponding_filename, 'meta_nechto.html')

        document = HypertextIndexDocument(config, '', [])
        self.assertEqual(document.corresponding_filename, 'index.html')
