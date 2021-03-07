# -*- coding: utf-8 -*-

"""Main settings.
"""

import os

__version__ = '1.4'
LAST_UPDATE = '2021-03-07'

LOGO = """
  ███╗   ███╗  ██╗  ███╗   ██╗  ██╗  ███╗   ███╗  ██╗   ██╗  ███████╗
  ████╗ ████║  ██║  ████╗  ██║  ██║  ████╗ ████║  ██║   ██║  ██╔════╝
  ██╔████╔██║  ██║  ██╔██╗ ██║  ██║  ██╔████╔██║  ██║   ██║  ███████╗
  ██║╚██╔╝██║  ██║  ██║╚██╗██║  ██║  ██║╚██╔╝██║  ██║   ██║  ╚════██║
  ██║ ╚═╝ ██║  ██║  ██║ ╚████║  ██║  ██║ ╚═╝ ██║  ╚██████╔╝  ███████║
  ╚═╝     ╚═╝  ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝     ╚═╝   ╚═════╝   ╚══════╝
""".rstrip()

LINE = '-' * (max(len(x) for x in LOGO.split('\n')) + 2)

# localisation of the user interface
LANGUAGE = 'RU'

# paths to work with
METAFILE_NAME = 'meta.json'
BASE_PATH = os.path.abspath(os.getcwd())
LAUNCH_DIRECTORY = BASE_PATH

SOURCE_DIRECTORY = os.path.join(BASE_PATH, 'source')
TARGET_DIRECTORY = os.path.join(BASE_PATH, 'target')
README_DIRECTORY = TARGET_DIRECTORY
