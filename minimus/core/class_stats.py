from collections import defaultdict
from typing import Dict

from minimus.core.class_document import Document


class Stats:

    def __init__(self) -> None:
        """Initialize instance."""
        self._storage: Dict[str, Document] = {}
        self.category_to_files = defaultdict(list)
        self.tags_to_files = defaultdict(list)
        self.associated_tags = defaultdict(list)

    def add_document(self, filename: str, document: Document) -> None:
        self._storage[filename] = document

        for tag in document.tags:
            self.tags_to_files[tag].append((filename, document.header))
            self.associated_tags[tag].extend(document.tags)

        if document.category:
            self.category_to_files[document.category].append((filename,
                                                              document.header))
