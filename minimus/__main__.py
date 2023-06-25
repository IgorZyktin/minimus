"""Основной модуль.
"""

import time

from minimus import output
from minimus import render
from minimus import storage


def main() -> None:
    """Точка входа.
    """
    start_time = time.perf_counter()

    output.greet()
    path = storage.get_path()
    cache = storage.get_cache(path)

    output.print_path(path)
    files = storage.get_files(path)

    output.header('Сохранение заметок')
    found_tags = {}
    for file in files:
        raw_tags = render.get_tags(file)
        found_tags[file] = raw_tags

    output.header('Генерация вспомогательных файлов')
    tags = render.make_tags(found_tags)
    storage.save_tags(path, tags)

    readme = render.make_readme(documents)
    readme_path = storage.save_readme(path, readme)
    print(f'\tСохранён {readme_path.absolute()}')

    cache_path = storage.save_cache(path, cache)
    print(f'\tСохранён {cache_path.absolute()}')

    output.complete(time.perf_counter() - start_time)


if __name__ == '__main__':
    main()
