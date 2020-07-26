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