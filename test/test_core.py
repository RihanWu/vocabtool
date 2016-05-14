# -*- coding: utf-8 -*-
"""Testing CLI module

Only supports Python 3.x now"""

import unittest

# Resolve import problem
import os
os.chdir("../")

from vocabtool import core


class TestCoreConfig(unittest.TestCase):
    """Test case for the config components of core"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_config(self):
        pass

    def test_read_config(self):
        pass

    def test_write_config(self):
        pass


class TestCoreLookUp(unittest.TestCase):
    """Test case for core's components related to looking up words"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_lookup_invalid_word(self):
        pass

    def test_lookup_invalid_language(self):
        pass

    def test_lookup_empty_source_list(self):
        pass


class TestCoreAddToDatabase(unittest.TestCase):
    """Test case for core's components related to adding entries to database"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_to_database(self):
        pass


class TestCoreGenerateLaTeX(unittest.TestCase):
    """Test case for core's components related to generate LaTeX output"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generate(self):
        pass

if __name__ == "__main__":
    unittest.main()
