# -*- coding: utf-8 -*-

"""Тесты.
"""
from minimus.utils.text_processing import make_prefix, numerate
from minimus.utils.output_processing import to_kv


def test_make_prefix():
    """Должен готовить префиксы с правильным числом разрядов.
    """
    assert make_prefix(1) == '{num:01} из {total:01d}'
    assert make_prefix(75) == '{num:02} из {total:02d}'
    assert make_prefix(825) == '{num:03} из {total:03d}'
    assert make_prefix(843346) == '{num:06} из {total:06d}'
    assert make_prefix(-1) == '{num:02} из {total:02d}'


def test_numerate_small():
    """Должен выполнить нумерацию с одним разрядом.
    """
    input_data = (chr(i) for i in range(97, 105))
    reference_data = [
        ('1 из 8', 'a'),
        ('2 из 8', 'b'),
        ('3 из 8', 'c'),
        ('4 из 8', 'd'),
        ('5 из 8', 'e'),
        ('6 из 8', 'f'),
        ('7 из 8', 'g'),
        ('8 из 8', 'h')
    ]
    assert list(numerate(input_data)) == reference_data


def test_numerate_big():
    """Должен выполнить нумерацию с двумя разрядами.
    """
    input_data = (chr(i) for i in range(65, 85))
    reference_data = [
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
    assert list(numerate(input_data)) == reference_data


def test_to_kv():
    """Должен разложить словарь в список аргументов.
    """
    assert to_kv({}) == []
    assert to_kv(dict(var=1, other='test')) == ['var=1', 'other=test']
