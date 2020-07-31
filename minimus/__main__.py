# -*- coding: utf-8 -*-

"""Головной файл проекта.
"""
import argparse
import sys
from pathlib import Path

from minimus.config import Config
from minimus.file_system import FileSystem
from minimus.processing import (
    map_tags_to_files, ensure_each_tag_has_metafile,
    ensure_each_tag_has_link, ensure_index_exists,
)
from minimus.syntax import Syntax
from minimus.text_file import TextFile


def init():
    """Подготовить параметры перед запуском.
    """
    parser = argparse.ArgumentParser(description='Parameters of sewing')

    parser.add_argument('--lang',
                        action='store',
                        default='RU',
                        choices=['EN', 'RU'],
                        help='Which language to use')

    parser.add_argument('--source_directory',
                        action='store',
                        help='Where to get source files')

    parser.add_argument('--target_directory',
                        action='store',
                        help='Where to save resulting files')

    parser.add_argument('--localexplorer',
                        action='store_true',
                        help='Generate links that are supposed to be '
                             'opened in explorer rather than browser?')

    args = parser.parse_args()

    config = Config()
    config.lang = args.lang
    FileSystem.set_config(config)
    Syntax.set_config(config)

    terminal_width = 79
    Syntax.stdout('-' * terminal_width)
    Syntax.stdout('Script has been started at folder: {folder}',
                  folder=FileSystem.cast_path(config.launch_directory))

    config.script_directory = config.launch_directory / 'minimus'
    if not config.script_directory.exists():
        Syntax.stdout('Unable to find folder with libraries: {folder}',
                      folder=FileSystem.cast_path(config.script_directory))
        sys.exit()

    if args.source_directory is None:
        config.source_directory = config.launch_directory / 'source'

    else:
        other_dir = Path(args.source_directory).absolute()

        if not other_dir.exists():
            Syntax.stdout('Unable to find folder with '
                          'source files: {folder}',
                          folder=FileSystem.cast_path(other_dir))
            sys.exit()

        config.source_directory = other_dir

    Syntax.stdout('Source files folder: {folder}',
                  folder=FileSystem.cast_path(config.source_directory))

    path = config.script_directory / 'template.html'
    try:
        with open(str(path.absolute()), mode='r', encoding='utf-8') as file:
            config.html_template = file.read()
    except FileNotFoundError:
        Syntax.stdout('Cannot find HTML template: {path}',
                      path=FileSystem.cast_path(path))
        sys.exit()

    if args.target_directory is None:
        config.target_directory = config.launch_directory / 'target'

    else:
        other_dir = Path(args.target_directory).absolute()
        config.target_directory = other_dir

    FileSystem.ensure_folder_exists(config.target_directory)
    Syntax.stdout('Output files folder: {folder}',
                  folder=FileSystem.cast_path(config.target_directory))

    if args.localexplorer:
        config.protocol = 'localexplorer:'
        Syntax.stdout('The assembly will be done using '
                      + 'the Local Explorer links style')

    main(config)


def main(config: Config):
    """Точка входа.
    """
    files = FileSystem.get_files_of_type(
        config.source_directory, 'md', TextFile
    )
    tags_to_files = map_tags_to_files(files)

    Syntax.stdout('\nStage 1. Metafile generation')
    ensure_each_tag_has_metafile(config, tags_to_files)

    Syntax.stdout('\nStage 2. Hyperlinks generation')
    ensure_each_tag_has_link(files)

    Syntax.stdout('\nStage 3. Indexes generation')
    ensure_index_exists(config, files)

    Syntax.stdout('\nStage 4. Main files saving')
    for number, file in Syntax.numerate(files):
        name = config.target_directory / file.filename
        if FileSystem.write(name, file.content):
            Syntax.stdout('\t{number}. Saved changes to the file {filename}',
                          number=number, filename=name.absolute())

    non_md = [
        x for x in config.source_directory.iterdir()
        if x.suffix.lower() != '.md'
    ]
    Syntax.stdout('\nStage 5. Additional files saving')
    for number, file in Syntax.numerate(non_md):
        FileSystem.copy(
            file.absolute(),
            config.target_directory.absolute() / file.name,
        )
        Syntax.stdout('\t{number} File has been copied: {filename}',
                      number=number, filename=file.absolute())

    if not files:
        Syntax.stdout('No source files found to work with')
        sys.exit()

    Syntax.stdout('\nStage 6. Libraries copying')
    js_files = [
        x for x in config.script_directory.iterdir()
        if x.suffix == '.js'
    ]

    for number, file in Syntax.numerate(js_files):
        if file.suffix == '.js':
            FileSystem.copy(
                file.absolute(),
                config.target_directory.absolute() / file.name,
            )
            Syntax.stdout('\t{number} File has been copied: {filename}',
                          number=number, filename=file.absolute())


if __name__ == '__main__':
    init()  # pragma: no cover
