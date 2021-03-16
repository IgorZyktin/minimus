# -*- coding: utf-8 -*-

"""Document rendering class.
"""
import re
from typing import List, Tuple, Dict

from minimus.core.class_abstract_renderer import AbstractRenderer
from minimus.core.simple_structures import Document
from minimus.utils.utils_locale import transliterate, translate as _
from minimus.utils.utils_text import numerate


class Markdown(AbstractRenderer):
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
    TAG_PATTERN = re.compile(r"""
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
            for tag in self.TAG_PATTERN.finditer(content)
        ]
        unique_tags = list(dict.fromkeys(all_tags).keys())
        return unique_tags

    @staticmethod
    def make_tag_pattern(tag: str) -> str:
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
        name = transliterate(tag).replace(' ', '_')
        return f'meta_{name}.md'

    @staticmethod
    def local(path: str) -> str:
        """Ensure path is pointing to a local file.
        """
        if not path.startswith('./'):
            return './' + path
        return path

    def extract_features(self, text: str) -> Document:
        """Extract features from raw text."""
        header = self.extract_header(text)
        tags = self.extract_tags(text)

        for tag in tags:
            text_from = self.make_tag_pattern(tag)
            url = self.make_filename_from_tag(tag)
            text_to = self.href(tag, self.local(url))
            text = re.sub(text_from, text_to, text)

        return Document(header=header,
                        tags=tags,
                        content=text,
                        category=tags[0] if tags else '')

    def render_metafile(self, tag: str,
                        corresponding_files: List[Tuple[str, str]],
                        associations: List[str]) -> Tuple[str, str]:
        """Render metainfo file."""
        filename = self.make_filename_from_tag(tag)

        # make them unique but preserve order
        associations = [
            x for x in dict.fromkeys(associations)
            if x != tag
        ]

        lines = [
            _('## All occurrences of the tag "{tag}"').format(tag=tag),
            '\n'
        ]
        corresponding_files.sort(key=lambda pair: pair[1])
        for number, (sub_filename, header) in numerate(corresponding_files):
            href = self.href(header, self.local(sub_filename))
            lines.append(f'{number}. {href}\n')

        if associations:
            lines.extend([
                '\n',
                _('### This tag occurs with'),
                '\n'
            ])
            for number, association in numerate(sorted(associations)):
                sub_filename = self.make_filename_from_tag(association)
                href = self.href(association, self.local(sub_filename))
                lines.append(f'{number}. {href}\n')

        lines.append('')
        return filename, '\n'.join(lines)

    def render_index(self, category_to_files: Dict[str, List[Tuple[str, str]]],
                     root: str = '') -> str:
        """Render index file."""
        lines = [
            _('# All entries'),
            '\n'
        ]
        collection = list(category_to_files.items())
        collection.sort(key=lambda pair: pair[0])

        if not root:
            root = './'
        else:
            root = root.rstrip().rstrip('/') + '/'

        for number, (cat, files) in numerate(collection):
            filename = self.make_filename_from_tag(cat)
            href = self.href(cat.title(), root + filename)
            lines.append(f'{number}. {href}\n')

            for sub_filename, header in files:
                href = self.href(header, root + sub_filename)
                lines.append(f'* {href}\n')

        lines.append('')
        return '\n'.join(lines)
