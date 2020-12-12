# -*- coding: utf-8 -*-

"""Контейнер с метаинформацией о файле.
"""
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, Any

from minimus.components.class_statistic import Statistic
from minimus.utils.output_processing import transliterate


@dataclass(eq=True, frozen=True)
class Meta:
    """Контейнер с метаинформацией о файле.
    """
    original_filename: str
    original_path: str
    statistic: Statistic

    def __repr__(self):
        """Вернуть текстовое представление.
        """
        return f'{type(self).__name__}(<{self.original_filename}>)'

    @cached_property
    def filename(self) -> str:
        """Вернуть оптимизированное имя файла.
        """
        return transliterate(self.original_filename)

    def to_dict(self) -> Dict[str, Any]:
        """Разложить экземпляр в словарь.
        """
        return {
            'original_filename': self.original_filename,
            'original_path': self.original_path,
            'statistic': self.statistic.to_dict(),
        }

    @classmethod
    def from_dict(cls, given_dict: dict):
        """Собрать экземпляр из словаря.
        """
        return cls(
            original_filename=given_dict['original_filename'],
            original_path=given_dict['original_path'],
            statistic=Statistic.from_dict(given_dict['statistic'])
        )
