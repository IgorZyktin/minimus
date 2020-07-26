# -*- coding: utf-8 -*-

"""Тесты.
"""
import unittest

from minimus.graph import Graph


class TestGraph(unittest.TestCase):

    def test_node(self):
        graph = Graph()
        graph.add_node('a', 'label', 'color', 'link')
        ref = {
            'edges': {},
            'nodes': {
                'a': {
                    'bg_color': 'color',
                    'label': 'label',
                    'link': 'link'
                }
            }
        }
        self.assertEqual(graph.as_dict(), ref)

    def test_edge(self):
        graph = Graph()
        graph.add_edge('start', 'finish')
        ref = {
            'edges': {
                'start': {
                    'finish': {
                        'weight': 0.1}}},
            'nodes': {}
        }
        self.assertEqual(graph.as_dict(), ref)
