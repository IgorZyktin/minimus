# -*- coding: utf-8 -*-

"""Набор абстрактных базовых классов для проекта.
"""
from abc import abstractmethod, ABC
from typing import List, Optional


class AbstractTextFile(ABC):
    """Абстрактный текстовый файл.
    """

    @abstractmethod
    def __getattr__(self, item):
        """Текстовый файл должен иметь и произвольные атрибуты тоже.
        """

    @property
    @abstractmethod
    def filename(self) -> str:
        """Вернуть соответствующее документу имя файла.
        """

    @property
    @abstractmethod
    def content(self) -> str:
        """Вернуть скомпонованный текст документа.
        """


class AbstractDocument(ABC):
    """Абстрактный документ.
    """

    BASE_TEMPLATE = ''

    def __init__(self,
                 title: str,
                 files: List[AbstractTextFile],
                 template: Optional[str] = None):
        """Инициализировать экземпляр.
        """
        self.files = files
        self.given_title = title
        self.given_template = template

    @property
    def template(self) -> str:
        """Вернуть шаблон, на котором строится этот документ.
        """
        if self.given_template is None:
            return type(self).BASE_TEMPLATE
        return self.given_template

    @property
    def title(self) -> str:
        """Вернуть заголовок документа.
        """
        return self.given_title

    @property
    def corresponding_filename(self) -> str:
        """Вернуть соответствующее имя для файла.
        """
        return self.make_corresponding_filename(self.given_title)

    @property
    @abstractmethod
    def content(self) -> str:
        """Вернуть скомпонованный текст документа.
        """

    @classmethod
    @abstractmethod
    def make_corresponding_filename(cls, title: str) -> str:
        """Вернуть соответствующее документу имя файла.
        """
