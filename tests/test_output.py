# -*- coding: utf-8 -*-

"""Tests.
"""
from unittest.mock import patch, call, ANY

from minimus import settings
from minimus.output import (
    show_greeting_message,
    show_resulting_settings,
    show_separation_line,
    show_user_files_rendering,
    show_auto_files_rendering,
    show_final_message,
    show_index_files_rendering,
)


@patch('minimus.output.stdout')
def test_show_greeting_message(fake_stdout):
    show_greeting_message()
    fake_stdout.assert_has_calls([
        call(settings.LINE, color=ANY),
        call(settings.LOGO, color=ANY),
        call('Version: {version}', color=ANY, version=settings.__version__),
        call(settings.LINE, color=ANY),
    ])


@patch('minimus.output.stdout')
def test_show_resulting_settings(fake_stdout):
    show_resulting_settings()
    fake_stdout.assert_has_calls([
        call('  Script started at: {folder}', color=ANY,
             folder=settings.LAUNCH_DIRECTORY),
        call('   Source directory: {folder}', color=ANY,
             folder=settings.SOURCE_DIRECTORY),
        call('   Output directory: {folder}', color=ANY,
             folder=settings.TARGET_DIRECTORY),
        call('README.md directory: {folder}', color=ANY,
             folder=settings.README_DIRECTORY),
    ])


@patch('minimus.output.stdout')
def test_show_separation_line(fake_stdout):
    show_separation_line()
    fake_stdout.assert_has_calls([
        call(settings.LINE, color=ANY),
    ])


@patch('minimus.output.stdout')
def test_show_user_files_rendering(fake_stdout):
    show_user_files_rendering()
    fake_stdout.assert_has_calls([
        call('Saving original files:', color=ANY),
    ])


@patch('minimus.output.stdout')
def test_show_auto_files_rendering(fake_stdout):
    show_auto_files_rendering()
    fake_stdout.assert_has_calls([
        call(''),
        call('Saving generated files:', color=ANY),
    ])


@patch('minimus.output.stdout')
def test_show_index_files_rendering(fake_stdout):
    show_index_files_rendering()
    fake_stdout.assert_has_calls([
        call(''),
        call('Saving indexes:', color=ANY),
    ])


@patch('minimus.output.stdout')
def test_show_final_message(fake_stdout):
    show_final_message(25.4)
    fake_stdout.assert_has_calls([
        call(settings.LINE, color=ANY),
        call('Processing complete in {seconds} sec.',
             color=ANY, seconds='25.40'),
        call(settings.LINE, color=ANY),
    ])
