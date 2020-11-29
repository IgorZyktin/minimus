# -*- coding: utf-8 -*-

"""Набор классов для документов.

Документы в проекте это просто контейнеры для текста.
Они не умеют работать непосредственно с файловой системой.
"""
import string

import minimus.utils.text_processing
from minimus.old.abstract import AbstractDocument
from minimus.old.markdown_parser import MarkdownParser
from minimus.old.syntax import Syntax


class MarkdownDocument(AbstractDocument):
    """Базовый markdown документ.
    """

    BASE_TEMPLATE = """
$title

---
    """.strip() + '\n\n'

    @classmethod
    def make_corresponding_filename(cls, title: str) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return '{name}.md'.format(name=Syntax.transliterate(title))

    @property
    def content(self) -> str:
        """Вернуть скомпонованный текст документа.
        """
        if not self.template or not self.files:
            return ''

        template = string.Template(self.template)
        head = template.safe_substitute({
            'title': self.title,
        })

        lines = []
        # noinspection PyTypeChecker
        for number, file in minimus.utils.text_processing.numerate(sorted(self.files)):
            lines.append('{}. {}\n'.format(
                number,
                MarkdownParser.href(file.title, file.filename),
            ))

        lines.append('')
        body = '\n'.join(lines)

        return head + body


class MarkdownMetaDocument(MarkdownDocument):
    """Метадокумент markdown.
    """

    @property
    def title(self) -> str:
        """Вернуть заголовок документа.
        """
        return f'## Все вхождения тега "{self.given_title}"'

    @classmethod
    def make_corresponding_filename(cls, title: str) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return 'meta_{name}.md'.format(name=Syntax.transliterate(title))


class MarkdownIndexDocument(MarkdownDocument):
    """Markdown индекс (стартовый файл).
    """

    @property
    def title(self) -> str:
        """Вернуть заголовок документа.
        """
        return '# Все записи'

    @property
    def corresponding_filename(self) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return 'index.md'
