# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest

from minimus.old.documents_markdown import MarkdownDocument, MarkdownMetaDocument
from minimus.old.markdown_parser import MarkdownParser
from tests.old.content import REF_MD, REF_MD_WITH_LINKS


class TestMarkdownParser(unittest.TestCase):
    def test_href(self):
        self.assertEqual(MarkdownParser.href('blah', 'zz'), '[blah](./zz)')
        self.assertEqual(MarkdownParser.href('other', 'xx'), '[other](./xx)')

    def test_tag2href(self):
        self.assertEqual(
            MarkdownParser.tag2href('лошадь', MarkdownDocument),
            r'[\#лошадь](./loshad.md)'
        )
        self.assertEqual(
            MarkdownParser.tag2href('bar', MarkdownDocument),
            r'[\#bar](./bar.md)'
        )
        self.assertEqual(
            MarkdownParser.tag2href('лошадь', MarkdownMetaDocument),
            r'[\#лошадь](./meta_loshad.md)'
        )
        self.assertEqual(
            MarkdownParser.tag2href('bar', MarkdownMetaDocument),
            r'[\#bar](./meta_bar.md)'
        )

    def test_extract_title(self):
        self.assertEqual(
            MarkdownParser.extract_title(REF_MD), 'Слон'
        )
        self.assertEqual(
            MarkdownParser.extract_title('XXXX'), '???'
        )

    def test_extract_tags(self):
        self.assertEqual(
            MarkdownParser.extract_tags(REF_MD),
            {'большой', '4 лапы', 'серый', 'хобот'}
        )

    def test_replace_tags_with_hrefs(self):
        self.assertEqual(
            MarkdownParser.replace_tags_with_hrefs(
                content=REF_MD,
                tags=MarkdownParser.extract_tags(REF_MD),
                maker=MarkdownMetaDocument,
            ), REF_MD_WITH_LINKS
        )
