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

__all__ = [
    'Graph',
    'TextFile',
    'Filesystem',
    'MarkdownSyntax',
    'HTMLSyntax',
    'map_tags_to_files',
]

from minimus.config import Config
from minimus.syntax import Syntax


class Graph:
    """Представление графа.
    """

    def __init__(self):
        """Инициализировать экземпляр.
        """
        self.nodes = {}
        self.edges = {}

    def add_node(self, name: str, label: str,
                 bg_color: str, link: str) -> None:
        """Добавить ноду в граф.
        """
        self.nodes[name] = {
            'label': label,
            'bg_color': bg_color,
            'link': link,
        }

    def add_edge(self, node_start: str, node_finish: str,
                 weight: float = 0.1) -> None:
        """Добавить грань в граф.
        """
        if node_start not in self.edges:
            self.edges[node_start] = {}

        self.edges[node_start][node_finish] = {'weight': weight}

    def as_dict(self) -> dict:
        """Вернуть граф в форме словаря.
        """
        return {
            'nodes': self.nodes,
            'edges': self.edges,
        }


class HTMLSyntax:
    """Мастер по работе с форматом HTML.
    """

    @staticmethod
    def get_index_filename() -> str:
        """Вернуть название файла индекса.
        """
        return 'index.html'

    # @classmethod
    # def get_tag_filename(cls, tag: str) -> str:
    #     """Вернуть соответствующее тегу имя файла.
    #
    #     >>> HTMLSyntax.get_tag_filename('планирование')
    #     'meta_planirovanie.html'
    #     """
    #     return 'meta_' + Syntax.transliterate(tag) + '.html'

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
                link=cls.make_link(file.filename)
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
                link=cls.make_link(file.filename)
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


class MarkdownSyntax:
    """Мастер по работе с форматом MarkDown.

    TITLE_PATTERN - шаблон заголовка
        Произвольное количество пробелов от начала строки, за которыми следуют
        один или несколько октоторпов. Потом идёт обязательный пробел (одно из
        отличий заголовка от тега), за которым произвольный набор символов
        до конца строки.

    HEAD_BARE_TAG_PATTERN - шаблон голого тега из заголовка статьи.
        Это тег, который ещё не был отформатирован пользователем.
        Строго с начала строки, затем экранированный октоторп и
        сразу текст без пробела, считываемый до конца строки.

    BODY_BARE_TAG_PATTERN - неотформатированный тег, но уже в теле документа.
        Мы заведомо не знаем, где кончается текст тега, так что этот
        шаблон надо по месту достравивать для каждого тега.

    FULL_TAG_PATTERN - отформатированный тег в теле документа.
        Он уже оформлен в виде гиперссылки.
    """

    @classmethod
    def make_metafile_contents(cls, tag: str, files: List['TextFile']) -> str:
        """Собрать текст метафайла из исходных данных.
        """
        return cls.render_text(f'## Все вхождения тега "{tag}"', files)

    @classmethod
    def make_index_contents(cls, files: List['TextFile']) -> str:
        """Собрать текст стартовой страницы из исходных данных.
        """
        return cls.render_text('# Все записи', files)







