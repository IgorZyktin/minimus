# -*- coding: utf-8 -*-

"""Abstract base renderer.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

from minimus.core.simple_structures import Document


class AbstractRenderer(ABC):
    """Abstract base renderer.
    """

    @abstractmethod
    def extract_features(self, text: str) -> Document:
        """Extract features from raw text."""

    @abstractmethod
    def render_metafile(self, tag: str,
                        corresponding_files: List[Tuple[str, str]],
                        associations: List[str]) -> Tuple[str, str]:
        """Render metainfo file."""

    @abstractmethod
    def render_index(self, category_to_files: Dict[str, List[Tuple[str, str]]],
                     root: str = '') -> str:
        """Render index file."""
