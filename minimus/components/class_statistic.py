# -*- coding: utf-8 -*-

"""Обёртка для работы с os.stat.
"""
from dataclasses import dataclass
from typing import Dict


@dataclass(eq=True, frozen=True)
class Statistic:
    """Перечень сведений о файле, нужен для обнаружения факта изменения.
    """
    created_at: int
    modified_at: int
    size: int

    def to_dict(self) -> Dict[str, int]:
        """Разложить экземпляр в словарь.
        """
        return {
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'size': self.size,
        }

    @classmethod
    def from_dict(cls, given_dict: dict):
        """Собрать экземпляр из словаря.
        """
        return cls(**given_dict)
