# -*- coding: utf-8 -*-

"""Document rendering class.
"""
import re
from typing import List

from minimus import settings
from minimus.core.class_document import Document
from minimus.utils.output_processing import translate


class Markdown:
    """Document rendering class.
    """
    # pattern for file header
    # example: '# Header'
    HEADER_PATTERN = re.compile(r"""
        ^      # start of string
        \s*?   # zero or more optional spaces
        \#+    # one or more octotorps
        \s?    # optional space
        (.*)   # optional text
    """, flags=re.VERBOSE)

    # pattern for tag (anywhere in the text)
    # example: '{{ something }}'
    BASE_TAG_PATTERN = re.compile(r"""
        (        # arbitrary amount of occurrence
        {{       # literally double curly brackets
        \s*?     # zero or more optional spaces
        (.+?)    # some text
        \s*?     # zero or more optional spaces
        }}       # literally double curly brackets
        )        # arbitrary amount of occurrence
    """, flags=re.VERBOSE)

    def extract_header(self, content: str) -> str:
        """Extract header from the document text.
        """
        match = self.HEADER_PATTERN.match(content)
        if match:
            return match.groups()[0].strip()
        return '???'

    def extract_tags(self, content: str) -> List[str]:
        """Extract tags from the document text.
        """
        all_tags = [
            tag.group().strip('{} ')
            for tag in self.BASE_TAG_PATTERN.finditer(content)
        ]
        unique_tags = list(dict.fromkeys(all_tags).keys())
        return unique_tags

    @staticmethod
    def make_tag_patter(tag: str) -> str:
        """Make new pattern for tag replacement."""
        return r'{{\s*' + tag + r'\s*}}'

    @staticmethod
    def href(label: str, url: str) -> str:
        """Make hyperlink.

        >>> Markdown.href('Hello!', 'world')
        '[Hello!](./world)'
        """
        return '[{}]({})'.format(label, url)

    @staticmethod
    def make_filename_from_tag(tag: str) -> str:
        """Make corresponding filename from actual tag text.

        >>> Markdown.make_filename_from_tag('some tag')
        'meta_some_tag.md'
        """
        name = translate(tag, language=settings.LANGUAGE).replace(' ', '_')
        return f'meta_{name}.md'

    def parse(self, text: str) -> Document:
        """Extract features from raw text."""
        header = self.extract_header(text)
        tags = self.extract_tags(text)

        for tag in tags:
            text_from = self.make_tag_patter(tag)
            url = self.make_filename_from_tag(tag)
            text_to = self.href(tag, './' + url)
            text = re.sub(text_from, text_to, text)

        return Document(
            header=header,
            tags=tags,
            content=text,
        )
