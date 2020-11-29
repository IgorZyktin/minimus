# -*- coding: utf-8 -*-

"""Инструменты работы с текстовым выводом для пользователя.
"""
from typing import Callable

from minimus import settings
from minimus.utils.text_processing import to_kv

VOCABULARY = {
    'RU': {
        'hello world': 'привет мир',

        'test {x}': 'тест {x}',

        '## All occurrences of the tag "{tag}"\n\n':
            '## Все вхождения тега "{tag}"\n\n',

        '# All entries"\n\n':
            '# Все записи\n\n',

        '\t{tag_number}. File created: {filename}':
            '\t{tag_number}. Создан файл: {filename}',

        '\t{number}. File has been updated: {filename}':
            '\t{number} Был обновлён файл: {filename}',

        'New folder has been created: {folder}':
            'Был создан каталог: {folder}',

        'Script has been started at folder: {folder}':
            'Скрипт был запущен в каталоге: {folder}',

        '\t{number}. File created: {filename}':
            '\t{number}. Создан файл: {filename}',

        '\tFile created: {filename}':
            '\tСоздан файл: {filename}',

        'Source directory: {folder}':
            'Каталог исходных данных: {folder}',

        'Output directory: {folder}':
            'Каталог обработанных данных: {folder}',

        'README.md directory: {folder}':
            'Каталог для файла README.md: {folder}',

        '\nStage 1. Metafile generation':
            '\nЭтап 1. Генерация метафайлов.',

        '\nStage 2. Indexes generation':
            '\nЭтап 2. Генерация индексов',

        '\nStage 4. Main files saving':
            '\nЭтап 4. Сохранение основных файлов',

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


def transliterate(something: str) -> str:
    """Выполнить транслитерацию из кириллицы.

    Используется только для имён файлов и
    не предполагает сложной обработки.

    >>> transliterate('Два весёлых гуся')
    'dva_veselyh_gusya'
    """
    return something.lower().translate(TRANS_MAP)


def announce(*args, callback: Callable = print, **kwargs) -> None:
    """Вывод для пользователя.
    """
    args = ', '.join(map(str, args))
    text = ', '.join([args, *to_kv(kwargs)])
    callback(text)


def stdout(template: str, *args,
           callback: Callable = print, **kwargs):
    """Вывод для пользователя, но с переводом на нужный язык.
    """
    template = translate(template, settings.LANGUAGE)
    text = template.format(**kwargs)
    announce(text, *args, callback=callback)


def translate(template: str, lang: str) -> str:
    """Перевести текст на нужный язык.

    >>> translate('hello world', 'RU')
    'привет мир'
    """
    if lang == 'EN' or lang not in VOCABULARY:
        return template

    return VOCABULARY[lang].get(template, template)
