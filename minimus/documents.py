# -*- coding: utf-8 -*-

"""Набор классов для документов.

Документы в проекте это просто контейнеры для текста.
Они не умеют работать непосредственно с файловой системой.
"""
import string

from minimus.abstract import AbstractDocument, MetaMixin
from minimus.markdown_parser import MarkdownParser
from minimus.syntax import Syntax


class MarkdownDocument(AbstractDocument):
    """Базовый markdown документ.
    """

    BASE_TEMPLATE = """
$title
---
    """.strip() + '\n'

    @property
    def corresponding_filename(self) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return Syntax.transliterate(self.given_title) + '.md'

    @property
    def content(self) -> str:
        """Вернуть скомпонованный текст документа.
        """
        if not self.template or not self.files:
            return ''

        template = string.Template(self.template)
        head = template.safe_substitute(dict(
            title=self.title
        ))

        lines = []
        for number, file in Syntax.numerate(sorted(self.files)):
            lines.append('{}. {}\n'.format(
                number,
                MarkdownParser.href(file.title, file.filename)
            ))

        lines.append('')
        body = '\n'.join(lines)

        return head + body


class MarkdownMetaDocument(MetaMixin, MarkdownDocument):
    """Метадокумент markdown.
    """

    @property
    def title(self) -> str:
        """Вернуть заголовок документа.
        """
        return f'## Все вхождения тега "{self.given_title}"'


class MarkdownIndexDocument(MarkdownDocument):
    """Markdown индекс (стартовый файл).
    """

    @property
    def title(self) -> str:
        """Вернуть заголовок документа.
        """
        return f'# Все записи'

    @property
    def corresponding_filename(self) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return 'index.md'


class HypertextDocument(AbstractDocument):
    """Базовый HTML документ.
    """
    BASE_TEMPLATE = """
    <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>$title</title>

            <script src="jquery-3.5.1.min.js" 
                type="application/javascript"></script>
            <script src="arbor.js" 
                type="application/javascript"></script>
            <script src="rendering.js" 
                type="application/javascript"></script>

            <style type="text/css">
                html, body {
                    margin: 0;
                    padding: 0;
                    background-color: gray;
                    overflow: hidden;
                }
            </style>

        </head>
        <body>
            <canvas id="viewport" width="1000" height="1000"></canvas>
            <script type="application/javascript">
                let main_data_block = $nodes;
            </script>
        </body>
    </html>
    """

    @property
    def corresponding_filename(self) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return Syntax.transliterate(self.given_title) + '.html'


class HupertextMetaDocument(MetaMixin, HypertextDocument):
    """Метадокумент HTML.
    """


class HypertextIndexDocument(HypertextDocument):
    """HTML индекс (стартовый файл).
    """

    @property
    def corresponding_filename(self) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return 'index.html'
