# -*- coding: utf-8 -*-

"""Основной рабочий код приложения.
"""
from collections import defaultdict
from typing import List, Dict

from minimus.abstract import AbstractDocument
from minimus.config import Config
from minimus.documents_html import (
    HypertextMetaDocument, HypertextIndexDocument,
)
from minimus.documents_markdown import (
    MarkdownMetaDocument, MarkdownIndexDocument,
)
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
                                 tags_to_files: Dict[str, List[TextFile]],
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
        if config.render_html:
            create_meta_html(config, tag, tag_files, prefix, i, total)
            i += 1


def create_meta_md(config: Config, tag: str, files: List[TextFile],
                   prefix: str, num: int, total: int) -> None:
    """Создать markdown метадокумент.
    """
    document = MarkdownMetaDocument(tag, files)
    create_meta(config, document, prefix, num, total)


def create_meta_html(config: Config, tag: str, files: List[TextFile],
                     prefix: str, num: int, total: int) -> None:
    """Создать html метадокумент.
    """
    document = HypertextMetaDocument(config, tag, files)
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


def ensure_each_tag_has_link(files: List['TextFile']) -> None:
    """Удостовериться, что каждый тег является ссылкой, а не текстом.
    """
    update_required = []

    for file in files:
        existing_content = file.content
        new_content = MarkdownParser.replace_tags_with_hrefs(
            content=existing_content,
            tags=file.tags,
            maker=MarkdownMetaDocument,
        )

        if new_content != existing_content:
            file.content = new_content
            update_required.append(file)

    for number, file in Syntax.numerate(update_required):
        Syntax.stdout('\t{number}. File has been updated: {filename}',
                      number=number, filename=file.filename)


def ensure_index_exists(config: Config, files: List[TextFile]) -> None:
    """Удостовериться, что у нас есть стартовая страница.
    """
    if not files:
        return

    def make_index(some_index):
        filename = config.target_directory / some_index.corresponding_filename
        if FileSystem.write(filename, some_index.content):
            Syntax.stdout('\tNew file has been created: {filename}',
                          filename=filename.absolute())

    index = MarkdownIndexDocument('', files)
    make_index(index)

    if config.render_html:
        index = HypertextIndexDocument(config, '', files)
        make_index(index)
