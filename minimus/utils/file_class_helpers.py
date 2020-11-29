# -*- coding: utf-8 -*-

"""Вспомогательные функции специально для класса файла.
"""
import bisect
from collections import defaultdict
from typing import List, Dict

from minimus import settings
from minimus.components.class_file import File
from minimus.components.class_slice import Slice
from minimus.utils.files_processing import write_text
from minimus.utils.markdown_processing import (
    extract_bare_tags, extract_full_tags,
)
from minimus.utils.output_processing import stdout
from minimus.utils.text_processing import numerate


def analyze_contents(files: List[File]) -> None:
    """Проанализаровать содержимое каждого из файлов.

    Мутирует состояние файлов.
    """
    for file in files:
        if not file.is_markdown():
            continue

        analyze_single_file(file)


def analyze_single_file(file: File) -> None:
    """Проанализаровать содержимое файла.

    Мутирует состояние файла.
    """
    slices = make_slices(file.original_content)

    string = file.original_content
    components = []
    position = 0

    for slice_ in slices:
        file.tags.add(slice_.inner_text)
        components.append(string[position:slice_.start_outer])
        components.append(slice_)
        position = slice_.end_outer

    components.append(string[position:])

    file.components = components


def make_slices(content: str) -> List[Slice]:
    """Собрать список нарезок по содержимому файла.

    Наредки вставляются упорядоченно согласно их месту в тексте.
    Перекрытие диапазонов не рассматривается.
    """
    slices = []

    for match in extract_bare_tags(content):
        bisect.insort_right(slices, Slice(match, full=False))

    for match in extract_full_tags(content):
        bisect.insort_right(slices, Slice(match, full=True))

    return slices


def map_tags_to_files(files: List[File]) -> Dict[str, List[File]]:
    """Собрать отображение тегов на файлы.

    Пример вывода:
    {
        '4 лапы':
            [
                File('2020-07-06_elephant.md'),
                File('2020-07-06_mouse.md')
            ],
        'серый':
            [
                File('2020-07-06_elephant.md'),
                File('2020-07-06_mouse.md')
            ],
    }
    """
    tags_to_files = defaultdict(list)

    for file in files:
        if file.is_markdown():
            for tag in file.tags:
                tags_to_files[tag].append(file)

    return {
        tag: files
        for tag, files in tags_to_files.items()
    }


def ensure_each_tag_has_metafile(tags_to_files: Dict[str, List[File]]) -> None:
    """Удостовериться, что для каждого тега есть персональная страничка.

    Вместо проверки правильности, она просто каждый раз создаётся заново.
    """
    for tag_number, (tag, tag_files) in numerate(tags_to_files.items()):
        stdout('\t{tag_number}. Tag name: "{tag}"',
               tag_number=tag_number, tag=tag)

        for file_number, file in numerate(tag_files):
            created = write_text(
                path=settings.TARGET_DIRECTORY,
                filename=file.filename,
                content=file.content,
            )

            stdout('\t\t{file_number}. File created: {filename}',
                   file_number=file_number, filename=created)
        stdout('')

# def create_meta_md(config: Config, tag: str, files: List[TextFile],
#                    prefix: str, num: int, total: int) -> None:
#     """Создать markdown метадокумент.
#     """
#     document = MarkdownMetaDocument(tag, files)
#     create_meta(config, document, prefix, num, total)
