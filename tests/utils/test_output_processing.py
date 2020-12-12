# -*- coding: utf-8 -*-

"""Тесты.
"""
from unittest.mock import Mock

from minimus.utils import output_processing


def test_transliterate():
    f = output_processing.transliterate
    assert f('Два весёлых гуся') == 'dva_veselyh_gusya'
    assert f('Мама мыла раму') == 'mama_myla_ramu'
    assert f('Ёкарный бабай') == 'ekarnyy_babay'
    assert f('ишь как оно итить') == 'ish_kak_ono_itit'


def test_announce():
    f = output_processing.announce
    mock = Mock()
    f('a', 1, None, test='value', callback=mock)
    mock.assert_called_once_with('a, 1, None, test=value')


def test_stdout_ru():
    mock = Mock()
    output_processing.stdout('test {x}', callback=mock, x=1, language='RU')
    mock.assert_called_once_with('тест 1')


def test_stdout_en():
    mock = Mock()
    output_processing.stdout('test {x}', callback=mock, x=1, language='EN')
    mock.assert_called_once_with('test 1')


def test_stdout_unknown():
    mock = Mock()
    output_processing.stdout('test {x}', callback=mock, x=1, language='??')
    mock.assert_called_once_with('test 1')
