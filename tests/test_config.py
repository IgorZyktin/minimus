# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest

from minimus.config import Config


class TestConfig(unittest.TestCase):

    def test_creation(self):
        config = Config()
        self.assertEqual(config.lang, 'RU')

    def test_repr(self):
        config = Config()
        self.assertEqual(repr(config), 'Config()')

    def test_str(self):
        config = Config()
        config.launch_directory = 'l'
        config.script_directory = 's'
        config.source_directory = 's'
        config.target_directory = 't'

        ref = """
Config(
    bg_color_node='#5a0000',
    bg_color_tag='#04266c',
    custom_source=False,
    custom_target=False,
    lang='RU',
    launch_directory='l',
    protocol='file://',
    script_directory='s',
    source_directory='s',
    target_directory='t'
)
        """.strip()
        self.assertEqual(str(config), ref)
