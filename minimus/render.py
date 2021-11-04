# -*- coding: utf-8 -*-

"""Модуль генерации текста.
"""
from minimus import objects, utils


def update_all_documents(documents: list[objects.Document]) -> None:
    """Обновить атрибут документа поместив туда обработанный вариант."""
    for document in documents:
        document.rendered = render_document(document)


def render_document(document: objects.Document) -> str:
    """Преобразовать документ в формат markdown."""
    return '\n'.join([
        f'# {document.title}\n',
        document.header,
        '\n---\n',
        render_tags(document),
        '\n---\n',
        document.body,
    ]) + '\n'


def render_tags(document: objects.Document) -> str:
    """Преобразовать список тегов в формат markdown."""
    tags = []
    for tag in document.tags:
        link = link_for_tag(tag, document.pointer.steps)
        tags.append(f'- [{tag}]({link})')
    return '\n'.join(['Теги:\n', *tags])


def make_correspondence(documents: list[objects.Document]
                        ) -> objects.Correspondence:
    """Собрать соответствие тегов и документов."""
    correspondence = objects.Correspondence()

    for document in documents:
        for tag in document.tags:
            correspondence.add_tag(tag, document)

    return correspondence


def render_tag_document(tag: str, documents: list[objects.Document],
                        correspondence: objects.Correspondence) -> str:
    """Собрать документ для описания тега."""
    lines = [f'## Тег "{tag}" применён в:\n']

    gen = sorted(documents, key=lambda x: x.title)

    for number, document in utils.numerate(gen):
        link = '/'.join([*document.pointer.steps[1:],
                         document.pointer.filename])
        link = escape(link)
        new_line = f'{number}. [{document.title}](../{link})\n'
        lines.append(new_line)

    tags = correspondence.tags_to_tags.get((tag, tag.casefold()))
    if tags:
        lines.append('## Близкие теги:\n')
        tags = sorted(tags)

        for number, tag in utils.numerate(tags):
            link = escape(as_filename(tag))
            new_line = f'{number}. [{tag}](./{link})\n'
            lines.append(new_line)

    return '\n'.join(lines) + '\n'


def make_tags(correspondence: objects.Correspondence) -> list[objects.Tag]:
    """Собрать экземпляр отрендеренных тегов."""
    tags = []

    gen = [
        (tag, documents)
        for (tag, _), documents in correspondence.tags_to_documents.items()
    ]
    gen.sort(key=lambda x: x[0])

    for tag, documents in gen:
        new_tag = objects.Tag(
            title=tag,
            filename=as_filename(tag),
            rendered=render_tag_document(tag, documents, correspondence),
        )
        tags.append(new_tag)

    return tags


def escape(link: str) -> str:
    """Заменить спецсимволы для гиперссылки."""
    return link \
        .replace(' ', '%20') \
        .replace('+', '%2B')


def as_filename(title: str) -> str:
    """Сгенерировать имя файла."""
    return f'{title}.md'


def link_for_tag(tag: str, steps: tuple[str, ...]) -> str:
    """Сгенерировать безопасную ссылку для тега."""
    up = ['..'] * len(steps[1:])
    up_text = '/'.join(up)
    tag = as_filename(escape(tag))

    if up_text:
        return f'{up_text}/_tags/{tag}'
    return f'_tags/{tag}'
