# -*- coding: utf-8 -*-

"""Инструменты работы с файловой системой.
"""
import json
import os
from typing import Dict

from colorama import Fore

from minimus.components.class_meta import Meta
from minimus.components.class_statistic import Statistic
from minimus.utils.filesystem import join, ensure_folder_exists
from minimus.utils.output_processing import translate, stdout


def get_metainfo(source_directory: str, language: str) -> Dict[str, Meta]:
    """Собрать плоский список всего, что есть в source_directory.

    Каталоги игнорируются.
    """
    if not os.path.exists(source_directory):
        return {}

    metainfo = {}

    for path, _, filenames in os.walk(source_directory):
        for filename in filenames:
            if filename in metainfo:
                raise FileExistsError(translate(
                    'Filenames are supposed to be unique: {filename}',
                    language=language,
                ))

            full_path = join(path, filename)
            stat = os.stat(full_path)
            meta = Meta(
                original_filename=filename,
                original_path=path,
                statistic=Statistic(
                    created_at=stat.st_ctime_ns,
                    modified_at=stat.st_mtime_ns,
                    size=stat.st_size,
                ),
            )
            metainfo[meta.original_filename] = meta

    return metainfo


def get_stored_metainfo(source_directory: str,
                        metafile_name: str) -> Dict[str, Meta]:
    """Попытаться загрузить метаинформацию с прошлого запуска.
    """
    path = join(source_directory, metafile_name)

    metainfo = {}

    try:
        with open(path, mode='r', encoding='utf-8') as file:
            raw_metainfo = json.load(file)

        for contents in raw_metainfo.values():
            meta = Meta.from_dict(contents)
            metainfo[meta.original_filename] = meta

    except FileNotFoundError:
        pass

    return metainfo


def dump_metainfo(directory: str, filename: str,
                  metainfo: Dict[str, Meta], language: str) -> None:
    """Сохранить актуальную метаинформацию на диск.
    """
    as_dict = {
        filename: meta.to_dict()
        for filename, meta in metainfo.items()
    }

    path = join(directory, filename)

    with open(path, mode='w', encoding='utf-8') as file:
        json.dump(as_dict, file, ensure_ascii=False, indent=4)

    stdout(
        template='\nMetainfo: {total} entries saved',
        language=language,
        total=len(as_dict),
        color=Fore.MAGENTA,
    )


def write_text(path: str, filename: str, content: str, language: str) -> str:
    """Сохранить некий текст под определённым именем на диск.
    """
    if not content:
        return ''

    full_path = join(path, filename)
    ensure_folder_exists(path, language)

    with open(full_path, mode='w', encoding='utf-8') as file:
        file.write(content)

    return full_path


def read_text(path: str, filename: str) -> str:
    """прочитать определённый файл с диска.
    """
    full_path = join(path, filename)

    with open(full_path, mode='r', encoding='utf-8') as file:
        content = file.read()

    return content
