# -*- coding: utf-8 -*-

"""Вспомогательные функции специально для класса файла.
"""
import bisect
import shutil
from collections import defaultdict
from typing import List, Dict, Generator, Tuple, Set

from colorama import Fore

from minimus import settings
from minimus.components import segment_types
from minimus.components.class_file import File
from minimus.components.class_repository import Repository
from minimus.utils import markdown_processing, spans_processing
from minimus.utils.files_processing import write_text
from minimus.utils.filesystem import join, find_shortest_common_path
from minimus.utils.output_processing import stdout, transliterate, translate
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


def title_sorter(file: File) -> str:
    """Функция для сортировки по заголовку.
    """
    return file.renderer.title


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


def map_tags_to_files(repository: Repository) \
        -> Tuple[Dict[str, List[File]], Dict[str, Set[str]]]:
    """Собрать отображение тегов на файлы.

    Пример связи тега с файлами:
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

    Пример связи тегов с тегами:
    {
        'хобот': {'серый', '4 лапы', 'хобот', 'машина'},
        '4 лапы': {'хвост', 'серый', '4 лапы', 'хобот'},
        'серый': {'хвост', 'серый', '4 лапы', 'хобот'},
        'хвост': {'хвост', 'серый', '4 лапы'},
        'машина': {'машина', 'хобот'}
    }
    """
    tags_to_files = defaultdict(list)
    associated_tags = defaultdict(set)

    for file in repository:
        if file.is_markdown:
            all_tags_in_file = file.renderer.get_tags()
            for tag in all_tags_in_file:
                tags_to_files[tag].append(file)
                associated_tags[tag].update(all_tags_in_file)

    return dict(tags_to_files), dict(associated_tags)


def ensure_each_tag_has_metafile(tags_to_files: Dict[str, List[File]],
                                 associated_tags: Dict[str, Set[str]]) -> None:
    """Удостовериться, что для каждого тега есть персональная страничка.

    Вместо проверки правильности, она просто каждый раз создаётся заново.
    """
    for tag_number, (tag, tag_files) in numerate(tags_to_files.items()):
        filename = 'meta_{name}.md'.format(name=transliterate(tag))
        content = create_metafile(tag, tag_files, associated_tags)

        created = write_text(
            path=settings.TARGET_DIRECTORY,
            filename=filename,
            content=content,
        )
        stdout('\t{number}. File created: {filename}',
               number=tag_number, filename=created, color=Fore.YELLOW)


def create_metafile(tag: str, files: List[File],
                    associated_tags: Dict[str, Set[str]]) -> str:
    """Собрать содержимое метафайла.
    """
    content = [
        translate(
            template='## All occurrences of the tag "{tag}"',
            language=settings.LANGUAGE,
        ).format(tag=tag),
        ''
    ]

    raw_pairs = []

    for file in files:
        raw_pairs.append((file.renderer.title, file.meta.filename))

    raw_pairs.sort()

    for number, (text, url) in numerate(raw_pairs):
        href = markdown_processing.href(text, url)
        content.append(f'{number}. {href}\n')

    close_tags = {x for x in associated_tags.get(tag, set()) if x != tag}

    if close_tags:
        content.append('---\n')
        content.append(translate(
            template='### This tag occurs with',
            language=settings.LANGUAGE,

        ))
        content.append('')

        for number, associated_tag in numerate(sorted(close_tags)):
            url = 'meta_' + transliterate(associated_tag) + '.md'
            href = markdown_processing.href(associated_tag, url)
            content.append(f'{number}. {href}\n')

    content.append('')

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

    if not base_folder.endswith('/') or not base_folder.endswith('\\'):
        base_folder += '/'

    base_folder = base_folder.replace('\\', '/')

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
    already_sent = set()

    for file in repository:
        if file.is_markdown and file.renderer.category:
            if file.renderer.category not in already_sent:
                yield file.renderer.category
                already_sent.add(file.renderer.category)


def create_index(repository: Repository, base_folder: str) -> str:
    """Собрать содержимое старотового файла.
    """
    content = [
        translate(
            template='# All entries',
            language=settings.LANGUAGE,
        ),
        ''
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

        for each_file in sorted(by_category[category], key=title_sorter):
            url = markdown_processing.href(
                label=each_file.renderer.title,
                link=each_file.meta.filename,
                base_folder=base_folder,
            )
            content.append(f'* {url}\n')

        content.append('')

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
