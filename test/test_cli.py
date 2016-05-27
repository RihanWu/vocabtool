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

    def test_show_version(self):
        args = self._parse("-v")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", None),
                          ("show_version", True)])
        args = self._parse("--version")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", None),
                          ("show_version", True)])

    def test_lookup_minimum_argument(self):
        args = self._parse("- test")
        self.assertEqual(args._get_kwargs(),
                         [("language", "en"),
                          ("source", None),
                          ("word", "test"),
                          ("subcmd", "-"),
                          ("show_version", False)])

    def test_lookup_specify_language(self):
        args = self._parse("lookup test -l de")
        self.assertEqual(args._get_kwargs(),
                         [("language", "de"),
                          ("source", None),
                          ("word", "test"),
                          ("subcmd", "lookup"),
                          ("show_version", False)])

        args = self._parse("lookup test --language de")
        self.assertEqual(args._get_kwargs(),
                         [("language", "de"),
                          ("source", None),
                          ("word", "test"),
                          ("subcmd", "lookup"),
                          ("show_version", False)])

    def test_lookup_specify_one_source(self):
        args = self._parse("lookup test -s foo")
        self.assertEqual(args._get_kwargs(),
                         [("language", "en"),
                          ("source", ["foo"]),
                          ("word", "test"),
                          ("subcmd", "lookup"),
                          ("show_version", False)])

        args = self._parse("lookup test --source foo")
        self.assertEqual(args._get_kwargs(),
                         [("language", "en"),
                          ("source", ["foo"]),
                          ("word", "test"),
                          ("subcmd", "lookup"),
                          ("show_version", False)])

    def test_lookup_specify_multiple_source(self):
        args = self._parse("lookup test -s foo bar")
        self.assertEqual(args._get_kwargs(),
                         [("language", "en"),
                          ("source", ["foo", "bar"]),
                          ("word", "test"),
                          ("subcmd", "lookup"),
                          ("show_version", False)])

    def test_config_no_argument(self):
        args = self._parse("config")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", "config"),
                          ("read_arg", None),
                          ("write_arg", None),
                          ("enable_list", None),
                          ("disable_list", None)])

    def test_config_read_config(self):
        args = self._parse("config -r foo.bar")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", "config"),
                          ("read_arg", "foo.bar"),
                          ("write_arg", None),
                          ("enable_list", None),
                          ("disable_list", None)])
        args = self._parse("config --read foo.bar")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", "config"),
                          ("read_arg", "foo.bar"),
                          ("write_arg", None),
                          ("enable_list", None),
                          ("disable_list", None)])

    def test_config_write_config(self):
        args = self._parse("config -w foo.bar value")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", "config"),
                          ("read_arg", None),
                          ("write_arg", ["foo.bar", "value"]),
                          ("enable_list", None),
                          ("disable_list", None)])
        args = self._parse("config --write foo.bar value")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", "config"),
                          ("read_arg", None),
                          ("write_arg", ["foo.bar", "value"]),
                          ("enable_list", None),
                          ("disable_list", None)])

    def test_config_enable_list(self):
        args = self._parse("config -e foo bar")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", "config"),
                          ("read_arg", None),
                          ("write_arg", None),
                          ("enable_list", ["foo", "bar"]),
                          ("disable_list", None)])
        args = self._parse("config --enable foo bar")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", "config"),
                          ("read_arg", None),
                          ("write_arg", None),
                          ("enable_list", ["foo", "bar"]),
                          ("disable_list", None)])

    def test_config_disable_list(self):
        args = self._parse("config -d foo bar")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", "config"),
                          ("read_arg", None),
                          ("write_arg", None),
                          ("enable_list", None),
                          ("disable_list", ["foo", "bar"])])
        args = self._parse("config --disable foo bar")
        self.assertEqual(args._get_kwargs(),
                         [("subcmd", "config"),
                          ("read_arg", None),
                          ("write_arg", None),
                          ("enable_list", None),
                          ("disable_list", ["foo", "bar"])])

if __name__ == "__main__":
    unittest.main()
