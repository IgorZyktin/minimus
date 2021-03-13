from collections import defaultdict
from typing import Dict

from minimus.core.class_document import Document


class Stats:

    def __init__(self) -> None:
        """Initialize instance."""
        self._storage: Dict[str, Document] = {}
        self.tags_to_files = defaultdict(list)
        self.associated_tags = defaultdict(list)

    def add_document(self, key: str, document: Document) -> None:
        self._storage[key] = document

        for tag in document.tags:
            self.tags_to_files[tag].append(key)
            self.associated_tags[tag].extend(document.tags)
