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
import string
from collections import defaultdict
from functools import cached_property, total_ordering
from pathlib import Path
from typing import List, Set, Callable, Union, TypeVar, Type, Optional, Tuple

__all__ = [
    'Syntax',
    'TextFile',
    'Filesystem',
]

T = TypeVar('T')


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


@total_ordering
class TextFile:
    """Текстовый файл с произвольным содержимым.
    """

    def __init__(self, filename: str, contents: str, is_changed: bool = False):
        """Инициализировать экземпляр.
        """
        self._original_contents = contents
        self._contents = contents
        self.filename = filename
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
        return False

    def __hash__(self) -> int:
        """Вернуть хеш по содержимому.
        """
        return hash(self.filename)

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
    def read(cls, filename: Union[str, Path]) -> str:
        """Поднять содержимое файла с жёсткого диска.
        """
        path = cls.cast_path(filename)
        with open(path, mode='r', encoding='utf-8') as file:
            contents = file.read()
        return contents

    @classmethod
    def write(cls, filename: Union[str, Path], contents: str,
              log: Callable = Syntax.announce) -> None:
        """Сохранить некий текст под определённым именем на диск.
        """
        if contents:
            path = cls.cast_path(filename)
            with open(path, mode='w', encoding='utf-8') as file:
                file.write(contents)
                log(f'Сохранены изменения в файле "{filename}"')















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





# class HTML:
#     """Контейнер для инструментов обработки текста в формате html.
#     """
#
#     @classmethod
#     def get_tag_filename(cls, tag: str) -> str:
#         """Вернуть соответствующее тегу имя файла.
#
#         >>> HTML.get_tag_filename('планирование')
#         'meta_planirovanie.html'
#         """
#         return 'meta_' + transliterate(tag) + '.html'
#
#     @classmethod
#     def render_tag_graph(cls, tag: str, files: List['MarkdownFile']) -> dict:
#         """Собрать граф для отображения тега.
#         """
#         # FIXME
#         directory = os.path.abspath(os.getcwd()).replace('\\', '/')
#
#         graph = {
#             'nodes': {
#                 'tag': {
#                     'label': tag,
#                     'bg_color': '#04266c',
#                     'link': 'localexplorer:' + directory + '/' + Markdown.get_tag_filename(
#                         tag)
#                 },
#             },
#             'edges': {
#                 'tag': {}
#             }
#         }
#         for i, file in enumerate(files, start=1):
#             num = str(i)
#             graph['nodes'][num] = {
#                 'label': file.title,
#                 'link': 'localexplorer:' + directory + '/' + file.filename
#             }
#             graph['edges']['tag'][num] = {
#                 'weight': 0.1
#             }
#
#         return graph
#
#     @classmethod
#     def render_index_graph(cls, files: List['MarkdownFile']) -> dict:
#         """Собрать граф для отображения стартовой страницы.
#         """
#         # FIXME
#         directory = os.path.abspath(os.getcwd()).replace('\\', '/')
#
#         graph = {
#             'nodes': {},
#             'edges': {}
#         }
#
#         for file in files:
#             graph['nodes'][file.filename] = {
#                 'label': file.title,
#             }
#             for tag in file.tags:
#                 name = transliterate(tag)
#                 graph['nodes'][name] = {
#                     'label': tag,
#                     'bg_color': '#04266c'
#                 }
#
#                 if file.filename not in graph['edges']:
#                     graph['edges'][file.filename] = {name: {'weight': 0.1}}
#                 else:
#                     graph['edges'][file.filename][name] = {'weight': 0.1}
#
#         return graph
#
#     @classmethod
#     def make_metafile_contents(cls, tag: str,
#                                files: List['MarkdownFile']) -> str:
#         """Собрать текст метафайла из исходных данных.
#         """
#         # FIXME
#         template = string.Template(HTML_TEMPLATE)
#         nodes_as_string = json.dumps(
#             cls.render_tag_graph(tag, files),
#             ensure_ascii=False,
#             indent=4
#         )
#         content = template.safe_substitute(
#             {'title': tag, 'nodes': nodes_as_string}
#         )
#         return content
#
#     @classmethod
#     def make_index_contents(cls, files: List['MarkdownFile']) -> str:
#         """Собрать текст стартовой страницы из исходных данных.
#         """
#         # FIXME
#         template = string.Template(HTML_TEMPLATE)
#         nodes_as_string = json.dumps(
#             cls.render_index_graph(files),
#             ensure_ascii=False,
#             indent=4
#         )
#         content = template.safe_substitute({
#             'title': 'Стартовая страница',
#             'nodes': nodes_as_string
#         })
#         return content
#
#
# class Markdown:
#     """Контейнер для инструментов обработки текста в формате markdown.
#
#     TITLE_PATTERN - шаблон заголовка
#         Произвольное количество пробелов от начала строки, за которыми следуют
#         один или несколько октоторпов. Потом идёт обязательный пробел (одно из
#         отличий заголовка от тега), за которым произвольный набор символов
#         до конца строки.
#
#     HEAD_BARE_TAG_PATTERN - шаблон голого тега из заголовка статьи.
#         Это тег, который ещё не был отформатирован пользователем.
#         Строго с начала строки, затем экранированный октоторп и
#         сразу текст без пробела, считываемый до конца строки.
#
#     BODY_BARE_TAG_PATTERN - неотформатированный тег, но уже в теле документа.
#         Мы заведомо не знаем, где кончается текст тега, так что этот
#         шаблон надо по месту достравивать для каждого тега.
#
#     FULL_TAG_PATTERN - отформатированный тег в теле документа.
#         Он уже оформлен в виде гиперссылки.
#     """
#
#     TITLE_PATTERN = re.compile(r"^\s*#+\s(.*)", flags=re.MULTILINE)
#
#     HEAD_BARE_TAG_PATTERN = re.compile(r'^\\#(.*)$', flags=re.MULTILINE)
#     HEAD_BARE_TAG_PATTERN_CUSTOM = r'^\\#{}$'
#     BODY_BARE_TAG_PATTERN_CUSTOM = r'(?<!\[)\\#({})(?!\])'
#
#     FULL_TAG_PATTERN = re.compile(r'\[\\#(.*)\]\(\./(.*.md)\)')
#
#     @staticmethod
#     def href(label: str, link: str) -> str:
#         """Собрать гиперссылку из частей.
#
#         >>> Markdown.href('Hello!', 'world')
#         '[Hello!](./world)'
#         """
#         return '[{}](./{})'.format(label, link)
#
#     @classmethod
#     def get_tag_filename(cls, tag: str) -> str:
#         """Вернуть соответствующее тегу имя файла.
#
#         >>> Markdown.get_tag_filename('планирование')
#         'meta_planirovanie.md'
#         """
#         return 'meta_' + transliterate(tag) + '.md'
#
#     @classmethod
#     def tag2href(cls, tag: str) -> str:
#         """Из текста тега сформировать гиперссылку.
#         """
#         filename = cls.get_tag_filename(tag)
#         href = cls.href('\\#' + tag, filename)
#         return href
#
#     @classmethod
#     def extract_title(cls, content: str) -> str:
#         """Извлечь заголовок из тела документа.
#         """
#         match = cls.TITLE_PATTERN.match(content)
#         if match:
#             return match.groups()[0].strip()
#         return '???'
#
#     @classmethod
#     def extract_tags(cls, content: str) -> Set[str]:
#         """Извлечь все теги из тела документа.
#         """
#         all_tags = set()
#         bare_tags = set()
#
#         for each in cls.HEAD_BARE_TAG_PATTERN.findall(content):
#             bare_tags.add(each)
#             all_tags.add(each)
#
#         for each in bare_tags:
#             sub_pattern = cls.BODY_BARE_TAG_PATTERN_CUSTOM.format(each)
#             for sub_tag in re.findall(sub_pattern, content):
#                 all_tags.add(sub_tag)
#
#         for full_tag in cls.FULL_TAG_PATTERN.finditer(content):
#             tag_text, _ = full_tag.groups()
#             all_tags.add(tag_text)
#
#         return {x.lower().strip() for x in all_tags}
#
#     @classmethod
#     def replace_tags_with_hrefs(cls, content: str, tags: Set[str]) -> str:
#         """Перестроить текст так, чтобы теги стали гиперрсылками.
#         """
#         bare_tags = set()
#
#         for each in cls.HEAD_BARE_TAG_PATTERN.findall(content):
#             bare_tags.add(each)
#             sub_pattern = cls.HEAD_BARE_TAG_PATTERN_CUSTOM.format(each)
#             content = re.sub(sub_pattern, cls.tag2href(each), content)
#
#         for each in tags:
#             sub_pattern = cls.BODY_BARE_TAG_PATTERN_CUSTOM.format(each)
#             content = re.sub(sub_pattern, cls.tag2href(each), content)
#
#         return content
#
#     @classmethod
#     def make_metafile_contents(cls, tag: str,
#                                files: List['MarkdownFile']) -> str:
#         """Собрать текст метафайла из исходных данных.
#         """
#         if not files:
#             return ''
#
#         lines = [
#             '## Все вхождения тега "{}"\n'.format(tag),
#             '---\n'
#         ]
#         total = len(files)
#         digits = len(str(total))
#         prefix = '{{num:0{0}}} из {{total:0{0}d}}'.format(digits)
#
#         for i, file in enumerate(sorted(files), start=1):
#             number = prefix.format(num=i, total=total)
#
#             lines.append('{}. {}\n'.format(
#                 number,
#                 Markdown.href(file.title, file.filename)
#             ))
#
#             lines.append('')
#
#         return '\n'.join(lines)





# class MarkdownFile:
#     """Обёртка для работы с файлами.
#     """
#
#     @cached_property
#     def title(self) -> str:
#         """Извлечь заголовок из тела документа.
#         """
#         return Markdown.extract_title(self.contents)
#
#     @cached_property
#     def tags(self) -> Set[str]:
#         """Извлечь объявленные теги из тела документа.
#         """
#         return Markdown.extract_tags(self.contents)





# def ensure_each_tag_has_metafile(files: List[MarkdownFile]) -> None:
#     """Удостовериться, что для каждого тега есть персональная страничка.
#
#     Вместо проверки правильности, она просто каждый раз создаётся заново.
#     """
#     tags_to_files = defaultdict(list)
#
#     for file in files:
#         for tag in file.tags:
#             tags_to_files[tag].append(file)
#
#     for tag, tag_files in tags_to_files.items():
#         # markdown форма
#         tag_filename_markdown = Markdown.get_tag_filename(tag)
#         contents = Markdown.make_metafile_contents(tag, tag_files)
#         Filesystem.write(tag_filename_markdown, contents)
#
#         # html форма
#         tag_filename_html = HTML.get_tag_filename(tag)
#         contents = HTML.make_metafile_contents(tag, tag_files)
#         Filesystem.write(tag_filename_html, contents)


# def ensure_each_tag_has_link(files: List[MarkdownFile]) -> None:
#     """Удостовериться, что каждый тег является ссылкой, а не текстом.
#     """
#     for file in files:
#         existing_contents = file.contents
#         new_contents = Markdown.replace_tags_with_hrefs(
#             content=existing_contents,
#             tags=file.tags
#         )
#
#         if new_contents != existing_contents:
#             file.contents = new_contents


# def ensure_index_exists(files: List[MarkdownFile]) -> None:
#     """Удостовериться, что у нас есть стартовая страница.
#     """
#     contents = HTML.make_index_contents(files)
#     Filesystem.write('index.html', contents)


def main():
    """Точка входа.
    """
    current_directory = Path().absolute()
    Syntax.announce(f'Анализируем каталог "{current_directory}"')

    files = Filesystem.get_files_of_type(current_directory, 'md', TextFile)
    print(files)
    # ensure_each_tag_has_metafile(files)
    # ensure_each_tag_has_link(files)
    # ensure_index_exists(files)
    #
    # for file in files:
    #     if file.is_changed:
    #         file.save()

    if not files:
        Syntax.announce('Не найдено файлов для обработки.')


if __name__ == '__main__':
    main()
