# -*- coding: utf-8 -*-

"""Настройки всей программы.
"""
import os
import re

LANGUAGE = 'RU'

# настрока путей для загрузки/сохранения файлов
BASE_PATH = os.path.abspath(os.getcwd())
LAUNCH_DIRECTORY = BASE_PATH
SOURCE_DIRECTORY = os.path.join(BASE_PATH, 'source')
TARGET_DIRECTORY = os.path.join(BASE_PATH, 'target')
README_DIRECTORY = BASE_PATH

# шаблоны регулярных выражений

# шаблон заголовка файла
# пример: '# Заголовок'
TITLE_PATTERN = re.compile(r"""
    ^     # начало строки
    \s*?  # произвольное число пробелов
    \#+   # один или несколько октоторпов
    \s?   # опциональный пробел
    (.*)  # произвольный текст
""", flags=re.VERBOSE)

# шаблон сырого тега, пользователь ввёл только имя без ссылки
# пример: '{{ название }}'
HEAD_BARE_TAG_PATTERN = re.compile(r"""
    {{    # буквально двойные фигурные скобки 
    \s*?  # произвольное число пробелов
    (.*)  # произвольный текст
    \s*?  # произвольное число пробелов
    }}    # буквально двойные фигурные скобки 
""", flags=re.VERBOSE)

# шаблон полного тега, с гиперссылкой
# пример: '[{{ название }}](./file.md)'
FULL_TAG_PATTERN = re.compile(r"""
# текст ссылки в квадратных скобках
\[
    {{\s*?(.*)\s*?}}
\]
# адрес ссылки в круглых скобках
\(
    \./(.*.md)
\)
""", flags=re.VERBOSE)
