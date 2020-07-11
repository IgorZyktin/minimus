# -*- coding: utf-8 -*-

"""Автоматический линковщик для заметок.

Выполняет следующие функции:
    1. Порождает метадокументы для тегов. Странички, на которых можно
    посмотреть, где ещё используется этот тег.
    2. Модифицирует вхождения тегов в документ,
    заменяя их ссылками на соответствующие метастраницы тегов.
"""
import json
import os
import re
import shutil
import string
import sys
from collections import defaultdict
from functools import total_ordering
from pathlib import Path
from typing import (
    List, Callable, Union, TypeVar, Type, Optional, Tuple,
    Any, Dict, Set, Collection, Generator
)

__all__ = [
    'Config',
    'Graph',
    'Syntax',
    'TextFile',
    'Filesystem',
    'MarkdownSyntax',
    'HTMLSyntax',

    'map_tags_to_files',
]

T = TypeVar('T')


class Config:
    """Хранилище настроек.
    """
    bg_color_tag = '#04266c'
    bg_color_node = '#5a0000'
    protocol = 'file://'

    source_directory = Path().absolute()
    target_directory = Path().absolute()

    custom_source = False
    custom_target = False

    HTML_TEMPLATE = """
    <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>$title</title>
            <link rel="stylesheet" href="lib/styles.css" type="text/css">
            <script src="lib/jquery-3.5.1.min.js" 
                type="application/javascript"></script>
            <script src="lib/arbor.js" 
                type="application/javascript"></script>
            <script src="lib/rendering.js" 
                type="application/javascript"></script>
            <script src="lib/main.js" 
                type="application/javascript"></script>
        </head>
        <body>
            <canvas id="viewport" width="1000" height="1000"></canvas>
            <script type="application/javascript">
                let main_data_block = $nodes;
            </script>
        </body>
    </html>
    """


class Syntax:
    """Мастер по манипуляциям с любым текстом.
    """
    _small_letters = {
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
    _big_letters = {
        key.upper(): value.upper() for key, value in _small_letters.items()
    }
    _trans_map = str.maketrans({**_small_letters, **_big_letters})

    @classmethod
    def transliterate(cls, something: str) -> str:
        """Выполнить транслитерацию из кириллицы.

        Используется только для имён файлов и
        не предполагает сложности обработки.

        >>> Syntax.transliterate('Два весёлых гуся')
        'dva_veselyh_gusya'
        """
        return something.lower().translate(cls._trans_map)

    @staticmethod
    def announce(*args, callback: Callable = print, **kwargs) -> None:
        """Вывод для пользователя.
        """
        args = ', '.join(map(str, args))
        kwargs = [f'{key}={value}' for key, value in kwargs.items()]
        callback(', '.join([args, *kwargs]))

    @staticmethod
    def make_prefix(total: int) -> str:
        """Собрать префикс для нумерации.
        """
        digits = len(str(total))
        prefix = '{{num:0{0}}} из {{total:0{0}d}}'.format(digits)
        return prefix

    @classmethod
    def numerate(cls, collection: Collection[T]) \
            -> Generator[Tuple[str, T], None, None]:
        """Аналог enumerate, только с красивыми номерами.
        """
        total = len(collection)
        prefix = cls.make_prefix(total)

        for i, each in enumerate(collection, start=1):
            number = prefix.format(num=i, total=total)
            yield number, each

    @staticmethod
    def to_json(something: dict) -> str:
        """Преобразовать словарь в JSON строку.
        """
        return json.dumps(something, ensure_ascii=False, indent=4)


@total_ordering
class TextFile:
    """Текстовый файл с произвольным содержимым.
    """
    normal_attrs = {'filename', 'contents', 'is_changed', '_filename',
                    '_contents',
                    'attrs', 'original_contents', 'original_filename'}

    def __init__(self, filename: str, contents: str, is_changed: bool = False):
        """Инициализировать экземпляр.
        """
        self.original_contents = contents
        self.original_filename = filename
        self._contents = contents
        self._filename = filename
        self.is_changed = is_changed
        self.attrs = {}

    def __repr__(self) -> str:
        """Текстовое представление.
        """
        return '{type}({filename})'.format(
            type=type(self).__name__,
            filename=repr(self.filename),
        )

    def __eq__(self, other):
        """Проверка на равенство.

        Нужна для сортировки по имени, поэтому проверяется только имя.
        """
        if isinstance(other, type(self)):
            return self.filename == other.filename
        return False

    def __lt__(self, other):
        """Проверка, на то, что значение меньше.

        Нужна для сортировки по имени, поэтому проверяется только имя.
        """
        if isinstance(other, type(self)):
            return self.filename < other.filename
        return NotImplemented

    def __hash__(self) -> int:
        """Вернуть хеш по содержимому.
        """
        return hash(self.filename)

    def __getattr__(self, item: str) -> Any:
        """В любой непонятной ситуации мы пытаемся обратиться к attrs.
        """
        value = self.attrs.get(item)

        if value is None:
            raise AttributeError(f'Экземпляр {self} не '
                                 f'имеет атрибута {item}.')
        return value

    def __setattr__(self, key: str, value: Any) -> None:
        """По умолчанию все атрибуты дописываются в attrs.
        """
        if key not in self.normal_attrs:
            self.attrs[key] = value
            return

        object.__setattr__(self, key, value)

    @property
    def filename(self) -> str:
        """Вернуть имя файла.
        """
        return self._filename

    @filename.setter
    def filename(self, new_filename: str) -> None:
        """Изменить содержимое файла.
        """
        self._filename = new_filename
        self.is_changed = True

    @property
    def contents(self) -> str:
        """Вернуть текстовое содержимое файла.
        """
        return self._contents

    @contents.setter
    def contents(self, new_contents: str) -> None:
        """Изменить содержимое файла.
        """
        self._contents = new_contents
        self.is_changed = True


class Filesystem:
    """Мастер по работе с файловой системой.
    """
    names_to_ignore = ('index', 'meta')

    @classmethod
    def get_files_of_type(cls, directory: Path, suffix: str,
                          desired_type: Type[T],
                          ignore: Optional[Tuple[str, ...]] = None) -> List[T]:
        """Получить перечень всех документов нужного типа в каталоге.

        Пример вывода:
        [
            TextFile('2020-07-06_elephant.md'),
            TextFile('2020-07-06_mouse.md'),
            TextFile('2020-07-06_recursion.md'),
            TextFile('2020-07-06_vacuum.md')
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
    def ensure_folder_exists(cls, target: Path):
        """Создать всю цепочку каталогов для указанного пути.
        """
        path = None
        parts = list(target.parts[:-1])

        while parts:
            if path is None:
                path = Path(parts.pop(0))

            else:
                path = path / parts.pop(0)

            if path.is_file():
                break

            if not path.exists():
                os.mkdir(cls.cast_path(path))
                Syntax.announce(f'Был создан каталог "{path}"')

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
            cls.ensure_folder_exists(filename)
            path = cls.cast_path(filename)
            with open(path, mode='w', encoding='utf-8') as file:
                file.write(contents)
                return True
        return False

    @classmethod
    def copy(cls, name_from: Path, name_to: Path):
        """Скопировать файл.
        """
        cls.ensure_folder_exists(name_to)

        shutil.copy(
            cls.cast_path(name_from),
            cls.cast_path(name_to)
        )


class Graph:
    """Представление графа.
    """

    def __init__(self):
        """Инициализировать экземпляр.
        """
        self.nodes = {}
        self.edges = {}

    def add_node(self, name: str, label: str,
                 bg_color: str, link: str) -> None:
        """Добавить ноду в граф.
        """
        self.nodes[name] = {
            'label': label,
            'bg_color': bg_color,
            'link': link,
        }

    def add_edge(self, node_start: str, node_finish: str,
                 weight: float = 0.1) -> None:
        """Добавить грань в граф.
        """
        if node_start not in self.edges:
            self.edges[node_start] = {}

        self.edges[node_start][node_finish] = {'weight': weight}

    def as_dict(self) -> dict:
        """Вернуть граф в форме словаря.
        """
        return {
            'nodes': self.nodes,
            'edges': self.edges,
        }


class HTMLSyntax:
    """Мастер по работе с форматом HTML.
    """

    @staticmethod
    def get_index_filename() -> str:
        """Вернуть название файла индекса.
        """
        return 'index.html'

    @classmethod
    def get_tag_filename(cls, tag: str) -> str:
        """Вернуть соответствующее тегу имя файла.

        >>> HTMLSyntax.get_tag_filename('планирование')
        'meta_planirovanie.html'
        """
        return 'meta_' + Syntax.transliterate(tag) + '.html'

    @staticmethod
    def get_local_dir() -> str:
        """Выдать локальную папку в читаемом для html формате.
        """
        return str(Config.target_directory.absolute()).replace('\\', '/')

    @classmethod
    def make_link(cls, text: str, protocol: Optional[str] = None) -> str:
        """Собрать ссылку для графа.
        """
        protocol = protocol or Config.protocol
        directory = cls.get_local_dir()
        return protocol + directory + '/' + text

    @classmethod
    def render_tag_graph(cls, tag: str, files: List['TextFile']) -> dict:
        """Собрать граф для отображения тега.
        """
        graph = Graph()

        graph.add_node(
            'tag', tag, Config.bg_color_tag,
            link=cls.make_link(MarkdownSyntax.get_tag_filename(tag))
        )

        for i, file in enumerate(files, start=1):
            graph.add_node(
                file.filename, file.title, Config.bg_color_node,
                link=cls.make_link(file.filename)
            )
            graph.add_edge('tag', file.filename)

        return graph.as_dict()

    @classmethod
    def render_index_graph(cls, files: List['TextFile']) -> dict:
        """Собрать граф для отображения стартовой страницы.
        """
        graph = Graph()

        for file in files:
            graph.add_node(
                file.filename, file.title, Config.bg_color_node,
                link=cls.make_link(file.filename)
            )

            for tag in file.tags:
                name = Syntax.transliterate(tag)
                graph.add_node(
                    name, tag, Config.bg_color_tag,
                    link=cls.make_link(MarkdownSyntax.get_tag_filename(tag))
                )
                graph.add_edge(file.filename, name)

        return graph.as_dict()

    @classmethod
    def make_metafile_contents(cls, tag: str,
                               files: List['TextFile']) -> str:
        """Собрать текст метафайла из исходных данных.
        """
        template = string.Template(Config.HTML_TEMPLATE)
        content = template.safe_substitute({
            'title': tag,
            'nodes': Syntax.to_json(cls.render_tag_graph(tag, files))
        })
        return content

    @classmethod
    def make_index_contents(cls, files: List['TextFile']) -> str:
        """Собрать текст стартовой страницы из исходных данных.
        """
        template = string.Template(Config.HTML_TEMPLATE)
        content = template.safe_substitute({
            'title': 'Стартовая страница',
            'nodes': Syntax.to_json(cls.render_index_graph(files))
        })
        return content


class MarkdownSyntax:
    """Мастер по работе с форматом MarkDown.

    TITLE_PATTERN - шаблон заголовка
        Произвольное количество пробелов от начала строки, за которыми следуют
        один или несколько октоторпов. Потом идёт обязательный пробел (одно из
        отличий заголовка от тега), за которым произвольный набор символов
        до конца строки.

    HEAD_BARE_TAG_PATTERN - шаблон голого тега из заголовка статьи.
        Это тег, который ещё не был отформатирован пользователем.
        Строго с начала строки, затем экранированный октоторп и
        сразу текст без пробела, считываемый до конца строки.

    BODY_BARE_TAG_PATTERN - неотформатированный тег, но уже в теле документа.
        Мы заведомо не знаем, где кончается текст тега, так что этот
        шаблон надо по месту достравивать для каждого тега.

    FULL_TAG_PATTERN - отформатированный тег в теле документа.
        Он уже оформлен в виде гиперссылки.
    """
    TITLE_PATTERN = re.compile(r"^\s*#+\s(.*)", flags=re.MULTILINE)

    HEAD_BARE_TAG_PATTERN = re.compile(r'^\\#(.*)$', flags=re.MULTILINE)
    HEAD_BARE_TAG_PATTERN_CUSTOM = r'^\\#{}$'
    BODY_BARE_TAG_PATTERN_CUSTOM = r'(?<!\[)\\#({})(?!\])'

    FULL_TAG_PATTERN = re.compile(r'\[\\#(.*)\]\(\./(.*.md)\)')

    @staticmethod
    def href(label: str, link: str) -> str:
        """Собрать гиперссылку из частей.

        >>> MarkdownSyntax.href('Hello!', 'world')
        '[Hello!](./world)'
        """
        return '[{}](./{})'.format(label, link)

    @staticmethod
    def get_index_filename() -> str:
        """Вернуть название файла индекса.
        """
        return 'index.md'

    @staticmethod
    def get_tag_filename(tag: str) -> str:
        """Вернуть соответствующее тегу имя файла.

        >>> MarkdownSyntax.get_tag_filename('планирование')
        'meta_planirovanie.md'
        """
        return 'meta_' + Syntax.transliterate(tag) + '.md'

    @classmethod
    def tag2href(cls, tag: str) -> str:
        """Из текста тега сформировать гиперссылку.
        """
        filename = cls.get_tag_filename(tag)
        href = cls.href('\\#' + tag, filename)
        return href

    @classmethod
    def extract_title(cls, content: str) -> str:
        """Извлечь заголовок из тела документа.
        """
        match = cls.TITLE_PATTERN.match(content)
        if match:
            return match.groups()[0].strip()
        return '???'

    @classmethod
    def extract_tags(cls, content: str) -> Set[str]:
        """Извлечь все теги из тела документа.
        """
        all_tags = set()
        bare_tags = set()

        for each in cls.HEAD_BARE_TAG_PATTERN.findall(content):
            bare_tags.add(each)
            all_tags.add(each)

        for each in bare_tags:
            sub_pattern = cls.BODY_BARE_TAG_PATTERN_CUSTOM.format(each)
            for sub_tag in re.findall(sub_pattern, content):
                all_tags.add(sub_tag)

        for full_tag in cls.FULL_TAG_PATTERN.finditer(content):
            tag_text, _ = full_tag.groups()
            all_tags.add(tag_text)

        return {x.lower().strip() for x in all_tags}

    @classmethod
    def replace_tags_with_hrefs(cls, content: str, tags: Set[str]) -> str:
        """Перестроить текст так, чтобы теги стали гиперрсылками.
        """
        bare_tags = set()

        for each in cls.HEAD_BARE_TAG_PATTERN.findall(content):
            bare_tags.add(each)
            sub_pattern = cls.HEAD_BARE_TAG_PATTERN_CUSTOM.format(each)
            content = re.sub(sub_pattern, cls.tag2href(each), content)

        for each in tags:
            sub_pattern = cls.BODY_BARE_TAG_PATTERN_CUSTOM.format(each)
            content = re.sub(sub_pattern, cls.tag2href(each), content)

        return content

    @staticmethod
    def render_text(title: str, files: List['TextFile']) -> str:
        """Собрать базовый вариант md документа.
        """
        if not files:
            return ''

        lines = [
            f'{title}\n',
            '---\n'
        ]

        for number, file in Syntax.numerate(sorted(files)):
            lines.append('{}. {}\n'.format(
                number,
                MarkdownSyntax.href(file.title, file.filename)
            ))

        lines.append('')

        return '\n'.join(lines)

    @classmethod
    def make_metafile_contents(cls, tag: str, files: List['TextFile']) -> str:
        """Собрать текст метафайла из исходных данных.
        """
        return cls.render_text(f'## Все вхождения тега "{tag}"', files)

    @classmethod
    def make_index_contents(cls, files: List['TextFile']) -> str:
        """Собрать текст стартовой страницы из исходных данных.
        """
        return cls.render_text('# Все записи', files)


def ensure_each_tag_has_metafile(
        tags_to_files: Dict[str, List[TextFile]]) -> None:
    """Удостовериться, что для каждого тега есть персональная страничка.

    Вместо проверки правильности, она просто каждый раз создаётся заново.
    """
    total = len(tags_to_files) * 2
    prefix = Syntax.make_prefix(total)

    i = 1
    for tag, tag_files in tags_to_files.items():
        # markdown форма
        name = Config.target_directory / MarkdownSyntax.get_tag_filename(tag)
        contents = MarkdownSyntax.make_metafile_contents(tag, tag_files)
        Filesystem.write(name, contents)
        number = prefix.format(num=i, total=total)
        Syntax.announce(f'{number}. Создан файл "{name}"')
        i += 1

        # html форма
        name = Config.target_directory / HTMLSyntax.get_tag_filename(tag)
        contents = HTMLSyntax.make_metafile_contents(tag, tag_files)
        Filesystem.write(name, contents)
        number = prefix.format(num=i, total=total)
        Syntax.announce(f'{number}. Создан файл "{name}"')
        i += 1


def ensure_each_tag_has_link(files: List['TextFile']) -> None:
    """Удостовериться, что каждый тег является ссылкой, а не текстом.
    """
    for file in files:
        existing_contents = file.contents
        new_contents = MarkdownSyntax.replace_tags_with_hrefs(
            content=existing_contents,
            tags=file.tags
        )

        if new_contents != existing_contents:
            file.contents = new_contents


def ensure_index_exists(files: List[TextFile]) -> None:
    """Удостовериться, что у нас есть стартовая страница.
    """
    if not files:
        return

    # markdown форма
    name = Config.target_directory / MarkdownSyntax.get_index_filename()
    contents = MarkdownSyntax.make_index_contents(files)
    if Filesystem.write(name, contents):
        Syntax.announce(f'Создан файл "{name}"')

    # html форма
    name = Config.target_directory / HTMLSyntax.get_index_filename()
    contents = HTMLSyntax.make_index_contents(files)
    if Filesystem.write(name, contents):
        Syntax.announce(f'Создан файл "{name}"')


def map_tags_to_files(files: List[TextFile]) -> Dict[str, List[TextFile]]:
    """Собрать отображение тегов на файлы.
    """
    tags_to_files = defaultdict(list)

    for file in files:
        file.title = MarkdownSyntax.extract_title(file.contents)
        file.tags = MarkdownSyntax.extract_tags(file.contents)
        for tag in file.tags:
            tags_to_files[tag].append(file)

    return {
        tag: sorted(files)
        for tag, files in tags_to_files.items()
    }


def init():
    """Подготовить параметры перед запуском.
    """
    if '--localexplorer' in sys.argv:
        Config.protocol = 'localexplorer:'
        Syntax.announce('Сборка будет произведена со '
                        'стилем ссылок Local Explorer.')

    for i in range(len(sys.argv)):
        if sys.argv[i] == '--source_directory':
            Config.source_directory = Path(sys.argv[i + 1]).absolute()
            Config.custom_source = True

        if sys.argv[i] == '--target_directory':
            Config.target_directory = Path(sys.argv[i + 1]).absolute()
            Config.custom_target = True

    main()


def main():
    """Точка входа.
    """
    Syntax.announce(f'Анализируем каталог "{Config.source_directory}"')

    files = Filesystem.get_files_of_type(
        Config.source_directory, 'md', TextFile
    )
    tags_to_files = map_tags_to_files(files)

    ensure_each_tag_has_metafile(tags_to_files)
    ensure_each_tag_has_link(files)
    ensure_index_exists(files)

    changed = []
    for file in files:
        if (file.is_changed or Config.custom_target) and file.contents:
            name = Config.target_directory / file.filename
            changed.append((name, file.contents))

    for number, (name, contents) in Syntax.numerate(changed):
        Filesystem.write(name, contents)
        Syntax.announce(f'{number}. Сохранены изменения в файле "{name}"')

    if not files:
        Syntax.announce('Не найдено файлов для обработки.')

    elif Config.custom_target:
        for file in (Config.source_directory / 'lib').iterdir():
            Filesystem.copy(
                Config.source_directory / 'lib' / file.name,
                Config.target_directory / 'lib' / file.name,
            )


if __name__ == '__main__':
    init()  # pragma: no cover
