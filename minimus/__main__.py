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
            print(f'\tТеги не менялись: {each_file.relative_path}')
        else:
            new_content = markup.replace_bare_tags(each_file.content)

            if new_content != each_file.content:
                each_file.content = new_content
                each_file.save()
                print(f'\t+++ Сохранён: {each_file.relative_path}')
            else:
                print(f'\tТеги не менялись: {each_file.relative_path}')

        cache.store_file(each_file)

    output.header('Сохранение тегов')
    storage.ensure_folder_for_tags(path)
    for tag, sub_files in gathered_tags.items():
        filename = markup.get_tag_filename(tag)
        sub_files = sorted(sub_files, key=lambda file: file.path.name)
        tag_content = markup.make_tag_content(tag, sub_files, neighbours)
        tag_path = path / constants.TAGS_FOLDER / filename
        tag = objects.File(path=tag_path, content=tag_content)
        tag.save()
    print(f'\tСохранено тегов: {len(gathered_tags)} шт. ')

    output.header('Генерация вспомогательных файлов')
    readme_content = markup.make_readme_content(files)
    readme_path = path / constants.README_FILENAME
    readme = objects.File(path=readme_path, content=readme_content)
    readme.save()
    print(f'\tСохранён: {readme_path.absolute()}')

    cache_path = cache.save()
    print(f'\tСохранён: {cache_path.absolute()}')

    output.complete(time.perf_counter() - start_time)


if __name__ == '__main__':
    main()
