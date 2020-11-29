# -*- coding: utf-8 -*-

"""Представление графа.
"""
from typing import Dict


class Graph:
    """Представление графа.

    Будучи полностью собранным, выглядит примерно вот так:
    {
        "nodes": {
            "tag": {
                "label": "Все вхождения тега \"4 лапы\"",
                "bg_color": "#04266c",
                "filename": "meta_4_lapy.html"
            },
            "slon": {
                "label": "Слон",
                "bg_color": "#5a0000",
            },
            "mysh": {
                "label": "Мышь",
                "bg_color": "#5a0000",
            }
        },
        "edges": {
            "tag": {
                "slon": {
                    "weight": 1.0,
                    "color": "#000000"
                },
                "mysh": {
                    "weight": 1.0,
                    "color": "#000000"
                }
            }
        }
    };
    """

    def __init__(self):
        """Инициализировать экземпляр.
        """
        self.nodes: Dict[str, dict] = {}
        self.edges = {}

    def add_node(self, name: str, label: str,
                 bg_color: str, link: str, **kwargs) -> None:
        """Добавить ноду в граф.
        """
        existing = self.nodes.get(name, {})

        self.nodes[name] = {
            'label': label,
            'bg_color': bg_color,
            'link': link,
            **kwargs,
            **existing,
        }

    def add_edge(self, node_start: str, node_finish: str,
                 weight: float = 1.0) -> None:
        """Добавить грань в граф.
        """
        if node_start not in self.edges:
            self.edges[node_start] = {}

        self.edges[node_start][node_finish] = {
            'weight': weight,
            'color': '#000000',
        }

    def as_dict(self) -> dict:
        """Вернуть граф в форме словаря.
        """
        return {
            'nodes': self.nodes,
            'edges': self.edges,
        }
