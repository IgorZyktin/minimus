# -*- coding: utf-8 -*-

"""Специальный класс для работы с файловой системой.
"""
import os
import shutil
from pathlib import Path
from typing import Type, TypeVar, Optional, Tuple, List, Union

from minimus.syntax import Syntax

T = TypeVar('T')


class FileSystem:
    """Специальный класс для работы с файловой системой.
    """
    names_to_ignore = (
        'index',
        'meta',
    )

    @classmethod
    def get_files_of_type(cls,
                          directory: Path,
                          suffix: str,
                          desired_type: Type[T],
                          ignore: Optional[Tuple[str, ...]] = None
                          ) -> List[T]:
        """Получить перечень всех документов нужного типа в каталоге.

        Пример вывода:
        [
            TextFile('2020-07-06_elephant.md'),
            TextFile('2020-07-06_mouse.md'),
            TextFile('2020-07-06_recursion.md'),
            TextFile('2020-07-06_vacuum.md'),
        ]
        """
        files = []
        ignore = ignore or cls.names_to_ignore

        for file in directory.iterdir():
            filename = file.name.lower()

            if filename.startswith(ignore):
                continue

            if filename.endswith(suffix):
                contents = cls.read(file)
                new_instance = desired_type(filename, contents)
                files.append(new_instance)

        return files

    @staticmethod
    def cast_path(filename: Union[str, Path]) -> str:
        """Преобразовать Path в текстовый путь.
        """
        if isinstance(filename, str):
            return filename
        return str(filename.absolute())

    @classmethod
    def ensure_folder_exists(cls, target: Path) -> Optional[str]:
        """Создать всю цепочку каталогов для указанного пути.

        Вернуть путь, если каталог был создан.
        """
        path = Path('.')
        parts = list(target.parts)[::-1]
        created = None

        while parts:
            path = path / parts.pop()

            if not parts and '.' in path.name:
                # это по всей видимости файл
                break

            if not path.exists():
                created = cls.cast_path(path)
                os.mkdir(created)

        return created

    @classmethod
    def read(cls, filename: Path) -> str:
        """Поднять содержимое файла с жёсткого диска.
        """
        path = cls.cast_path(filename)
        with open(path, mode='r', encoding='utf-8') as file:
            contents = file.read()
        return contents

    @classmethod
    def write(cls, filename: Path, contents: str) -> bool:
        """Сохранить некий текст под определённым именем на диск.
        """
        if contents:
            path = cls.cast_path(filename)
            with open(path, mode='w', encoding='utf-8') as file:
                file.write(contents)
                return True
        return False

    @classmethod
    def copy(cls, copy_from: Path, copy_to: Path):
        """Скопировать файл.
        """
        shutil.copy(
            cls.cast_path(copy_from),
            cls.cast_path(copy_to)
        )
