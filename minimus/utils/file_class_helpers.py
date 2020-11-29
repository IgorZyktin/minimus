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
    extract_bare_tags, extract_full_tags, href,
)
from minimus.utils.output_processing import stdout, transliterate, translate
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
        file.add_tag(slice_.inner_text)
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
            for tag in file.get_tags():
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
        filename = 'meta_{name}.md'.format(name=transliterate(tag))
        content = create_metafile(tag, tag_files)

        created = write_text(
            path=settings.TARGET_DIRECTORY,
            filename=filename,
            content=content,
        )
        stdout('\t{tag_number}. File created: {filename}',
               tag_number=tag_number, filename=created)


def create_metafile(tag: str, files: List[File]) -> str:
    """Собрать содержимое метафайла.
    """
    content = [
        translate(
            template='## All occurrences of the tag "{tag}"\n\n',
            lang=settings.LANGUAGE,
        ).format(tag=tag)
    ]

    raw_pairs = []

    for file in files:
        text = file.title
        raw_pairs.append((text, file.filename))

    raw_pairs.sort()

    for number, (text, url) in numerate(raw_pairs):
        content.append(f'{number}. {href(text, url)}\n')

    return '\n'.join(content)


def ensure_index_exists(files: List[File]) -> None:
    """Удостовериться, что у нас есть стартовая страница.
    """
    if not files:
        return

    content = create_index(files)
    created = write_text(
        path=settings.TARGET_DIRECTORY,
        filename='index.md',
        content=content,
    )

    stdout(
        '\tFile created: {filename}',
        filename=created,
    )


def create_index(files: List[File]) -> str:
    """Собрать содержимое старотового файла.
    """
    content = [
        translate(
            template='# All entries"\n\n',
            lang=settings.LANGUAGE,
        )
    ]

    categories = sorted({
        x.category for x in files
        if x.category is not None
    })

    unfixed_files = files.copy()
    by_cat = defaultdict(list)

    for file in unfixed_files:
        by_cat[file.category].append(file)

    for number, category in numerate(categories):
        content.append(f'{number}. {category.title()}\n')
        for each_file in by_cat[category]:
            content.append(f'* {href(each_file.title, each_file.filename)}\n')

    return '\n'.join(content)
