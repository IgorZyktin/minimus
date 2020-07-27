# -*- coding: utf-8 -*-

"""Набор классов для документов.

Документы в проекте это просто контейнеры для текста.
Они не умеют работать непосредственно с файловой системой.
"""
import string
from typing import List, Optional

from minimus.abstract import AbstractDocument, MetaMixin, AbstractTextFile
from minimus.config import Config
from minimus.graph import Graph
from minimus.markdown_parser import MarkdownParser
from minimus.syntax import Syntax


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
        return Syntax.transliterate(title) + '.md'

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

    def __init__(self, config: Config, title: str,
                 files: List[AbstractTextFile],
                 template: Optional[str] = None):
        """Инициализировать экземпляр.
        """
        self.config = config
        super().__init__(title, files, template)

    @classmethod
    def make_corresponding_filename(cls, title: str) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return Syntax.transliterate(title) + '.html'

    def get_local_dir(self) -> str:
        """Выдать локальную папку в читаемом для html формате.
        """
        return str(self.config.target_directory.absolute()).replace('\\', '/')

    def make_link(self, text: str, protocol: Optional[str] = None) -> str:
        """Собрать ссылку для графа.
        """
        protocol = protocol or self.config.protocol
        directory = self.get_local_dir()
        return protocol + directory + '/' + text

    @property
    def content(self) -> str:
        """Вернуть скомпонованный текст документа.
        """
        template = string.Template(self.template)
        content = template.safe_substitute({
            'title': 'Стартовая страница',
            'nodes': Syntax.to_json(self.render_graph(self.files))
        })
        return content

    # noinspection PyMethodMayBeStatic
    def render_graph(self, files: List[AbstractTextFile]) -> dict:
        """Базовый HTML документ не умеет в графы.
        """
        return {}


class HypertextMetaDocument(MetaMixin, HypertextDocument):
    """Метадокумент HTML.
    """

    def render_graph(self, files: List[AbstractTextFile]) -> dict:
        """Граф для метафайла (простой).
        """
        return {}


class HypertextIndexDocument(HypertextDocument):
    """HTML индекс (стартовый файл).
    """

    @property
    def title(self) -> str:
        """Вернуть заголовок документа.
        """
        return 'Стартовая страница'

    @property
    def corresponding_filename(self) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return 'index.html'

    def render_graph(self, files: List[AbstractTextFile]) -> dict:
        """Граф для индекса (сложный).
        """
        graph = Graph()

        for file in files:
            base_key = Syntax.transliterate(file.title)
            graph.add_node(
                base_key, file.title, self.config.bg_color_node,
                link=self.make_link(file.filename)
            )

            for tag in file.tags:
                key = Syntax.transliterate(tag)
                graph.add_node(
                    key, tag, self.config.bg_color_tag,
                    link=self.make_link(
                        MarkdownDocument.make_corresponding_filename(tag))
                )
                graph.add_edge(base_key, key)

        return graph.as_dict()
