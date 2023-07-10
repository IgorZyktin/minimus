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


def make_tag_content(
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
            link=escape(f'../{file_path}'),
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
                link=escape(f'../{full_path}'),
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
    return f'[{title}]({link})'


def make_readme_content(files: list[objects.File]) -> str:
    """Собрать содержимое головного файла README."""
    lines = [f'# Всего записей: {len(files)} шт.\n']

    category: list[str] = []

    for file in files:
        folder = file.path.parent.relative_to(file.root)
        file_path = file.path.relative_to(file.root)

        parts = list(list(folder.parts))
        if category != parts:
            for part in parts:
                prefix = '\t' * len(category)
                lines.append(f'{prefix}- {part}\n')
                category.append(part)

        link = as_href(
            title=file.title,
            link=escape(f'./{file_path}'),
        )
        prefix = '\t' * len(category)
        lines.append(f'{prefix}- {link}\n')

    return '\n'.join(lines) + '\n'


def replace_bare_tags(file: objects.File) -> str:
    """Заменить теги на ссылки.

    Работает только для тех тегов, которые оформлены как простой текст.
    Есть риск, что replace очень медленный, но пока предполагаем,
    что файлы у нас не очень большие.
    """
    content = file.content
    already_replaced: set[str] = set()

    for tag in constants.BARE_TAG_PATTERN.finditer(file.content):
        prefix = tag.groups()[0]
        text = tag.groups()[1]
        suffix = tag.groups()[2]

        if text in already_replaced:
            continue

        text_before = prefix + text + suffix
        tag_filename = get_tag_filename(text)
        link = get_relative_path_for_tag(file.root, file.path, tag_filename)
        text_after = as_href(
            title=f'{{{{ {text} }}}}',
            link=link,
        )
        content = content.replace(text_before, text_after)
        already_replaced.add(text)

    return content


def get_relative_path_for_tag(
    root: Path,
    file_path: Path,
    tag_filename: str,
) -> str:
    """Вернуть относительный путь от файла до указанного тега."""
    from_root = file_path.parent.relative_to(root)
    hops = len(from_root.parts)

    path = f'{constants.TAGS_FOLDER}/{tag_filename}'

    if hops == 0:
        path = f'./{path}'

    else:
        for _ in range(hops):
            path = f'../{path}'

    return path
