# -*- coding: utf-8 -*-

"""Абстракция файла.

Не занимается работой с файловой системой, берёт на себя только
логику отслеживания изменений.
"""
from functools import cached_property
from typing import Optional

from minimus.components.class_meta import Meta
from minimus.components.class_renderer import Renderer
from minimus.utils.filesystem import get_ext


class File:
    """Абстракция файла.
    """

    def __init__(self, meta: Meta, stored_meta: Optional[Meta]) -> None:
        """Инициализировать экземпляр.
        """
        self.meta = meta
        self.stored_meta = stored_meta
        self.renderer: Optional[Renderer] = None

    def __repr__(self):
        """Вернуть текстовое представление.
        """
        return f'{type(self).__name__}({self.meta.filename})'

    @cached_property
    def is_markdown(self) -> bool:
        """Вернуть True если это markdown файл.
        """
        return (not self.is_metafile and
                get_ext(self.meta.original_filename) == 'md')

    @cached_property
    def is_updated(self) -> bool:
        """Вернуть True если файл изменился с прошлого запуска скрипта.
        """
        return self.meta != self.stored_meta

    @cached_property
    def is_metafile(self) -> bool:
        """Вернуть True если является вспомогательным и не должен копироваться.
        """
        return self.meta.filename.startswith('meta')
