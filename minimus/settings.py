# -*- coding: utf-8 -*-

"""Настройки всей программы.
"""

import os

__version__ = '1.2'

LOGO = """
███╗   ███╗  ██╗  ███╗   ██╗  ██╗  ███╗   ███╗  ██╗   ██╗  ███████╗
████╗ ████║  ██║  ████╗  ██║  ██║  ████╗ ████║  ██║   ██║  ██╔════╝
██╔████╔██║  ██║  ██╔██╗ ██║  ██║  ██╔████╔██║  ██║   ██║  ███████╗
██║╚██╔╝██║  ██║  ██║╚██╗██║  ██║  ██║╚██╔╝██║  ██║   ██║  ╚════██║
██║ ╚═╝ ██║  ██║  ██║ ╚████║  ██║  ██║ ╚═╝ ██║  ╚██████╔╝  ███████║
╚═╝     ╚═╝  ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝     ╚═╝   ╚═════╝   ╚══════╝
""".strip()

LINE = '-' * len(LOGO.split('\n')[0])

# настройки локализации вывода для пользователя
LANGUAGE = 'RU'

# настрока путей для загрузки/сохранения файлов
METAFILE_NAME = 'meta.json'
BASE_PATH = os.path.abspath(os.getcwd())
LAUNCH_DIRECTORY = BASE_PATH

SOURCE_DIRECTORY = os.path.join(BASE_PATH, 'source')
TARGET_DIRECTORY = os.path.join(BASE_PATH, 'target')
README_DIRECTORY = TARGET_DIRECTORY
