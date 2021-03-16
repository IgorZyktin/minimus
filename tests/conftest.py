# -*- coding: utf-8 -*-

"""Tests.
"""
from unittest.mock import Mock

import pytest

from minimus.core.class_file_repository import FileRepository
from minimus.core.class_filesystem import Filesystem
from minimus.core.simple_structures import Document, File


@pytest.fixture()
def document1():
    return Document(
        header='zebra',
        tags=['one', 'two'],
        content='wtf1',
        category='wine',
    )


@pytest.fixture()
def document2():
    return Document(
        header='alpaca',
        tags=['one', 'two'],
        content='wtf2',
        category='chocolate',
    )


@pytest.fixture()
def ref_tags_to_files():
    return {
        'one': [('doc2.md', 'alpaca'), ('doc1.md', 'zebra')],
        'two': [('doc2.md', 'alpaca'), ('doc1.md', 'zebra')]
    }


@pytest.fixture()
def ref_cats_to_files():
    return {
        'chocolate': [('doc2.md', 'alpaca')],
        'wine': [('doc1.md', 'zebra')],
    }


@pytest.fixture()
def ref_associated_tags():
    return {
        'one': ['one', 'two'],
        'two': ['one', 'two']
    }


@pytest.fixture()
def filesystem():
    return Filesystem(
        source_directory='source',
        target_directory='target',
        readme_directory='readme',
    )


@pytest.fixture()
def ref_files_in_repo():
    return [
        File(directory='folder1', filename='somefile1.md', content='{}',
             is_markdown=True, is_new=False),
        File(directory='folder1', filename='somefile2.md', content='{}',
             is_markdown=True, is_new=False),
        File(directory='folder1', filename='somefile3.md', content='{}',
             is_markdown=True, is_new=False),
    ]


@pytest.fixture()
def ref_upd_files_in_repo():
    return [
        File(directory='folder1', filename='somefile1.md', content='wtf',
             is_markdown=True, is_new=False),
        File(directory='folder1', filename='somefile2.md', content='wtf',
             is_markdown=True, is_new=False),
        File(directory='folder1', filename='somefile3.md', content='wtf',
             is_markdown=True, is_new=False)
    ]


@pytest.fixture()
def repository_real_fs(filesystem):
    return FileRepository(filesystem)


@pytest.fixture()
def repository():
    fake_filesystem = Mock()
    fake_filesystem.read_file.return_value = '{}'
    fake_filesystem.get_stats_for_file.return_value = {}
    fake_filesystem.at_source.return_value = 'src'

    fake_filesystem.iterate_on_unique_filenames.return_value = [
        ('folder1', 'meta.json'),
        ('folder1', 'somefile1.md'),
        ('folder1', 'somefile2.md'),
        ('folder1', 'somefile3.md'),

    ]
    return FileRepository(fake_filesystem)


class FakeRenderer:
    count = 0

    def extract_features(self, *args):
        self.count += 1
        return Document(str(self.count), ['a', 'b'], 'wtf', 'null')
