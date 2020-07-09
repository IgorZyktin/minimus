# -*- coding: utf-8 -*-

"""Тесты линковщика.
"""
import os
import tempfile
import unittest
from pathlib import Path
from typing import Union
from unittest.mock import Mock

from .linker import *


class TestSyntax(unittest.TestCase):
    def test_transliterate(self):
        f = Syntax.transliterate
        self.assertEqual(f('Два весёлых гуся'), 'dva_veselyh_gusya')
        self.assertEqual(f('Мама мыла раму'), 'mama_myla_ramu')
        self.assertEqual(f('Ёкарный бабай'), 'ekarnyy_babay')
        self.assertEqual(f('ишь как оно итить'), 'ish_kak_ono_itit')

    def test_announce(self):
        f = Syntax.announce
        mock = Mock()
        f('a', 1, None, test='value', callback=mock)
        mock.assert_called_once_with('a, 1, None, test=value')


class TestFilesystem(unittest.TestCase):
    def test_cast_path(self):
        f = Filesystem.cast_path
        self.assertEqual(f('test'), 'test')

        local = os.path.abspath(os.getcwd())
        self.assertEqual(f(Path()), local)

    def test_read(self):
        tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        try:
            tmp.write('xyz')
            tmp.seek(0)
            tmp.close()

            content = Filesystem.read(tmp.name)
            self.assertEqual(content, 'xyz')
        finally:
            os.remove(tmp.name)

    def test_write(self):
        tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        try:
            mock = Mock()
            Filesystem.write(tmp.name, '', mock)
            mock.assert_not_called()

            mock = Mock()
            Filesystem.write(tmp.name, 'abc', mock)

            text = mock.mock_calls[0].args[0]

            self.assertTrue(text.startswith('Сохранены изменения в файле'))
        finally:
            tmp.close()
            os.remove(tmp.name)

    def test_get_files_of_type(self):
        class TFilesystem(Filesystem):
            @classmethod
            def read(cls, filename: Union[str, Path]) -> str:
                return f'<{filename}>'

        fake = Mock()
        fake.iterdir.return_value = [
            Path('file.txt'),
            Path('file.oth'),
            Path('z.zet'),
            Path('index.zet'),
        ]
        files = TFilesystem.get_files_of_type(fake, 'zet', TextFile)
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0].filename == 'z.zet')


if __name__ == '__main__':
    unittest.main()
