# -*- coding: utf-8 -*-

"""Вспомогательные функции специально для класса файла.
"""
import bisect
import shutil
from collections import defaultdict
from typing import List, Dict, Generator

from colorama import Fore

from minimus import settings
from minimus.components import segment_types
from minimus.components.class_file import File
from minimus.components.class_repository import Repository
from minimus.utils import markdown_processing
from minimus.utils.files_processing import write_text
from minimus.utils.filesystem import join, find_shortest_common_path
from minimus.utils.output_processing import stdout, transliterate, translate
from minimus.utils import spans_processing
from minimus.utils.text_processing import numerate

__all__ = [
    'analyze_files',
    'analyze_single_file',
    'map_tags_to_files',
    'ensure_each_tag_has_metafile',
    'create_metafile',
    'ensure_index_exists',
    'ensure_readme_exists',
    'create_index',
    'save_main_files',
    'save_additional_files',
]


def analyze_files(repository: Repository) -> None:
    """Проанализаровать содержимое каждого из файлов.

    Мутирует состояние файлов.
    """
    for file in repository:
        if file.is_markdown:
            analyze_single_file(file)


def analyze_single_file(file: File) -> None:
    """Проанализаровать содержимое файла.

    Мутирует состояние файла.
    """
    segments = []
    content = file.renderer.original_content

    for segment in segment_types.BareTag.from_string(content):
        file.renderer.add_tag(segment.inner_text)
        bisect.insort_right(segments, segment)

    for segment in segment_types.MarkdownUrl.from_string(content):
        bisect.insort_right(segments, segment)

    # на этом этапе надо добавить в сегменты простые текстовые куски файла
    spans = spans_processing.make_spans_for_segments(segments)
    inverted_spans = spans_processing.make_inverted_spans(spans, len(content))

    for span in inverted_spans:
        segment = segment_types.TextSegment(
            start_outer=span.start,
            content=content[span.start:span.stop],
        )
        bisect.insort_right(segments, segment)

    file.renderer.segments = segments


def map_tags_to_files(repository: Repository) -> Dict[str, List[File]]:
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

    for file in repository:
        if file.is_markdown:
            for tag in file.renderer.get_tags():
                tags_to_files[tag].append(file)

    return dict(tags_to_files)


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
        stdout('\t{number}. File created: {filename}',
               number=tag_number, filename=created, color=Fore.YELLOW)


def create_metafile(tag: str, files: List[File]) -> str:
    """Собрать содержимое метафайла.
    """
    content = [
        translate(
            template='## All occurrences of the tag "{tag}"',
            language=settings.LANGUAGE,
        ).format(tag=tag),
        '\n---\n'
    ]

    raw_pairs = []

    for file in files:
        raw_pairs.append((file.renderer.title, file.meta.filename))

    raw_pairs.sort()

    for number, (text, url) in numerate(raw_pairs):
        content.append(f'{number}. {markdown_processing.href(text, url)}\n')

    return '\n'.join(content)


def ensure_index_exists(repository: Repository) -> None:
    """Удостовериться, что у нас есть стартовая страница.
    """
    if not repository:
        return

    content = create_index(repository, './')
    created = write_text(
        path=settings.TARGET_DIRECTORY,
        filename='index.md',
        content=content,
    )

    stdout('\tFile created: {filename}', filename=created, color=Fore.YELLOW)


def ensure_readme_exists(repository: Repository) -> None:
    """Удостовериться, что у нас есть стартовая страница.
    """
    if not repository:
        return

    base_folder = find_shortest_common_path(
        current_directory=settings.README_DIRECTORY,
        target_directory=settings.TARGET_DIRECTORY,
    )

    content = create_index(repository, base_folder)
    created = write_text(
        path=settings.README_DIRECTORY,
        filename='README.md',
        content=content,
    )

    stdout('\tFile created: {filename}', filename=created, color=Fore.YELLOW)


def get_all_categories(repository: Repository) -> Generator[str, None, None]:
    """Извлечь все категории всех файлов.
    """
    for file in repository:
        if file.is_markdown and file.renderer.category:
            yield file.renderer.category


def create_index(repository: Repository, base_folder: str) -> str:
    """Собрать содержимое старотового файла.
    """
    content = [
        translate(
            template='# All entries',
            language=settings.LANGUAGE,
        ),
        '\n---\n'
    ]

    categories = sorted(get_all_categories(repository))
    by_category = defaultdict(list)

    for file in repository:
        if file.is_markdown and file.renderer.category:
            by_category[file.renderer.category].append(file)

    for number, category in numerate(categories):
        meta_url = markdown_processing.href(
            label=category.title(),
            link='meta_' + transliterate(category) + '.md',
            base_folder=base_folder,
        )
        content.append(f'{number}. {meta_url}\n')

        for each_file in by_category[category]:
            url = markdown_processing.href(
                label=each_file.renderer.title,
                link=each_file.meta.filename,
                base_folder=base_folder,
            )
            content.append(f'* {url}\n')

        content.append('')

    return '\n'.join(content)


def save_main_files(repository: Repository) -> None:
    """Сохранить файлы маркдаун в целевой каталог.
    """
    files = [x for x in repository if not x.is_metafile and x.is_markdown]

    for number, file in numerate(files):
        filename = file.meta.filename

        if file.is_updated:
            write_text(
                path=settings.TARGET_DIRECTORY,
                filename=filename,
                content=file.renderer.content,
            )
            stdout('\t{number}. Saved changes: {filename}',
                   number=number, filename=filename, color=Fore.YELLOW)
        else:
            stdout('\t{number}. No changes detected: {filename}',
                   number=number, filename=filename)


def save_additional_files(repository: Repository) -> None:
    """Сохранить файлы с медиа контентом в целевой каталог.
    """
    files = [x for x in repository if not x.is_metafile and not x.is_markdown]

    for number, file in numerate(files):
        filename = file.meta.filename

        if file.is_updated:
            source = join(file.meta.original_path, file.meta.original_filename)
            target = join(settings.TARGET_DIRECTORY, filename)
            shutil.copy(source, target)
            stdout('\t{number}. Copied file: {filename}',
                   number=number, filename=filename, color=Fore.YELLOW)
        else:
            stdout('\t{number}. No changes detected: {filename}',
                   number=number, filename=filename)

    if not files:
        stdout('\tNo files to save')
