"""Модуль по работе с файловой системой.
"""

import os
import sys
from pathlib import Path

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


# def make_fingerprint(path: str) -> objects.Fingerprint:
#     """Получить слепок файла."""
#     try:
#         stat = os.stat(path)
#
#         with open(path, 'rb') as f:
#             file_hash = hashlib.md5()
#             while chunk := f.read(8192):
#                 file_hash.update(chunk)
#     except FileNotFoundError:
#         fingerprint = objects.Fingerprint(md5='',
#                                           created=-1,
#                                           modified=-1,
#                                           size=-1)
#     else:
#         fingerprint = objects.Fingerprint(md5=str(file_hash.hexdigest()),
#                                           created=int(stat.st_ctime),
#                                           modified=int(stat.st_mtime),
#                                           size=stat.st_size)
#     return fingerprint
#
#
# def gather_pointers(source: str) -> list[objects.Pointer]:
#     """Собрать указатели на файлы."""
#     pointers = []
#     _recursively_dig(source, pointers, steps=[])
#     return pointers
#
#
# def _recursively_dig(path: str, pointers: list[objects.Pointer],
#                      steps: list[str]) -> None:
#     """Рекурсивно собрать данные по всем файлам в каталоге."""
#     entries = os.listdir(path)
#
#     for entry in entries:
#         if entry.startswith('.'):
#             # .git попадает сюда
#             continue
#
#         sub_path = os.path.join(path, entry)
#         if os.path.isfile(sub_path):
#             new_pointer = objects.Pointer(
#                 path=sub_path,
#                 filename=entry,
#                 steps=tuple(steps),
#                 fingerprint=make_fingerprint(sub_path),
#             )
#             pointers.append(new_pointer)
#         else:
#             _recursively_dig(sub_path, pointers, steps + [entry])
#
#
# def gather_cache(source: str) -> dict:
#     """Загрузить данные об уже обработанных файлах."""
#     path = os.path.join(source, '~meta.json')
#     try:
#         with open(path, mode='r', encoding='utf-8') as file:
#             contents = json.load(file)
#     except FileNotFoundError:
#         contents = {}
#     return contents
#
#
# def save_cache(source: str, cache: dict) -> None:
#     """Сохранить данные об уже обработанных файлах."""
#     path = os.path.join(source, '~meta.json')
#     with open(path, mode='w', encoding='utf-8') as file:
#         json.dump(cache, file, ensure_ascii=False, indent=4)
#
#
# def skip_private_files(pointers: list[objects.Pointer]
#                        ) -> list[objects.Pointer]:
#     """Убрать файлы не предназначенные для обработки."""
#     return [
#         x for x in pointers
#         if not x.filename.startswith(('~', '_'))
#     ]
#
#
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
def save_tags(path: Path, tags: list[objects.Tag]) -> None:
    """Сохранить документы для тегов."""
#     for tag in tags:
#         path = os.path.join(target, 'content', '_tags', tag.filename)
#         with open(path, mode='w', encoding='utf-8') as file:
#             file.write(tag.rendered)
#
#     print(f'\tСохранено {len(tags)} тегов')


def save_readme(path: Path, readme: str) -> None:
    """Сохранить README.md."""
    full_path = str((path / 'README.md').absolute())
    with open(full_path, mode='w', encoding='utf-8') as file:
        file.write(readme)

    print(f'\tСохранён {path}')
