"""Модуль по работе с файловой системой.
"""
import json
import os
import sys
from pathlib import Path
from typing import Iterator

from minimus import objects

README_FILENAME = 'README.md'
CACHE_FILENAME = '.minimus_cache.json'
IGNORED_PREFIXES = ('~', '.', '_')
SUPPORTED_EXTENSIONS = ('.md',)


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
    full_path = path / CACHE_FILENAME

    try:
        with open(full_path, mode='r', encoding='utf-8') as file:
            cache = json.load(file)
    except FileNotFoundError:
        cache = {}

    return cache


def save_readme(path: Path, readme: str) -> Path:
    """Сохранить README.md."""
    full_path = path / README_FILENAME

    with open(full_path, mode='w', encoding='utf-8') as file:
        file.write(readme)

    return full_path


def save_cache(path: Path, cache: dict) -> Path:
    """Сохранить данные об уже обработанных файлах."""
    full_path = path / CACHE_FILENAME

    with open(full_path, mode='w', encoding='utf-8') as file:
        json.dump(cache, file, ensure_ascii=False, indent=4)

    return full_path


def get_files(path: Path) -> list[objects.File]:
    """Собрать файлы."""
    files = []
    _recursively_dig(path, files)
    return files


def _recursively_dig(path: Path, files: list[objects.File]) -> None:
    """Рекурсивно собрать данные по всем файлам в каталоге."""
    entries = os.listdir(path)

    for filename in get_normal_filenames(entries):
        sub_path = path / filename

        if sub_path.is_file():
            new_file = objects.File(path)
            files.append(new_file)
        else:
            _recursively_dig(sub_path, files)


def get_normal_filenames(entries: list[str]) -> Iterator[str]:
    """Вернуть только имена, подходящие для обработки."""
    for entry in entries:
        if entry.lower().startswith(IGNORED_PREFIXES):
            continue

        if not entry.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        yield entry


# def split_pointers(pointers: list[objects.Pointer]
#                    ) -> tuple[list[objects.Pointer], list[objects.Pointer]]:
#     """Разделить исходные файлы на текстовые заметки и всё остальное."""
#     notes = []
#     media = []
#
#     for pointer in pointers:
#         if pointer.filename.lower().endswith('md'):
#             notes.append(pointer)
#         else:
#             media.append(pointer)
#
#     return notes, media
#
#
# def copy_media(target: str, media: list[objects.Pointer],
#                cache: dict, force: bool) -> None:
#     """Скопировать медиа файлы при необходимости."""
#     for number, pointer in utils.numerate(media):
#         if is_changed(pointer, cache) or force:
#             print(Fore.YELLOW
#                   + f'\t{number}. Скопирован: {pointer.location}')
#             cache[pointer.location] = pointer.fingerprint
#             path = os.path.join(target, pointer.location)
#             shutil.copy(pointer.path, path)
#         else:
#             print(Fore.LIGHTWHITE_EX
#                   + f'\t{number}. Не менялся: {pointer.location_url}')
#
#
# def is_changed(pointer: objects.Pointer, cache: dict) -> bool:
#     """Вернуть True если файл поменялся."""
#     return cache.get(pointer.location) != pointer.fingerprint
#
#
# def load_text(notes: list[objects.Pointer]
#               ) -> list[tuple[objects.Pointer, str]]:
#     """Загрузить тело документов, но пока не обрабатывать."""
#     notes_with_text = []
#     for note in notes:
#         with open(note.path, mode='r', encoding='utf-8') as file:
#             text = file.read()
#             notes_with_text.append((note, text))
#
#     return notes_with_text
#
#
# def save_documents(target: str, documents: list[objects.Document],
#                    cache: dict, force: bool) -> None:
#     """Сохранить все документы."""
#     create_folder(os.path.join(target, 'content', '_tags'))
#
#     for number, document in utils.numerate(documents):
#         if is_changed(document.pointer, cache) or force:
#             print(Fore.YELLOW
#                   + f'\t{number}. Сохранён: {document.pointer.location_url}')
#             cache[document.pointer.location] = document.pointer.fingerprint
#
#             create_folder(os.path.join(target, *document.pointer.steps))
#             path = os.path.join(target, document.pointer.location)
#             with open(path, mode='w', encoding='utf-8') as file:
#                 file.write(document.rendered)
#         else:
#             print(
#                 Fore.LIGHTWHITE_EX
#                 + f'\t{number}. Не менялся: {document.pointer.location_url}'
#             )
#
#
# def save_tags(path: Path, tags: list[objects.Tag]) -> None:
#     """Сохранить документы для тегов."""
#     for tag in tags:
#         path = os.path.join(target, 'content', '_tags', tag.filename)
#         with open(path, mode='w', encoding='utf-8') as file:
#             file.write(tag.rendered)
#
#     print(f'\tСохранено {len(tags)} тегов')
