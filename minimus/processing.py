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
        Syntax.announce(f'\t{number}. Создан файл "{name.absolute()}"')
        i += 1

        # html форма
        name = Config.target_directory / HTMLSyntax.get_tag_filename(tag)
        contents = HTMLSyntax.make_metafile_contents(tag, tag_files)
        Filesystem.write(name, contents)
        number = prefix.format(num=i, total=total)
        Syntax.announce(f'\t{number}. Создан файл "{name.absolute()}"')
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
        Syntax.announce(f'\tСоздан файл "{name.absolute()}"')

    # html форма
    name = Config.target_directory / HTMLSyntax.get_index_filename()
    contents = HTMLSyntax.make_index_contents(files)
    if Filesystem.write(name, contents):
        Syntax.announce(f'\tСоздан файл "{name.absolute()}"')


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

