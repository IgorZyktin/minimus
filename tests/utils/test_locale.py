# -*- coding: utf-8 -*-

"""Tests.
"""
from unittest.mock import Mock, patch

from minimus.utils import utils_locale


def test_transliterate():
    f = utils_locale.transliterate
    assert f('Два весёлых гуся') == 'dva_veselyh_gusya'
    assert f('Мама мыла раму') == 'mama_myla_ramu'
    assert f('Ёкарный бабай') == 'ekarnyy_babay'
    assert f('ишь как оно итить') == 'ish_kak_ono_itit'


def test_announce():
    f = utils_locale.announce
    mock = Mock()
    f('a', 1, None, test='value', callback=mock)
    mock.assert_called_once_with('a, 1, None, test=value')


def test_stdout_ru():
    mock = Mock()
    utils_locale.stdout('test {x}', callback=mock, x=1, language='RU')
    mock.assert_called_once_with('тест 1')


def test_stdout_en():
    mock = Mock()
    utils_locale.stdout('test {x}', callback=mock, x=1, language='EN')
    mock.assert_called_once_with('test 1')


def test_stdout_unknown():
    mock = Mock()
    utils_locale.stdout('test {x}', callback=mock, x=1, language='??')
    mock.assert_called_once_with('test 1')


def test_translate_normal():
    with patch('minimus.utils.utils_locale.settings') as fake_settings:
        fake_settings.LANGUAGE = 'EN'
        assert utils_locale.translate('test {x}', 'RU') == 'тест {x}'
        assert utils_locale.translate('test {x}', 'EN') == 'test {x}'
        assert utils_locale.translate('test {x}', '') == 'test {x}'

        fake_settings.LANGUAGE = 'RU'
        assert utils_locale.translate('test {x}', 'RU') == 'тест {x}'
        assert utils_locale.translate('test {x}', 'EN') == 'test {x}'
        assert utils_locale.translate('test {x}', '') == 'тест {x}'
