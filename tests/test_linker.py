# -*- coding: utf-8 -*-

"""Тесты линковщика.
"""
import os
import tempfile
import unittest
from pathlib import Path
from typing import Union
from unittest.mock import Mock

from minimus.linker import *

REF_MD = r"""
# Слон

Большое млекопитающие.

---
\#хобот
[\#4 лапы](./meta_4_lapy.md)
[\#серый](./meta_seryy.md)
\#большой

Живёт в Африке и Индии \#большой.
""".strip()

REF_MD_WITH_LINKS = r"""
# Слон

Большое млекопитающие.

---
[\#хобот](./meta_hobot.md)
[\#4 лапы](./meta_4_lapy.md)
[\#серый](./meta_seryy.md)
[\#большой](./meta_bolshoy.md)

Живёт в Африке и Индии [\#большой](./meta_bolshoy.md).
""".strip()

REF_METAFILE_MD = """
## Все вхождения тега "ultra"

---


1 из 2. [Title 1](./a.txt)

2 из 2. [Title 2](./b.txt)

""".lstrip()





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

            content = Filesystem.read(Path(tmp.name))
            self.assertEqual(content, 'xyz')
        finally:
            os.remove(tmp.name)

    def test_write(self):
        tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        try:
            Filesystem.write(Path(tmp.name), 'zzz')
            tmp.close()
            text = Filesystem.read(Path(tmp.name))
            self.assertEqual(text, 'zzz')
        finally:
            os.remove(tmp.name)

        self.assertFalse(Filesystem.write(Path('test'), ''))

    def test_get_files_of_type(self):
        class TFilesystem(Filesystem):
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
        files = TFilesystem.get_files_of_type(fake, 'minimus', TextFile)
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0].filename == 'z.minimus')


class TestTextFile(unittest.TestCase):
    def test_str(self):
        file = TextFile('some.txt', 'blah bla')
        self.assertEqual(str(file), "TextFile('some.txt')")
        self.assertEqual(file.filename, 'some.txt')
        self.assertEqual(file.contents, 'blah bla')
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
        file1.contents = 'other text'
        self.assertTrue(file1.is_changed)

        file2 = TextFile('b.txt', 'some text')
        self.assertFalse(file2.is_changed)
        file2.filename = 'other.txt'
        self.assertTrue(file2.is_changed)

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


class TestMarkdownSyntax(unittest.TestCase):
    def test_href(self):
        self.assertEqual(MarkdownSyntax.href('blah', 'zz'), '[blah](./zz)')
        self.assertEqual(MarkdownSyntax.href('other', 'xx'), '[other](./xx)')

    def test_tag2href(self):
        self.assertEqual(
            MarkdownSyntax.tag2href('лошадь'),
            r'[\#лошадь](./meta_loshad.md)'
        )
        self.assertEqual(
            MarkdownSyntax.tag2href('bar'),
            r'[\#bar](./meta_bar.md)'
        )

    def test_index_filename(self):
        self.assertEqual(MarkdownSyntax.get_index_filename(), 'index.md')

    def test_get_tag_filename(self):
        self.assertEqual(
            MarkdownSyntax.get_tag_filename('некий тег'), 'meta_nekiy_teg.md')
        self.assertEqual(
            MarkdownSyntax.get_tag_filename('упячка'), 'meta_upyachka.md')

    def test_extract_title(self):
        self.assertEqual(
            MarkdownSyntax.extract_title(REF_MD), 'Слон'
        )
        self.assertEqual(
            MarkdownSyntax.extract_title('XXXX'), '???'
        )

    def test_extract_tags(self):
        self.assertEqual(
            MarkdownSyntax.extract_tags(REF_MD),
            {'большой', '4 лапы', 'серый', 'хобот'}
        )


class TestHTMLSyntax(unittest.TestCase):

    def setUp(self) -> None:
        class HTMLTest(HTMLSyntax):
            @staticmethod
            def get_local_dir() -> str:
                return 'dir'

        self.inst = HTMLTest()

    def test_make_link(self):
        link = self.inst.make_link('text')
        self.assertEqual(link, 'file://dir/text')

    def test_get_local_dir(self):
        link = HTMLSyntax.get_local_dir()
        self.assertTrue('\\' not in link)

    def test_render_tag_graph(self):
        file_a = TextFile('a.txt', 'nothing')
        file_b = TextFile('b.txt', 'nothing')
        file_c = TextFile('c.txt', 'nothing')

        file_a.title = 'Title a'
        file_b.title = 'Title b'
        file_c.title = 'Title c'

        ref = {'edges': {'tag': {'title_a': {'weight': 0.1},
                                 'title_b': {'weight': 0.1},
                                 'title_c': {'weight': 0.1}}},
               'nodes': {'tag': {'bg_color': '#04266c',
                                 'label': 'test',
                                 'link': 'file://dir/meta_test.md'},
                         'title_a': {'bg_color': '#5a0000',
                                     'label': 'Title a',
                                     'link': 'file://dir/a.txt'},
                         'title_b': {'bg_color': '#5a0000',
                                     'label': 'Title b',
                                     'link': 'file://dir/b.txt'},
                         'title_c': {'bg_color': '#5a0000',
                                     'label': 'Title c',
                                     'link': 'file://dir/c.txt'}}}

        res = self.inst.render_tag_graph('test', [file_a, file_b, file_c])
        self.assertEqual(res, ref)

    def test_index_filename(self):
        self.assertEqual(HTMLSyntax.get_index_filename(), 'index.html')

    def test_get_tag_filename(self):
        self.assertEqual(
            HTMLSyntax.get_tag_filename('некий тег'), 'meta_nekiy_teg.html')
        self.assertEqual(
            HTMLSyntax.get_tag_filename('упячка'), 'meta_upyachka.html')

    def test_make_metafile_contents(self):
        file_1 = TextFile('a.txt', '')
        file_1.title = 'Title 1'

        file_2 = TextFile('b.txt', '')
        file_2.title = 'Title 2'

        text = MarkdownSyntax.make_metafile_contents('ultra', [file_1, file_2])
        self.assertEqual(text, REF_METAFILE_MD)

        text = MarkdownSyntax.make_metafile_contents('ultra', [])
        self.assertEqual(text, '')

    def test_replace_tags_with_hrefs(self):
        text = MarkdownSyntax.replace_tags_with_hrefs(
            REF_MD, {'большой', '4 лапы', 'серый', 'хобот'}
        )
        self.assertEqual(text, REF_MD_WITH_LINKS)


class TestGraph(unittest.TestCase):

    def test_node(self):
        graph = Graph()
        graph.add_node('a', 'label', 'color', 'link')
        ref = {
            'edges': {},
            'nodes': {
                'a': {
                    'bg_color': 'color',
                    'label': 'label',
                    'link': 'link'
                }
            }
        }
        self.assertEqual(graph.as_dict(), ref)

    def test_edge(self):
        graph = Graph()
        graph.add_edge('start', 'finish')
        ref = {
            'edges': {
                'start': {
                    'finish': {
                        'weight': 0.1}}},
            'nodes': {}
        }
        self.assertEqual(graph.as_dict(), ref)


class TestFunctions(unittest.TestCase):
    def test_map_tags_to_files(self):
        file_1 = TextFile('a.txt', '# File 1\n\\#tag1\n\\#tag2')
        file_2 = TextFile('b.txt', '# File 1\n\\#tag2\n\\#tag3')
        file_3 = TextFile('c.txt', '# File 1\n\\#tag3\n\\#tag1')

        mapped = map_tags_to_files([file_1, file_2, file_3])

        ref = {
            'tag1': [file_1, file_3],
            'tag2': [file_1, file_2],
            'tag3': [file_2, file_3],
        }

        self.assertEqual(mapped, ref)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
