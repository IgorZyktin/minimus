# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest

from minimus.documents import MarkdownDocument, MarkdownMetaDocument, \
    MarkdownIndexDocument
from minimus.text_file import TextFile


class TestMarkdownDocument(unittest.TestCase):
    def test_make_corresponding_filename(self):
        self.assertEqual(
            MarkdownDocument.make_corresponding_filename(
                'обжорка'),
            'obzhorka.md')
        self.assertEqual(
            MarkdownDocument.make_corresponding_filename(
                'превысокопредседательствующий'),
            'prevysokopredsedatelstvuyschiy.md')

    def test_content(self):
        file_1 = TextFile('a.txt', '', title='a')
        file_2 = TextFile('b.txt', '', title='b')
        file_3 = TextFile('c.txt', '', title='c')

        ref = """
## Все вхождения тега "suppa"

---

1 из 3. [a](./a.txt)

2 из 3. [b](./b.txt)

3 из 3. [c](./c.txt)

        """.strip() + '\n\n'

        r = MarkdownMetaDocument('suppa', [file_1, file_2, file_3])
        self.assertEqual(r.content, ref)

    # noinspection PyTypeChecker
    def test_template(self):
        doc1 = MarkdownDocument('one', [None])
        self.assertEqual(doc1.template, MarkdownDocument.BASE_TEMPLATE)

        doc2 = MarkdownDocument('two', [None], template='')
        self.assertEqual(doc2.content, '')


class TestMarkdownMetaDocument(unittest.TestCase):
    def test_make_corresponding_filename(self):
        self.assertEqual(
            MarkdownMetaDocument.make_corresponding_filename(
                'обжорка'),
            'meta_obzhorka.md')
        self.assertEqual(
            MarkdownMetaDocument.make_corresponding_filename(
                'превысокопредседательствующий'),
            'meta_prevysokopredsedatelstvuyschiy.md')

    def test_title(self):
        r = MarkdownMetaDocument('test', [])
        self.assertEqual(r.given_title, 'test')
        self.assertEqual(r.title, '## Все вхождения тега "test"')


class TestMarkdownIndexDocument(unittest.TestCase):
    def test_title(self):
        document = MarkdownIndexDocument('', [])
        self.assertEqual(document.title, '# Все записи')

    def test_corresponding_filename(self):
        document = MarkdownIndexDocument('', [])
        self.assertEqual(document.corresponding_filename, 'index.md')
