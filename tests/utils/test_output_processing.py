# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest
from unittest.mock import Mock, patch

from minimus.utils import output_processing


class TestOutputProcessing(unittest.TestCase):
    def test_transliterate(self):
        f = output_processing.transliterate
        self.assertEqual(f('Два весёлых гуся'), 'dva_veselyh_gusya')
        self.assertEqual(f('Мама мыла раму'), 'mama_myla_ramu')
        self.assertEqual(f('Ёкарный бабай'), 'ekarnyy_babay')
        self.assertEqual(f('ишь как оно итить'), 'ish_kak_ono_itit')

    def test_announce(self):
        f = output_processing.announce
        mock = Mock()
        f('a', 1, None, test='value', callback=mock)
        mock.assert_called_once_with('a, 1, None, test=value')

    def test_stdout_ru(self):
        mock = Mock()
        with patch('minimus.utils.output_processing.settings.LANGUAGE', 'RU'):
            output_processing.stdout('test {x}', callback=mock, x=1)
            mock.assert_called_once_with('тест 1')

    def test_stdout_en(self):
        mock = Mock()
        with patch('minimus.utils.output_processing.settings.LANGUAGE', 'EN'):
            output_processing.stdout('test {x}', callback=mock, x=1)
            mock.assert_called_once_with('test 1')

    def test_stdout_unknown(self):
        mock = Mock()
        with patch('minimus.utils.output_processing.settings.LANGUAGE', '???'):
            output_processing.stdout('test {x}', callback=mock, x=1)
            mock.assert_called_once_with('test 1')
