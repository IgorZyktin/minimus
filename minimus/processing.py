# -*- coding: utf-8 -*-

"""Основной рабочий код приложения.
"""
from collections import defaultdict
from typing import List, Dict

from minimus.abstract import AbstractDocument
from minimus.config import Config
from minimus.documents import MarkdownMetaDocument, HupertextMetaDocument
from minimus.file_system import FileSystem
from minimus.markdown_parser import MarkdownParser
from minimus.syntax import Syntax
from minimus.text_file import TextFile


def map_tags_to_files(files: List[TextFile]) -> Dict[str, List[TextFile]]:
    """Собрать отображение тегов на файлы.

    Пример вывода:
    {
        '4 лапы':
            [
                TextFile('2020-07-06_elephant.md'),
                TextFile('2020-07-06_mouse.md')
            ],
        'серый':
            [
                TextFile('2020-07-06_elephant.md'),
                TextFile('2020-07-06_mouse.md')
            ],
    }

    """
    tags_to_files = defaultdict(list)

    for file in files:
        file.title = MarkdownParser.extract_title(file.content)
        file.tags = MarkdownParser.extract_tags(file.content)

        for tag in file.tags:
            tags_to_files[tag].append(file)

    return {
        tag: sorted(files)
        for tag, files in tags_to_files.items()
    }


def ensure_each_tag_has_metafile(config: Config,
                                 tags_to_files: Dict[str, List[TextFile]]
                                 ) -> None:
    """Удостовериться, что для каждого тега есть персональная страничка.

    Вместо проверки правильности, она просто каждый раз создаётся заново.
    """
    total = len(tags_to_files) * 2
    prefix = Syntax.make_prefix(total)

    i = 1
    for tag, tag_files in tags_to_files.items():
        # markdown форма
        create_meta_md(config, tag, tag_files, prefix, i, total)
        i += 1

        # html форма
        create_meta_html(config, tag, tag_files, prefix, i, total)
        i += 1


def create_meta_md(config: Config, tag: str, files: List[TextFile],
                   prefix: str, num: int, total: int) -> None:
    """Создать markdown метадокумент.
    """
    document = MarkdownMetaDocument(tag, files)
    create_meta(config, document, prefix, num, total)


def create_meta(config: Config, document: AbstractDocument,
                prefix: str, num: int, total: int) -> None:
    """Создать метадокумент.
    """
    filename = config.target_directory / document.corresponding_filename
    FileSystem.write(filename, document.content)

    number = prefix.format(num=num, total=total)
    Syntax.stdout('\t{number}. File created: {filename}',
                  number=number, filename=filename.absolute())


# def ensure_each_tag_has_link(files: List['TextFile']) -> None:
#     """Удостовериться, что каждый тег является ссылкой, а не текстом.
#     """
#     for file in files:
#         existing_contents = file.contents
#         new_contents = MarkdownSyntax.replace_tags_with_hrefs(
#             content=existing_contents,
#             tags=file.tags
#         )
#
#         if new_contents != existing_contents:
#             file.contents = new_contents


# def ensure_index_exists(files: List[TextFile]) -> None:
#     """Удостовериться, что у нас есть стартовая страница.
#     """
#     if not files:
#         return
#
#     # markdown форма
#     name = Config.target_directory / MarkdownSyntax.get_index_filename()
#     contents = MarkdownSyntax.make_index_contents(files)
#     if Filesystem.write(name, contents):
#         Syntax.announce(f'\tСоздан файл "{name.absolute()}"')
#
#     # html форма
#     name = Config.target_directory / HTMLSyntax.get_index_filename()
#     contents = HTMLSyntax.make_index_contents(files)
#     if Filesystem.write(name, contents):
#         Syntax.announce(f'\tСоздан файл "{name.absolute()}"')


def create_meta_html(config: Config, tag: str, files: List[TextFile],
                     prefix: str, num: int, total: int) -> None:
    """Создать html метадокумент.
    """
    document = HupertextMetaDocument(tag, files)
    create_meta(config, document, prefix, num, total)
