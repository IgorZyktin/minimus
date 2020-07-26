# -*- coding: utf-8 -*-

"""Автоматический линковщик для заметок.

Выполняет следующие функции:
    1. Порождает метадокументы для тегов. Странички, на которых можно
    посмотреть, где ещё используется этот тег.
    2. Модифицирует вхождения тегов в документ,
    заменяя их ссылками на соответствующие метастраницы тегов.
"""
import string
from typing import (
    List, Optional
)

from minimus.config import Config
from minimus.graph import Graph
from minimus.syntax import Syntax


class HTMLSyntax:
    """Мастер по работе с форматом HTML.
    """

    @staticmethod
    def get_index_filename() -> str:
        """Вернуть название файла индекса.
        """
        return 'index.html'

    @staticmethod
    def get_local_dir() -> str:
        """Выдать локальную папку в читаемом для html формате.
        """
        return str(Config.target_directory.absolute()).replace('\\', '/')

    @classmethod
    def make_link(cls, text: str, protocol: Optional[str] = None) -> str:
        """Собрать ссылку для графа.
        """
        protocol = protocol or Config.protocol
        directory = cls.get_local_dir()
        return protocol + directory + '/' + text

    @classmethod
    def render_tag_graph(cls, tag: str, files: List['TextFile']) -> dict:
        """Собрать граф для отображения тега.
        """
        graph = Graph()

        graph.add_node(
            'tag', tag, Config.bg_color_tag,
            link=cls.make_link(MarkdownSyntax.get_tag_filename(tag))
        )

        for i, file in enumerate(files, start=1):
            key = Syntax.transliterate(file.title)
            graph.add_node(
                key, file.title, Config.bg_color_node,
                link=cls.make_link(file.corresponding_filename)
            )
            graph.add_edge('tag', key)

        return graph.as_dict()

    @classmethod
    def render_index_graph(cls, files: List['TextFile']) -> dict:
        """Собрать граф для отображения стартовой страницы.
        """
        graph = Graph()

        for file in files:
            base_key = Syntax.transliterate(file.title)
            graph.add_node(
                base_key, file.title, Config.bg_color_node,
                link=cls.make_link(file.corresponding_filename)
            )

            for tag in file.tags:
                key = Syntax.transliterate(tag)
                graph.add_node(
                    key, tag, Config.bg_color_tag,
                    link=cls.make_link(MarkdownSyntax.get_tag_filename(tag))
                )
                graph.add_edge(base_key, key)

        return graph.as_dict()

    @classmethod
    def make_metafile_contents(cls, tag: str,
                               files: List['TextFile']) -> str:
        """Собрать текст метафайла из исходных данных.
        """
        template = string.Template(Config.HTML_TEMPLATE)
        content = template.safe_substitute({
            'title': tag,
            'nodes': Syntax.to_json(cls.render_tag_graph(tag, files))
        })
        return content

    @classmethod
    def make_index_contents(cls, files: List['TextFile']) -> str:
        """Собрать текст стартовой страницы из исходных данных.
        """
        template = string.Template(Config.HTML_TEMPLATE)
        content = template.safe_substitute({
            'title': 'Стартовая страница',
            'nodes': Syntax.to_json(cls.render_index_graph(files))
        })
        return content

