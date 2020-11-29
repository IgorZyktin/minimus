# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest

from minimus.old.text_file import TextFile


class TestTextFile(unittest.TestCase):
    def test_str(self):
        file = TextFile('some.txt', 'blah bla')
        self.assertEqual(str(file), "TextFile('some.txt')")
        self.assertEqual(file.filename, 'some.txt')
        self.assertEqual(file.content, 'blah bla')
        self.assertFalse(file.is_changed)

    def test_ordering(self):
        file1 = TextFile('a.txt', 'some text')
        file2 = TextFile('b.txt', 'some text')

        self.assertNotEqual(file1, file2)
        self.assertGreater(file2, file1)

        self.assertFalse(file1 == 25)

        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            _ = file1 > 25

    def test_hash(self):
        file1 = TextFile('a.txt', 'some text')

        hash_ref = hash(file1)
        self.assertEqual(hash(file1), hash_ref)

    def test_change(self):
        file1 = TextFile('a.txt', 'some text')
        self.assertFalse(file1.is_changed)
        file1.content = 'other text'
        self.assertTrue(file1.is_changed)

        file2 = TextFile('b.txt', 'some text')
        self.assertFalse(file2.is_changed)
        file2.filename = 'other.txt'
        self.assertTrue(file2.is_changed)

        with self.assertRaises(NameError) as cm:
            file1.contents = 25

        self.assertEqual(
            cm.exception.args[0],
            'Атрибут TextFile с текстовым содержимым '
            'должен называться "content", а не "contents".'
        )

    def test_attrs(self):
        file1 = TextFile('a.txt', 'some text')
        self.assertFalse(file1.attrs)

        file1.test = 825
        self.assertEqual(file1.test, 825)

        self.assertEqual(file1.filename, 'a.txt')
        file1.filename = 'other_file.txt'
        self.assertEqual(file1.filename, 'other_file.txt')
        self.assertTrue(file1.is_changed)

        with self.assertRaises(AttributeError) as cm:
            _ = file1.something

        self.assertEqual(
            cm.exception.args[0],
            "Экземпляр TextFile('other_file.txt') не имеет атрибута something."
        )
