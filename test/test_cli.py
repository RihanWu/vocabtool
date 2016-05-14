# -*- coding: utf-8 -*-
"""Testing CLI module

Only supports Python 3.x now"""

import unittest

# Resolve import problem
import os
os.chdir("../")

from vocabtool import cli


class TestCLI(unittest.TestCase):
    """Test case for CLI"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _parse(self, test_string):
        return cli.parser.parse_args(test_string.split())

    def test_minimum_argument(self):
        args = self._parse("test")
        self.assertEqual(args._get_kwargs(),
                         [('language', 'en'),
                          ('source', None),
                          ('word', 'test')])

    def test_specify_language(self):
        args = self._parse("test -l de")
        self.assertEqual(args._get_kwargs(),
                         [('language', 'de'),
                          ('source', None),
                          ('word', 'test')])

        args = self._parse("test --language de")
        self.assertEqual(args._get_kwargs(),
                         [('language', 'de'),
                          ('source', None),
                          ('word', 'test')])

    def test_specify_one_source(self):
        args = self._parse("test -s m_w_c_d")
        self.assertEqual(args._get_kwargs(),
                         [('language', 'en'),
                          ('source', ["m_w_c_d"]),
                          ('word', 'test')])

        args = self._parse("test --source m_w_c_d")
        self.assertEqual(args._get_kwargs(),
                         [('language', 'en'),
                          ('source', ["m_w_c_d"]),
                          ('word', 'test')])

    def test_specify_multiple_source(self):
        args = self._parse("test -s m_w_c_d iciba_com dict_cn")
        self.assertEqual(args._get_kwargs(),
                         [('language', 'en'),
                          ('source', ["m_w_c_d", "iciba_com", "dict_cn"]),
                          ('word', 'test')])

if __name__ == "__main__":
    unittest.main()
