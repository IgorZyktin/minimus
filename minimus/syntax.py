# -*- coding: utf-8 -*-

"""Специальный класс для работы с текстом.
"""
import json
from typing import TypeVar, List, Callable, Generator, Tuple, Iterable

from minimus.config import Config

T = TypeVar('T')


class Syntax:
    """Специальный класс для работы с текстом.
    """
    VOCABULARY = {
        'RU': {
            'test {x}': 'тест {x}',
            'New folder has been created: {folder}':
                'Был создан каталог {folder}',
            'Script has been started at folder {folder}':
                'Скрипт был запущен в каталоге {folder}',
            '\t{number}. File created: {filename}':
                '\t{number}. Создан файл: {filename}',
            'Unable to find folder with libraries: {folder}':
                'Не удаётся найти каталог с библиотеками: {folder}',
            'Unable to find folder with source files: {folder}':
                'Не удаётся найти каталог исходных данных: {folder}',
            'Source files folder: {folder}':
                'Каталог исходных данных: {folder}',
            'Output files folder: {folder}':
                'Каталог обработанных данных: {folder}',
            'The assembly will be done using the Local Explorer links style':
                'Сборка будет произведена со стилем ссылок Local Explorer',
            '\nStage 1. Metafile generation':
                '\nЭтап 1. Генерация метафайлов.',
            '\nStage 2. Hyperlinks generation':
                '\nЭтап 2. Генерация гиперссылок',
            '\nStage 3. Indexes generation':
                '\nЭтап 3. Генерация индексов',
            '\nStage 4. Main files saving':
                '\nЭтап 4. Сохранение основных файлов',
            '\nStage 5. Libraries copying':
                '\nЭтап 5. Копирование библиотек',
            '\t{number} File has been copied: {filename}':
                '\t{number}. Скопирован файл {filename}',
            'No source files found to work with':
                'Не найдено файлов для обработки',
            '\t{number}. Saved changes to the file {filename}':
                '\t{number}. Сохранены изменения в файле {filename}',
        }
    }

    SMALL_LETTERS = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sch',
        'ъ': '',
        'ы': 'y',
        'ь': '',
        'э': 'e',
        'ю': 'y',
        'я': 'ya',
        ' ': '_',
    }

    BIG_LETTERS = {
        key.upper(): value.upper()
        for key, value in SMALL_LETTERS.items()
    }

    TRANS_MAP = str.maketrans(
        {
            **SMALL_LETTERS,
            **BIG_LETTERS
        }
    )
    config: Config

    @classmethod
    def set_config(cls, given_config: Config) -> None:
        """Запомнить новый экземпляр настроек.
        """
        cls.config = given_config

    @classmethod
    def transliterate(cls, something: str) -> str:
        """Выполнить транслитерацию из кириллицы.

        Используется только для имён файлов и
        не предполагает сложной обработки.

        >>> Syntax.transliterate('Два весёлых гуся')
        'dva_veselyh_gusya'
        """
        return something.lower().translate(cls.TRANS_MAP)

    @staticmethod
    def to_kv(something: dict) -> List[str]:
        """Разложить словарь в набор пар ключ=значение.
        """
        return [
            f'{key}={value}'
            for key, value in something.items()
        ]

    @classmethod
    def announce(cls, *args, callback: Callable = print, **kwargs) -> None:
        """Вывод для пользователя.
        """
        args = ', '.join(map(str, args))
        callback(', '.join([args, *cls.to_kv(kwargs)]))

    @classmethod
    def stdout(cls, template: str, *args,
               callback: Callable = print, **kwargs):
        """Вывод для пользователя, но с переводом на нужный язык.
        """
        template = cls.translate(template, cls.config.lang)
        text = template.format(**kwargs)
        cls.announce(text, *args, callback=callback)

    @classmethod
    def translate(cls, template: str, lang: str) -> str:
        """Перевести текст на нужный язык.
        """
        if lang == 'EN' or lang not in cls.VOCABULARY:
            return template

        return cls.VOCABULARY[lang].get(template, template)

    @staticmethod
    def make_prefix(total: int) -> str:
        """Собрать префикс для нумерации.
        """
        digits = len(str(total))
        prefix = '{{num:0{0}}} из {{total:0{0}d}}'.format(digits)
        return prefix

    @classmethod
    def numerate(cls, collection: Iterable[T]) \
            -> Generator[Tuple[str, T], None, None]:
        """Аналог enumerate, только с красивыми номерами.
        """
        collection = list(collection)
        total = len(collection)
        prefix = cls.make_prefix(total)

        for i, each in enumerate(collection, start=1):
            number = prefix.format(num=i, total=total)
            yield number, each

    @staticmethod
    def to_json(something: dict, indent: int = 4) -> str:
        """Преобразовать словарь в JSON строку.
        """
        return json.dumps(something, ensure_ascii=False, indent=indent)
