"""Модуль по работе с файловой системой.
"""
import json
import os
import sys
from pathlib import Path

from minimus import constants
from minimus import objects


def get_path() -> Path:
    """Верни корневой каталог, в котором хранятся заметки."""
    match sys.argv:
        case [_]:
            raw_path = '.'
        case [_, raw_path]:
            pass
        case _:
            msg = 'Для запуска Minimus требуется указать корневой каталог'
            raise ValueError(msg)

    match raw_path:
        case '.':
            path = Path(os.getcwd())
        case _:
            path = Path(raw_path)

    if not path.exists():
        msg = f'Указанный путь не существует: {path.absolute()!r}'
        raise FileNotFoundError(msg)

    if not path.is_dir():
        msg = f'Указанный путь это файл, а не каталог: {path.absolute()!r}'
        raise FileNotFoundError(msg)

    return path


def get_cache(path: Path) -> dict:
    """Загрузить данные об уже обработанных файлах."""
    full_path = path / constants.CACHE_FILENAME

    try:
        with open(full_path, mode='r', encoding='utf-8') as file:
            cache = json.load(file)
    except FileNotFoundError:
        cache = {}

    return cache


def save_readme(path: Path, readme: str) -> Path:
    """Сохранить README.md."""
    full_path = path / constants.README_FILENAME

    with open(full_path, mode='w', encoding='utf-8') as file:
        file.write(readme)

    return full_path


def save_cache(path: Path, cache: dict) -> Path:
    """Сохранить данные об уже обработанных файлах."""
    full_path = path / constants.CACHE_FILENAME

    with open(full_path, mode='w', encoding='utf-8') as file:
        json.dump(cache, file, ensure_ascii=False, indent=4)

    return full_path


def get_files(path: Path) -> list[objects.File]:
    """Собрать файлы."""
    files = []
    _recursively_dig(path, path, files)
    return files


def _recursively_dig(
        root: Path,
        path: Path,
        files: list[objects.File],
) -> None:
    """Рекурсивно собрать данные по всем файлам в каталоге."""
    entries: list[str] = os.listdir(path)

    for name in entries:
        sub_path = path / name

        if sub_path.is_file():
            if can_handle_this(name):
                new_file = objects.File(root, sub_path)
                files.append(new_file)
        else:
            if name != constants.TAGS_FOLDER:
                _recursively_dig(root, sub_path, files)


def can_handle_this(name: str) -> bool:
    """Вернуть True если мы умеем обрабатывать такие файлы."""
    if name.lower().startswith(constants.IGNORED_PREFIXES):
        return False

    if not name.lower().endswith(constants.SUPPORTED_EXTENSIONS):
        return False

    if name == constants.README_FILENAME:
        return False

    return True


def ensure_folder_for_tags(path: Path) -> None:
    """Создать каталог для тегов, если такового нет."""
    (path / constants.TAGS_FOLDER).mkdir(exist_ok=True)


def save_tag(path: Path, filename: str, content: str) -> Path:
    """Сохранить документ для тега."""
    full_path = path / constants.TAGS_FOLDER / filename

    with open(full_path, mode='w', encoding='utf-8') as file:
        file.write(content)

    return full_path
