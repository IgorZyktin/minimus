"""Постоянные значения.
"""
import re

LOGO = """
███╗   ███╗██╗███╗   ██╗██╗   ██╗███╗   ███╗██╗   ██╗███████╗    ██████╗     ██████╗
████╗ ████║██║████╗  ██║██║   ██║████╗ ████║██║   ██║██╔════╝    ╚════██╗   ██╔═████╗
██╔████╔██║██║██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║███████╗     █████╔╝   ██║██╔██║
██║╚██╔╝██║██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║╚════██║    ██╔═══╝    ████╔╝██║
██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████║    ███████╗██╗╚██████╔╝
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝    ╚══════╝╚═╝ ╚═════╝
""".strip()  # noqa

LINE = '-' * (max(len(x) for x in LOGO.split('\n')))

UNKNOWN = '???'
README_FILENAME = 'README.md'
CACHE_FILENAME = '.minimus_cache.json'
TAGS_FOLDER = '__tags'

IGNORED_PREFIXES = (
    '~',
    '.',
    '_',
)

SUPPORTED_EXTENSIONS = (
    '.md',
)

SMALL_LETTERS = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
                 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
                 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
                 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
                 'э': 'e', 'ю': 'y', 'я': 'ya', ' ': '_', }

BIG_LETTERS = {
    key.upper(): value.upper()
    for key, value in SMALL_LETTERS.items()
}

TRANS_MAP = str.maketrans({**SMALL_LETTERS, **BIG_LETTERS})

# Базовый шаблон для тега, любые включения в документ
# Примеры: '{{ something }}', '[{{ tag }}](./tag.md)'
BASIC_TAG_PATTERN = re.compile(r"""
    {{       # две открывающие фигурные скобки
    \s+?     # ноль или более пробелов
    (.+?)    # произвольный текст
    \s+?     # ноль или более пробелов
    }}       # две закрывающие фигурные скобки
""", flags=re.VERBOSE)

# Шаблон заголовка файла
# Примеры: '# something'
TITLE_PATTERN = re.compile(r"""
    ^        # начало строки
    \#       # октоторп        
    \s+?     # ноль или более пробелов
    (.+)    # произвольный текст
""", flags=re.VERBOSE)
