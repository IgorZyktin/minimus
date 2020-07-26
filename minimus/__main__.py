# -*- coding: utf-8 -*-

"""Головной файл проекта.
"""
import argparse
import sys

from minimus.file_system import FileSystem
from minimus.config import Config
from minimus.syntax import Syntax


def init():
    """Подготовить параметры перед запуском.
    """
    parser = argparse.ArgumentParser(description='Параметры сшивки заметок')

    parser.add_argument('--source_directory', action='store',
                        help='Каталог с исходными данными')
    parser.add_argument('--target_directory', action='store',
                        help='Каталог для обработанных данных')
    parser.add_argument('--localexplorer', action='store_true',
                        help='Пытаться открывать файлы через '
                             'стандартное приложение, а не барузер?')

    args = parser.parse_args()
    config = Config()
    config.launch_directory = Path()
    Syntax.announce('-' * 79)
    Syntax.announce('Скрипт запущен в каталоге {}.'
                    .format(FileSystem.cast_path(Config.launch_directory)))

    Config.script_directory = Config.launch_directory / 'minimus'
    if not Config.script_directory.exists():
        Syntax.announce('Не удаётся найти каталог с библиотеками: {}'
                        .format(FileSystem.cast_path(Config.script_directory)))
        sys.exit()

    if args.source_directory is None:
        Config.source_directory = Config.launch_directory / 'source'

    else:
        other_dir = Path(args.source_directory).absolute()

        if not other_dir.exists():
            Syntax.announce('Не удаётся найти каталог исходных данных: {}'
                            .format(FileSystem.cast_path(other_dir)))
            sys.exit()

        Config.source_directory = other_dir

    Syntax.announce('Каталог исходных данных: {}.'
                    .format(FileSystem.cast_path(Config.source_directory)))

    if args.target_directory is None:
        Config.target_directory = Config.launch_directory / 'target'

    else:
        other_dir = Path(args.target_directory).absolute()
        FileSystem.ensure_folder_exists(other_dir)
        Config.target_directory = other_dir

    Syntax.announce('Каталог обработанных данных: {}.'
                    .format(FileSystem.cast_path(Config.target_directory)))

    if args.localexplorer:
        Config.protocol = 'localexplorer:'
        Syntax.announce('Сборка будет произведена со '
                        'стилем ссылок Local Explorer.')

    main()


def main():
    """Точка входа.
    """
    files = FileSystem.get_files_of_type(
        Config.source_directory, 'md', TextFile
    )
    tags_to_files = map_tags_to_files(files)

    Syntax.announce('\nЭтап 1. Генерация метафайлов.')
    ensure_each_tag_has_metafile(tags_to_files)

    Syntax.announce('\nЭтап 2. Генерация гиперссылок.')
    ensure_each_tag_has_link(files)

    Syntax.announce('\nЭтап 3. Генерация индексов.')
    ensure_index_exists(files)

    Syntax.announce('\nЭтап 4. Сохранение основных файлов.')
    for number, file in Syntax.numerate(files):
        name = Config.target_directory / file.filename
        if FileSystem.write(name, file.contents):
            Syntax.announce(f'\t{number}. Сохранены изменения'
                            f' в файле "{name.absolute()}"')

    if not files:
        Syntax.announce('Не найдено файлов для обработки.')

    Syntax.announce('\nЭтап 5. Копирование библиотек.')
    js_files = [
        x for x in Config.script_directory.iterdir()
        if x.suffix == '.js'
    ]
    Syntax.announce(f'Был создан каталог "{path}"')
    for number, file in Syntax.numerate(js_files):
        if file.suffix == '.js':
            FileSystem.copy(
                file.absolute(),
                Config.target_directory.absolute() / file.name,
            )
            Syntax.announce(f'\t{number}. Скопирован файл "{file.absolute()}"')


if __name__ == '__main__':
    init()  # pragma: no cover
