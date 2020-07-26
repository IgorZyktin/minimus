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
        self.assertTrue(files[0].corresponding_filename == 'z.minimus')
