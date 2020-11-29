# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest
from unittest.mock import Mock

import minimus.utils.text_processing
from minimus.old.syntax import Syntax


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

    def test_to_json(self):
        d = dict(a=1, b=2, c=None)
        res = Syntax.to_json(d)
        ref = """
{
    "a": 1,
    "b": 2,
    "c": null
}
        """.strip()
        self.assertEqual(res, ref)

    def test_make_prefix(self):
        self.assertEqual(minimus.utils.text_processing.make_prefix(1), '{num:01} из {total:01d}')
        self.assertEqual(minimus.utils.text_processing.make_prefix(75), '{num:02} из {total:02d}')
        self.assertEqual(minimus.utils.text_processing.make_prefix(825), '{num:03} из {total:03d}')
        self.assertEqual(minimus.utils.text_processing.make_prefix(843346), '{num:06} из {total:06d}')
        self.assertEqual(minimus.utils.text_processing.make_prefix(-1), '{num:02} из {total:02d}')

    def test_numerate(self):
        inp = (chr(i) for i in range(97, 105))
        ref = [
            ('1 из 8', 'a'),
            ('2 из 8', 'b'),
            ('3 из 8', 'c'),
            ('4 из 8', 'd'),
            ('5 из 8', 'e'),
            ('6 из 8', 'f'),
            ('7 из 8', 'g'),
            ('8 из 8', 'h')
        ]
        self.assertEqual(list(minimus.utils.text_processing.numerate(inp)), ref)

        inp = (chr(i) for i in range(65, 85))
        ref = [
            ('01 из 20', 'A'),
            ('02 из 20', 'B'),
            ('03 из 20', 'C'),
            ('04 из 20', 'D'),
            ('05 из 20', 'E'),
            ('06 из 20', 'F'),
            ('07 из 20', 'G'),
            ('08 из 20', 'H'),
            ('09 из 20', 'I'),
            ('10 из 20', 'J'),
            ('11 из 20', 'K'),
            ('12 из 20', 'L'),
            ('13 из 20', 'M'),
            ('14 из 20', 'N'),
            ('15 из 20', 'O'),
            ('16 из 20', 'P'),
            ('17 из 20', 'Q'),
            ('18 из 20', 'R'),
            ('19 из 20', 'S'),
            ('20 из 20', 'T')
        ]
        self.assertEqual(list(minimus.utils.text_processing.numerate(inp)), ref)

    def test_stdout(self):
        config = Mock()
        mock = Mock()
        Syntax.set_config(config)

        config.lang = 'RU'
        Syntax.stdout('test {x}', callback=mock, x=1)
        mock.assert_called_once_with('тест 1')
        mock.reset_mock()

        config.lang = 'EN'
        Syntax.stdout('test {x}', callback=mock, x=2)
        mock.assert_called_once_with('test 2')
        mock.reset_mock()

        Syntax.stdout('x', 1, 2, 3, 4, callback=mock)
        mock.assert_called_once_with('x, 1, 2, 3, 4')
