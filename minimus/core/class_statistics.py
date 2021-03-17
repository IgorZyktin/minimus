# -*- coding: utf-8 -*-

"""Statistics, that help tie files together.
"""
from collections import defaultdict
from typing import Dict, List, Tuple

from minimus.core.simple_structures import Document

MapTuples = Dict[str, List[Tuple[str, str]]]


class Statistics:
    """Statistics, that help tie files together.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        self._category_to_files: MapTuples = defaultdict(list)
        self._tags_to_files: MapTuples = defaultdict(list)
        self._associated_tags: Dict[str, List[str]] = defaultdict(list)

    def add_document(self, filename: str, document: Document) -> None:
        """Analyze document components."""
        for tag in document.tags:
            self._tags_to_files[tag].append((filename, document.header))
            self._associated_tags[tag].extend(document.tags)

        if document.category:
            element = (filename, document.header)
            self._category_to_files[document.category].append(element)

    def get_tags_to_files(self) -> MapTuples:
        """Safely get attribute."""
        return {
            key: sorted(value, key=lambda x: x[1])
            for key, value in sorted(
                self._tags_to_files.items(), key=lambda x: x[0]
            )
        }

    def get_categories_to_files(self) -> MapTuples:
        """Safely get attribute."""
        return {
            key: sorted(value, key=lambda x: x[1])
            for key, value in sorted(
                self._category_to_files.items(), key=lambda x: x[0]
            )
        }

    def get_associated_tags(self) -> Dict[str, List[str]]:
        """Safely get attribute."""
        return {
            key: sorted(set(value))
            for key, value in sorted(
                self._associated_tags.items(), key=lambda x: x[0]
            )
        }
