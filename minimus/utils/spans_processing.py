# -*- coding: utf-8 -*-

"""Инструменты для работы с отрезками внутри текста.
"""
from collections import deque
from typing import NamedTuple, List

from minimus.components.segment_types import RegExSegment


class Span(NamedTuple):
    """Запись о том, где сегмент начинается и где заканчивается.
    """
    start: int
    stop: int


def make_spans_for_segments(segments: List[RegExSegment]) -> List[Span]:
    """Выделить информацию о начале и конце сегментов.
    """
    spans = []
    for segment in segments:
        spans.append(Span(segment.start_outer, segment.end_outer))
    return spans


def make_inverted_spans(spans: List[Span], total: int) -> List[Span]:
    """Собрать список отрезков, внутри которых нет регулярных выражений.
    """
    if not spans:
        return [Span(0, total)]

    if len(spans) == 1:
        return make_inverted_spans_for_one(spans[0], total)

    inverted_spans = []

    # первый кусок текста в файле
    if spans[0].start > 0:
        inverted_spans.append(Span(0, spans[0].start))

    unprocessed_spans = deque(spans)

    while unprocessed_spans:
        next_span = unprocessed_spans.popleft()

        # последний кусок текста в файле
        if not unprocessed_spans:
            if next_span.stop != total:
                inverted_spans.append(Span(next_span.stop, total))
            break

        inverted_spans.append(
            Span(next_span.stop, unprocessed_spans[0].start)
        )

    return inverted_spans


def make_inverted_spans_for_one(span: Span, total: int) -> List[Span]:
    """Собрать список отрезков, внутри которых нет регулярных выражений.
    """
    if span.start == span.stop:
        return [Span(0, total)]

    elif span.start == 0 and span.stop != total:
        return [Span(span.stop, total)]

    elif span.start != 0 and span.stop == total:
        return [Span(0, span.start)]

    elif span.start != 0 and span.stop != total:
        return [Span(0, span.start), Span(span.stop, total)]

    return []
