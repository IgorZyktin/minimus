# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest
from unittest.mock import Mock

from minimus.old.documents_html import (
    HypertextMetaDocument, HypertextIndexDocument, HypertextDocument
)


class TestHypertextDocument(unittest.TestCase):
    def test_title(self):
        config = Mock()
        config.htmt_template = ''
        document = HypertextDocument(config, 'Нечто', [])
        self.assertEqual(document.title, 'Нечто')

        document = HypertextIndexDocument(config, 'Нечто', [])
        self.assertEqual(document.title, 'Стартовая страница')

        document = HypertextMetaDocument(config, 'Нечто', [])
        self.assertEqual(document.title, 'Все вхождения тега "Нечто"')

    def test_corresponding_filename(self):
        config = Mock()
        config.htmt_template = ''

        res = HypertextDocument.make_corresponding_filename('упячка')
        self.assertEqual(res, 'upyachka.html')

        document = HypertextMetaDocument(config, 'Нечто', [])
        self.assertEqual(document.corresponding_filename, 'meta_nechto.html')

        document = HypertextIndexDocument(config, '', [])
        self.assertEqual(document.corresponding_filename, 'index.html')

    def test_render_graph(self):
        config = Mock()
        config.htmt_template = ''

        document = HypertextDocument(config, 'Нечто', [])
        self.assertEqual(document.render_graph([]), {})
