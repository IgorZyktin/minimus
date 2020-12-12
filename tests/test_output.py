# -*- coding: utf-8 -*-

"""Тесты.
"""
from functools import partial
from unittest.mock import patch, call, Mock

from minimus.config import Config
from minimus.output import describe_resulting_config
from minimus.utils.output_processing import stdout


def test_describe_config_ru():
    """Должен вывести на экран содержимое конфига.
    """
    config = Config()
    config.LANGUAGE = 'RU'
    config.BASE_PATH = 'path0'
    config.LAUNCH_DIRECTORY = 'path1'
    config.SOURCE_DIRECTORY = 'path2'
    config.TARGET_DIRECTORY = 'path3'
    config.README_DIRECTORY = 'path4'

    fake_stdout = Mock()
    describe_resulting_config(config, fake_stdout)

    fake_stdout.assert_has_calls([
        call('Script started at: {folder}', folder='path1'),
        call('Source directory: {folder}', folder='path2'),
        call('Output directory: {folder}', folder='path3'),
        call('README.md directory: {folder}', folder='path4')
    ])

    with patch('builtins.print') as fake_print:
        _stdout = partial(stdout, language='RU')
        describe_resulting_config(config, _stdout)

    fake_print.assert_has_calls([
        call('Скрипт запущен в каталоге: path1'),
        call('Каталог исходных данных: path2'),
        call('Каталог обработанных данных: path3'),
        call('Каталог для файла README.md: path4'),
    ])


def test_describe_config_en():
    """Должен вывести на экран содержимое конфига.
    """
    config = Config()
    config.LANGUAGE = 'EN'
    config.BASE_PATH = 'path0'
    config.LAUNCH_DIRECTORY = 'path1'
    config.SOURCE_DIRECTORY = 'path2'
    config.TARGET_DIRECTORY = 'path3'
    config.README_DIRECTORY = 'path4'

    fake_stdout = Mock()
    describe_resulting_config(config, fake_stdout)

    fake_stdout.assert_has_calls([
        call('Script started at: {folder}', folder='path1'),
        call('Source directory: {folder}', folder='path2'),
        call('Output directory: {folder}', folder='path3'),
        call('README.md directory: {folder}', folder='path4'),
    ])

    with patch('builtins.print') as fake_print:
        _stdout = partial(stdout, language='EN')
        describe_resulting_config(config, _stdout)

    fake_print.assert_has_calls([
        call('Script started at: path1'),
        call('Source directory: path2'),
        call('Output directory: path3'),
        call('README.md directory: path4'),
    ])
