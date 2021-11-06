# -*- coding: utf-8 -*-

"""Основной модуль.
"""

import time

import click
from colorama import init

from minimus import output
from minimus import render
from minimus import storage
from minimus import parse

init(autoreset=True)


@click.command()
@click.option('--source',
              required=True,
              help='Каталог с исходными материалами')
@click.option('--target',
              required=True,
              help='Каталог для сохранения обработанных материалов')
@click.option('--force-notes/--no-force-notes',
              default=False,
              help='Принудительно перезаписывать '
                   'файлы заметок даже если они не обновлялись')
@click.option('--force-media/--no-force-media',
              default=False,
              help='Принудительно перезаписывать '
                   'файлы данных даже если они не обновлялись')
def main(source: str, target: str, force_notes: bool, force_media: bool):
    """Точка входа.
    """
    start_time = time.monotonic()
    output.greeting_message()

    source, target = storage.validate_setup(source, target)
    output.setup(source, target, force_notes, force_media)

    cache = storage.gather_cache(source)

    pointers = storage.gather_pointers(source)
    pointers = storage.skip_private_files(pointers)
    notes, media = storage.split_pointers(pointers)

    output.header('Сохранение заметок')
    notes_with_text = storage.load_text(notes)
    documents = parse.make_documents(notes_with_text)
    correspondence = render.make_correspondence(documents)
    render.update_all_documents(documents)
    storage.save_documents(target, documents, cache, force_notes)

    output.header('Генерация вспомогательных файлов')
    tags = render.make_tags(correspondence)
    storage.save_tags(target, tags)
    readme = render.make_readme(documents)
    storage.save_readme(target, readme)

    output.header('Сохранение прочих файлов')
    storage.copy_media(target, media, cache, force_media)
    storage.save_cache(source, cache)

    warnings = parse.extract_warnings(documents)
    if warnings:
        output.header('К исходникам есть замечания')
        output.warnings(warnings)

    output.final_message(time.monotonic() - start_time)


if __name__ == '__main__':
    main()  # pragma: no cover
