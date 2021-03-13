# -*- coding: utf-8 -*-

"""Project wide constants.
"""
VOCABULARY = {
    'RU': {
        'hello world': 'привет мир',

        'test {x}': 'тест {x}',

        '  Script started at: {folder}':
            '  Скрипт запущен в каталоге: {folder}',

        '   Source directory: {folder}':
            '    Каталог исходных данных: {folder}',

        '   Output directory: {folder}':
            'Каталог обработанных данных: {folder}',

        'README.md directory: {folder}':
            'Каталог для файла README.md: {folder}',

        ' New folder created: {folder}':
            '             Создан каталог: {folder}',


        '## All occurrences of the tag "{tag}"':
            '## Все вхождения тега "{tag}"',

        '# All entries':
            '# Все записи',



        '\t{number}. File created: {filename}':
            '\t{number}. Создан файл: {filename}',

        '\tFile created: {filename}':
            '\tСоздан файл: {filename}',

        'Stage 1. Metafile generation':
            'Этап 1. Генерация метафайлов',

        'Stage 2. Indexes generation':
            'Этап 2. Генерация индексов',

        'Stage 3. Main files saving':
            'Этап 3. Сохранение основных файлов',

        'Stage 4. Additional files saving':
            'Этап 4. Сохранение дополнительных файлов',

        'No source files found to work with':
            'Не найдено файлов для обработки',

        '\t{number}. Saved changes: {filename}':
            '\t{number}. Сохранены изменения: {filename}',

        '\t{number}. No changes detected: {filename}':
            '\t{number}. Файл не менялся: {filename}',

        '\t{number}. Copied file: {filename}':
            '\t{number}. Скопирован файл: {filename}',

        'Metainfo: {total} entries saved':
            'Метаинформация: сохранено {total} записей',

        'Processing complete in {seconds} sec.':
            'Обработка завершена за {seconds} сек.',

        '\tNo files to save':
            '\tНет файлов для сохранения',

        'Version: {version}, last_update: {last_update}':
            'Версия: {version}, последнее обновление: {last_update}',

        '### This tag occurs with':
            '### Этот тег встречается вместе с',
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