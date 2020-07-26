# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest


class TestMarkdownSyntax(unittest.TestCase):
    def test_href(self):
        self.assertEqual(MarkdownSyntax.href('blah', 'zz'), '[blah](./zz)')
        self.assertEqual(MarkdownSyntax.href('other', 'xx'), '[other](./xx)')

    def test_tag2href(self):
        self.assertEqual(
            MarkdownSyntax.tag2href('лошадь'),
            r'[\#лошадь](./meta_loshad.md)'
        )
        self.assertEqual(
            MarkdownSyntax.tag2href('bar'),
            r'[\#bar](./meta_bar.md)'
        )

    def test_index_filename(self):
        self.assertEqual(MarkdownSyntax.get_index_filename(), 'index.md')

    def test_get_tag_filename(self):
        self.assertEqual(
            MarkdownSyntax.get_tag_filename('некий тег'), 'meta_nekiy_teg.md')
        self.assertEqual(
            MarkdownSyntax.get_tag_filename('упячка'), 'meta_upyachka.md')

    def test_extract_title(self):
        self.assertEqual(
            MarkdownSyntax.extract_title(REF_MD), 'Слон'
        )
        self.assertEqual(
            MarkdownSyntax.extract_title('XXXX'), '???'
        )

    def test_extract_tags(self):
        self.assertEqual(
            MarkdownSyntax.extract_tags(REF_MD),
            {'большой', '4 лапы', 'серый', 'хобот'}
        )