"""Основной модуль.
"""
import time

from minimus import markup
from minimus import output
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
    files.sort(key=lambda file: file.path.name)

    gathered_tags, neighbours = markup.gather_tags_from_files(files)

    if gathered_tags:
        output.header('Сохранение заметок')
        for each_file in files:
            cache[str(each_file.path)] = each_file.fingerprint
            # TODO

        output.header('Сохранение тегов')
        storage.ensure_folder_for_tags(path)
        for tag, sub_files in gathered_tags.items():
            filename = markup.get_tag_filename(tag)
            sub_files = sorted(sub_files, key=lambda file: file.path.name)
            content = markup.render_tag(tag, sub_files, neighbours)
            storage.save_tag(path, filename, content)
        print(f'\tСохранено {len(gathered_tags)} шт. тегов')

        output.header('Генерация вспомогательных файлов')
        readme = markup.make_readme(files)
        readme_path = storage.save_readme(path, readme)
        print(f'\tСохранён {readme_path.absolute()}')

        cache_path = storage.save_cache(path, cache)
        print(f'\tСохранён кеш {cache_path.absolute()}')

    output.complete(time.perf_counter() - start_time)


if __name__ == '__main__':
    main()
