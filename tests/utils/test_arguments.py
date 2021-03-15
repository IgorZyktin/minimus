# -*- coding: utf-8 -*-

"""Tests.
"""
from unittest.mock import patch

import pytest

from minimus.utils.arguments import (
    parse_command_line_arguments,
    apply_cli_args_to_settings,
)


@pytest.fixture()
def fix_default_arguments():
    """No additional arguments."""
    return {
        'language': 'RU',
        'readme_directory': None,
        'source_directory': None,
        'target_directory': None,
    }


@pytest.fixture()
def fix_use_english():
    """Language is specified."""
    return {
        'language': 'EN',
        'readme_directory': None,
        'source_directory': None,
        'target_directory': None,
    }


@pytest.fixture()
def fix_use_readme():
    """Readme folder is specified."""
    return {
        'language': 'RU',
        'readme_directory': 'somewhere',
        'source_directory': None,
        'target_directory': None,
    }


@pytest.fixture()
def reference(request, fix_default_arguments,
              fix_use_english, fix_use_readme) -> dict:
    """Fixture selector."""
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
    """Must extract specific parameters."""
    result = parse_command_line_arguments(raw_arguments)
    assert result == reference


def test_apply_cli_args_to_config_default(fix_default_arguments):
    """Config must stay the same."""
    with patch('minimus.utils.arguments.settings') as fake_settings:
        apply_cli_args_to_settings(fix_default_arguments)

    for key, value in fix_default_arguments.items():
        if value is not None:
            assert getattr(fake_settings, key.upper()) == value


def test_apply_cli_args_to_config_new(fix_use_english, fix_use_readme):
    """Config must be mutated."""
    arguments = {
        **{k: v for k, v in fix_use_english.items() if v is not None},
        **{k: v for k, v in fix_use_readme.items() if v is not None},
    }
    with patch('minimus.utils.arguments.settings') as fake_settings:
        apply_cli_args_to_settings(arguments)

    for key, value in arguments.items():
        if value is not None:
            assert getattr(fake_settings, key.upper()) == value


def test_apply_cli_args_readme(fix_default_arguments):
    """Must use target directory for readme."""
    fix_default_arguments['target_directory'] = 'somewhere'

    with patch('minimus.utils.arguments.settings') as fake_settings:
        apply_cli_args_to_settings(fix_default_arguments)

    assert fake_settings.README_DIRECTORY == 'somewhere'
