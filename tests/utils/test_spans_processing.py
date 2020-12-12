# -*- coding: utf-8 -*-

"""Тесты.
"""
import re

import pytest

from minimus.components.segment_types import BareTag
from minimus.utils.spans_processing import make_spans_for_segments, Span, \
    make_inverted_spans, make_inverted_spans_for_one


@pytest.fixture()
def segments():
    """Набор обработанных сегментов на базе регулярных выражений.
    """
    string = 'one dot two dot three'
    return [
        BareTag(re.search('one', string)),
        BareTag(re.search('two', string)),
        BareTag(re.search('three', string)),
    ]


@pytest.fixture()
def fix_spans_for_segments():
    """Эталонные отрезки для сегментов.
    """
    return [
        Span(start=0, stop=3),
        Span(start=8, stop=11),
        Span(start=16, stop=21)
    ]


@pytest.fixture()
def ref_spans_for_inverted_segments():
    """Эталонные отрезки для инвертированных сегментов.
    """
    return [
        Span(start=3, stop=8),
        Span(start=11, stop=16),
    ]


@pytest.fixture()
def fix_spans_for_inverted_segments_big():
    """Набор отрезков для инвертирования.
    """
    return [
        Span(start=2, stop=3),
        Span(start=8, stop=11),
        Span(start=16, stop=18)
    ]


@pytest.fixture()
def ref_spans_for_inverted_segments_big():
    """Эталонные отрезки для инвертированных сегментов.
    """
    return [
        Span(start=0, stop=2),
        Span(start=3, stop=8),
        Span(start=11, stop=16),
        Span(start=18, stop=20),
    ]


def test_make_spans_for_segments(segments, fix_spans_for_segments):
    """Должен создать отрезки для набора сегментов.
    """
    spans = make_spans_for_segments(segments)
    assert spans == fix_spans_for_segments


def test_make_inverted_spans(fix_spans_for_segments,
                             ref_spans_for_inverted_segments):
    """Должен создать отрезки, заполняющие дыры между сегментами.
    """
    inverted = make_inverted_spans(fix_spans_for_segments,
                                   total=fix_spans_for_segments[-1].stop)
    assert inverted == ref_spans_for_inverted_segments


def test_make_inverted_spans_empty():
    """Должен вернуть весь отрезок.
    """
    inverted = make_inverted_spans([], total=10)
    assert inverted == [Span(start=0, stop=10)]


def test_make_inverted_spans_single_1():
    """Должен обработать один отрезок.
    """
    inverted = make_inverted_spans_for_one(Span(start=0, stop=10), total=10)
    assert inverted == []


def test_make_inverted_spans_single_2():
    """Должен обработать один отрезок.
    """
    inverted = make_inverted_spans_for_one(Span(start=5, stop=10), total=10)
    assert inverted == [Span(start=0, stop=5)]


def test_make_inverted_spans_single_3():
    """Должен обработать один отрезок.
    """
    inverted = make_inverted_spans_for_one(Span(start=0, stop=5), total=10)
    assert inverted == [Span(start=5, stop=10)]


def test_make_inverted_spans_single_4():
    """Должен обработать один отрезок.
    """
    inverted = make_inverted_spans_for_one(Span(start=0, stop=0), total=10)
    assert inverted == [Span(start=0, stop=10)]


def test_make_inverted_spans_single_5():
    """Должен обработать один отрезок.
    """
    inverted = make_inverted_spans([Span(start=3, stop=6)], total=10)
    assert inverted == [
        Span(start=0, stop=3),
        Span(start=6, stop=10),
    ]


def test_make_inverted_spans_big(fix_spans_for_inverted_segments_big,
                                 ref_spans_for_inverted_segments_big):
    """Должен создать отрезки, заполняющие дыры между сегментами.
    """
    inverted = make_inverted_spans(
        fix_spans_for_inverted_segments_big,
        total=20
    )
    assert inverted == ref_spans_for_inverted_segments_big
