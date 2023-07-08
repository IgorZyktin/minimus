"""Основной модуль.
"""
import time

from minimus.src import constants
from minimus.src import markup
from minimus.src import objects
from minimus.src import output
from minimus.src import storage


def main() -> None:
    """Точка входа.
    """
    start_time = time.perf_counter()

    path = storage.get_path()
    output.greet()
    output.print_path(path)

    cache = objects.Cache(path=path, contents={})
    cache.load()

    files = storage.get_files(path)
    files.sort(key=lambda file: file.path)

    gathered_tags, neighbours = markup.gather_tags_from_files(files)

    if not gathered_tags:
        output.header(f'В каталоге {path.absolute()} заметок не найдено')
        return

    output.header('Сохранение заметок')
    for each_file in files:
        if cache.has_no_changes(each_file):
            print(f'\tБез изменений: {each_file.relative_path}')
        else:
            # TODO - тут мы меняем теги в файле
            pass

        cache.store_file(each_file)

    output.header('Сохранение тегов')
    storage.ensure_folder_for_tags(path)
    for tag, sub_files in gathered_tags.items():
        filename = markup.get_tag_filename(tag)
        sub_files = sorted(sub_files, key=lambda file: file.path.name)
        content = markup.render_tag(tag, sub_files, neighbours)
        storage.save_tag(path, filename, content)
    print(f'\tСохранено тегов: {len(gathered_tags)} шт. ')

    output.header('Генерация вспомогательных файлов')
    readme_content = markup.make_readme(files)
    readme_path = path / constants.README_FILENAME
    readme = objects.File(path=readme_path, content=readme_content)
    readme.save()
    print(f'\tСохранён: {readme_path.absolute()}')

    cache_path = cache.save()
    print(f'\tСохранён: {cache_path.absolute()}')

    output.complete(time.perf_counter() - start_time)


if __name__ == '__main__':
    main()
