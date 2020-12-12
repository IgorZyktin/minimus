# -*- coding: utf-8 -*-

"""Тесты.
"""
import pytest

from minimus.settings import Config
from minimus.utils.arguments import parse_command_line_arguments, \
    apply_cli_args_to_settings


@pytest.fixture()
def fix_default_arguments():
    """Для случая, когда дополнительные аргументы не заданы.
    """
    return {'language': 'RU', 'readme_directory': None,
            'source_directory': None, 'target_directory': None}


@pytest.fixture()
def fix_use_english():
    """Для случая, когда выбран язык.
    """
    return {'language': 'EN', 'readme_directory': None,
            'source_directory': None, 'target_directory': None}


@pytest.fixture()
def fix_use_readme():
    """Для случая, когда указан каталог для readme.md.
    """
    return {'language': 'RU', 'readme_directory': 'somewhere',
            'source_directory': None, 'target_directory': None}


@pytest.fixture()
def reference(request, fix_default_arguments,
              fix_use_english, fix_use_readme) -> dict:
    """Диспетчер для выбора фикстур.
    """
    return {
        'default': fix_default_arguments,
        'english': fix_use_english,
        'readme': fix_use_readme,
    }[request.param]


@pytest.mark.parametrize('raw_arguments,reference', [
    ([], 'default'),
    (['', '--language', 'EN'], 'english'),
    (['', '--readme_directory', 'somewhere'], 'readme'),
], indirect=['reference'])
def test_parse_command_line_arguments(raw_arguments, reference):
    """Должен выделить нужные параметры из списка аргументов командной строки.
    """
    result = parse_command_line_arguments(raw_arguments)
    assert result == reference


def test_apply_cli_args_to_config_default(fix_default_arguments):
    """Должен оставить конфиг как есть.
    """
    config = Config()
    apply_cli_args_to_settings(config, fix_default_arguments)

    for argument in dir(Config):
        if argument.isupper():
            assert getattr(config, argument) == getattr(Config, argument)


def test_apply_cli_args_to_config_new(fix_use_english, fix_use_readme):
    """Должен мутировать экземпляр конфига.
    """
    config = Config()
    arguments = {
        **{k: v for k, v in fix_use_english.items() if v is not None},
        **{k: v for k, v in fix_use_readme.items() if v is not None},
    }
    apply_cli_args_to_settings(config, arguments)

    for key, value in arguments.items():
        assert getattr(config, key.upper()) == value
