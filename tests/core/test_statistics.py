# -*- coding: utf-8 -*-

"""Tests.
"""

from minimus.core.class_statistics import Statistics


def test_add(document1):
    """Must store changes."""
    inst = Statistics()
    assert not inst.get_tags_to_files()

    inst.add_document('test', document1)
    assert inst.get_tags_to_files()


def test_add_empty(document1):
    """Must not store changes."""
    inst = Statistics()
    document1.category = ''
    inst.add_document('test', document1)
    assert not inst.get_categories_to_files()


def test_get_tags_to_files(document1, document2, ref_tags_to_files):
    """Must save corresponding names."""
    inst = Statistics()
    inst.add_document('doc1.md', document1)
    inst.add_document('doc2.md', document2)
    assert inst.get_tags_to_files() == ref_tags_to_files


def test_get_categories_to_files(document1, document2, ref_cats_to_files):
    """Must group by category."""
    inst = Statistics()
    inst.add_document('doc1.md', document1)
    inst.add_document('doc2.md', document2)
    assert inst.get_categories_to_files() == ref_cats_to_files


def test_get_associated_tags(document1, document2, ref_associated_tags):
    """Must combine tags from different files."""
    inst = Statistics()
    inst.add_document('doc1.md', document1)
    inst.add_document('doc2.md', document2)
    assert inst.get_associated_tags() == ref_associated_tags
