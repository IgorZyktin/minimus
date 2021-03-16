# -*- coding: utf-8 -*-

"""Tests.
"""
from minimus.core.class_markdown import Markdown


def test_extract_header():
    """Must find actual header."""
    markdown = Markdown()
    res = markdown.extract_header('# Test\nwtf')
    assert res == 'Test'
    res = markdown.extract_header('\n### Demo\nwtf')
    assert res == 'Demo'
    res = markdown.extract_header('')
    assert res == '???'


def test_extract_tags():
    """Must find all tags in text."""
    markdown = Markdown()
    res = markdown.extract_tags("""
    {{ tag1}} and some {{tag2}}
    and also
    {{       tag3      }}
    """)
    assert res == ['tag1', 'tag2', 'tag3']


def test_make_tag_pattern():
    """Must create pattern suitable for tag replacement."""
    markdown = Markdown()
    assert markdown.make_tag_pattern('some_tag') == r'{{\s*some_tag\s*}}'


def test_local():
    """Must create local folder path."""
    markdown = Markdown()
    assert markdown.local('this') == './this'
    assert markdown.local('./this') == './this'


def test_extract_features():
    """Must find all elements in given text."""
    markdown = Markdown()
    raw_text = """
    # Super 
    {{ mega test }}
    for finding {{ various }} {{ elements }} 
    in {{ mega test }}
    """

    text = ("""
    # Super 
    [mega test](./meta_mega_test.md)
    for finding [various](./meta_various.md) [elements](./meta_elements.md) 
    in [mega test](./meta_mega_test.md)
    """)
    res = markdown.extract_features(raw_text)
    assert res.header == 'Super'
    assert res.tags == ['mega test', 'various', 'elements']
    assert res.content == text
    assert res.category == 'mega test'
