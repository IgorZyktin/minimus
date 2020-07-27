# -*- coding: utf-8 -*-

"""Тесты.
"""
import os
import tempfile
import unittest
from pathlib import Path
from typing import Union
from unittest.mock import Mock

from minimus.file_system import FileSystem
from minimus.text_file import TextFile


class TestFileSystem(unittest.TestCase):
    def test_cast_path(self):
        f = FileSystem.cast_path
        self.assertEqual(f('test'), 'test')

        local = os.path.abspath(os.getcwd())
        self.assertEqual(f(Path()), local)

    def test_read(self):
        tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        try:
            tmp.write('xyz')
            tmp.seek(0)
            tmp.close()

            content = FileSystem.read(Path(tmp.name))
            self.assertEqual(content, 'xyz')
        finally:
            os.remove(tmp.name)

    def test_write(self):
        tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        try:
            FileSystem.write(Path(tmp.name), 'zzz')
            tmp.close()
            text = FileSystem.read(Path(tmp.name))
            self.assertEqual(text, 'zzz')
        finally:
            os.remove(tmp.name)

        self.assertFalse(FileSystem.write(Path('test'), ''))

    def test_get_files_of_type(self):
        class TFileSystem(FileSystem):
            @classmethod
            def read(cls, filename: Union[str, Path]) -> str:
                return f'<{filename}>'

        fake = Mock()
        fake.iterdir.return_value = [
            Path('file.txt'),
            Path('file.oth'),
            Path('z.minimus'),
            Path('index.minimus'),
        ]
        files = TFileSystem.get_files_of_type(fake, 'minimus', TextFile)
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0].filename == 'z.minimus')
