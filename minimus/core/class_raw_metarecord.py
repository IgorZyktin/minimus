# -*- coding: utf-8 -*-

"""Абстракция исходной записи.

Соответствует файлу созданному пользователем.

Типичный пример:
-------------------------------------------------------------------------------
# Мышь

Маленькое млекопитающее.

{{ 4 лапы }}

{{ серый }}

{{ хвост }}

Живёт почти везде.
-------------------------------------------------------------------------------
"""
from typing import List


class RawMetarecord:
    """Оригинальный файл от пользователя.
    """

    def __init__(self, filename: str, is_changed: bool, title: str,
                 description: str, tags: List[str], body: str) -> None:
        """Инициализировать экземпляр.
        """
        self.filename = filename
        self.is_changed = is_changed
        self.title = title
        self.description = description
        self.category = tags[0] if tags else ''
        self.tags = tags
        self.body = body
