# -*- coding: utf-8 -*-

"""Tests.
"""
import os
import tempfile
from unittest.mock import patch

import pytest

from minimus.__main__ import main
from minimus.core.class_filesystem import Filesystem


@pytest.fixture()
def ref_text1():
    return """
# Header for the first file

[tag1](./meta_tag1.md)
[tag2](./meta_tag2.md)

Some content.
    """.strip()


@pytest.fixture()
def ref_text2():
    return """
# Other header

[tag1](./meta_tag1.md)
[tag2](./meta_tag2.md)

Some other content.
    """.strip()


@pytest.fixture()
def ref_text3():
    return """
## All occurrences of the tag "tag1"


1 of 2. [Header for the first file](./file1.md)

2 of 2. [Other header](./file2.md)



### This tag occurs with


1 of 1. [tag2](./meta_tag2.md)
    """.strip() + '\n\n'


@pytest.fixture()
def ref_text4():
    return """
## All occurrences of the tag "tag2"


1 of 2. [Header for the first file](./file1.md)

2 of 2. [Other header](./file2.md)



### This tag occurs with


1 of 1. [tag1](./meta_tag1.md)
    """.strip() + '\n\n'


@pytest.fixture()
def ref_text5():
    return """
# All entries


1 of 1. [Tag1](./meta_tag1.md)

* [Header for the first file](./file1.md)

* [Other header](./file2.md)
    """.strip() + '\n\n'


@pytest.fixture()
def ref_text6():
    return """
# All entries


1 of 1. [Tag1](./content/meta_tag1.md)

* [Header for the first file](./content/file1.md)

* [Other header](./content/file2.md)
    """.strip() + '\n\n'


def _init_directory(path: str) -> tuple:
    """Create all required resources."""
    source = os.path.join(path, 'source')
    os.mkdir(source)

    readme = os.path.join(path, 'target')
    os.mkdir(readme)

    target = os.path.join(path, 'target', 'content')
    os.mkdir(target)

    filesystem = Filesystem(source, target, readme)
    _init_files(filesystem)

    return source, target, readme, filesystem


def _init_files(filesystem: Filesystem) -> None:
    path1 = filesystem.at_source('file1.md')
    filesystem.write_file(path1, """
# Header for the first file

{{ tag1 }}
{{ tag2 }}

Some content.
    """.strip())

    path2 = filesystem.at_source('file2.md')
    filesystem.write_file(path2, """
# Other header

{{ tag1 }}
{{ tag2 }}

Some other content.
    """.strip())


def test_integration(ref_text1, ref_text2, ref_text3,
                     ref_text4, ref_text5, ref_text6):
    """Must go the whole path."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        source, target, readme, filesystem = _init_directory(tmp_dir)
        with patch('minimus.__main__.sys') as fake_sys, \
                patch('minimus.output.stdout'), \
                patch('minimus.core.class_file_repository.stdout'), \
                patch('minimus.utils.utils_auto.stdout'):
            fake_sys.argv = [
                '',
                '--language', 'EN',
                '--source_directory', source,
                '--target_directory', target,
                '--readme_directory', readme,
            ]
            main()

        cont1 = filesystem.read_file(filesystem.at_target('file1.md'))
        cont2 = filesystem.read_file(filesystem.at_target('file2.md'))
        cont3 = filesystem.read_file(filesystem.at_target('meta_tag1.md'))
        cont4 = filesystem.read_file(filesystem.at_target('meta_tag2.md'))
        cont5 = filesystem.read_file(filesystem.at_target('index.md'))
        cont6 = filesystem.read_file(filesystem.at_readme('README.md'))

        assert cont1 == ref_text1
        assert cont2 == ref_text2
        assert cont3 == ref_text3
        assert cont4 == ref_text4
        assert cont5 == ref_text5
        assert cont6 == ref_text6


def test_integration_from_nothing():
    """Must go the whole path, but there are no source files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        source = os.path.join(tmp_dir, 'source')
        readme = os.path.join(tmp_dir, 'target')
        target = os.path.join(tmp_dir, 'target', 'content')

        with patch('minimus.__main__.sys') as fake_sys, \
                patch('minimus.output.stdout'), \
                patch('minimus.core.class_file_repository.stdout'), \
                patch('minimus.core.class_filesystem.stdout'), \
                patch('minimus.utils.utils_auto.stdout'):
            fake_sys.argv = [
                '',
                '--language', 'EN',
                '--source_directory', source,
                '--target_directory', target,
                '--readme_directory', readme,
            ]
            main()
