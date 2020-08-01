# -*- coding: utf-8 -*-

"""Набор классов для HTML документов.
"""
import string
from abc import abstractmethod
from typing import List, Optional

from minimus.abstract import AbstractDocument, AbstractTextFile
from minimus.config import Config
from minimus.documents_markdown import MarkdownMetaDocument
from minimus.graph import Graph
from minimus.syntax import Syntax


class HypertextDocument(AbstractDocument):
    """Базовый HTML документ.
    """

    def __init__(self, config: Config, title: str,
                 files: List[AbstractTextFile],
                 template: Optional[str] = None):
        """Инициализировать экземпляр.
        """
        self.config = config
        super().__init__(title, files, template)

        if template is None:
            self.given_template = config.html_template

    @classmethod
    def make_corresponding_filename(cls, title: str) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return '{name}.html'.format(name=Syntax.transliterate(title))

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
            'title': self.title,
            'nodes': Syntax.to_json(self.render_graph(self.files)),
        })
        return content

    @abstractmethod
    def render_graph(self, files: List[AbstractTextFile]) -> dict:
        """Базовый HTML документ не умеет в графы.
        """
        return {}


class HypertextMetaDocument(HypertextDocument):
    """Метадокумент HTML.
    """

    def render_graph(self, files: List[AbstractTextFile]) -> dict:
        """Граф для метафайла (простой).
        """
        graph = Graph()

        graph.add_node(
            name='tag',
            label=self.title,
            bg_color=self.config.bg_color_tag,
            link=self.make_link(self.corresponding_filename),
            filename=self.corresponding_filename,
        )

        for i, file in enumerate(files, start=1):
            key = Syntax.transliterate(file.title)
            filename = MarkdownMetaDocument\
                .make_corresponding_filename(self.title)
            graph.add_node(
                name=key,
                label=file.title,
                bg_color=self.config.bg_color_node,
                link=self.make_link(filename)
            )
            graph.add_edge('tag', key)

        return graph.as_dict()

    @classmethod
    def make_corresponding_filename(cls, title: str) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return 'meta_{name}.html'.format(name=Syntax.transliterate(title))


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
                name=base_key,
                label=file.title,
                bg_color=self.config.bg_color_node,
                link=self.make_link(file.filename),
                filename=file.filename,
            )

            for tag in file.tags:
                key = Syntax.transliterate(tag)
                filename = MarkdownMetaDocument\
                    .make_corresponding_filename(tag)

                graph.add_node(
                    name=key,
                    label=tag,
                    bg_color=self.config.bg_color_tag,
                    link=self.make_link(filename),
                    filename=filename,
                )
                graph.add_edge(base_key, key)

        return graph.as_dict()
