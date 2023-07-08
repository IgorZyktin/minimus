"""Модуль обработки текста.
"""
from collections import defaultdict
from pathlib import Path

from minimus.src import constants
from minimus.src import objects
from minimus.src import utils


def get_tag_filename(text: str) -> str:
    """Вернуть имя файла для тега."""
    return utils.transliterate(text) + '.md'


def gather_tags_from_files(
        files: list[objects.File],
) -> tuple[
    dict[str, set[objects.File]],
    dict[str, set[str]],
]:
    """Собрать словарь из соответствия тег-файлы."""
    found_tags: dict[str, set[objects.File]] = defaultdict(set)
    neighbours: dict[str, set[str]] = defaultdict(set)

    for file in files:
        for tag in file.tags:
            found_tags[tag].add(file)
            neighbours[tag].update(x for x in file.tags if x != tag)

    return found_tags, neighbours


def render_tag(
        tag: str,
        files: list[objects.File],
        neighbours: dict[str, set[str]],
) -> str:
    """Собрать документ для описания тега."""
    lines = [
        f'# {tag}\n',
        f'### Встречается в:\n',
    ]

    for number, file in utils.numerate(files):
        file_path = file.path.relative_to(file.root)
        link = as_href(
            title=file.title,
            link=escape(str(file_path)),
        )
        lines.append(f'{number}. {link}\n')

    close_tags = neighbours.get(tag)

    if close_tags:
        lines.append('\n### Близкие теги:\n')
        sorted_close_tags = sorted(close_tags)

        for number, tag in utils.numerate(sorted_close_tags):
            filename = get_tag_filename(tag)
            full_path = Path(constants.TAGS_FOLDER) / filename
            link = as_href(
                title=tag,
                link=escape(str(full_path)),
            )
            lines.append(f'{number}. {link}\n')

    return '\n'.join(lines) + '\n'


def escape(link: str) -> str:
    """Заменить спецсимволы для гиперссылки."""
    return link.replace(' ', '%20').replace('+', '%2B')


def as_filename(title: str) -> str:
    """Сгенерировать имя файла."""
    return f'{title}.md'


def as_href(title: str, link: str) -> str:
    """Сгенерировать гиперссылку."""
    return f'[{title}](../{link})'


def make_readme(files: list[objects.File]) -> str:
    """Собрать содержимое головного файла README."""
    lines = [f'# Всего записей: {len(files)} шт.\n']

    for number, file in utils.numerate(files):
        path = file.path.relative_to(file.root.parent)
        link = as_href(
            title=file.title,
            link=escape(str(path)),
        )
        lines.append(f'{number}. {link}\n')

    return '\n'.join(lines) + '\n'
