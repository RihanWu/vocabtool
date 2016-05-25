# -*- coding: utf-8 -*-
"""Testing core module

Only supports Python 3.x now"""

import unittest

# Resolve import problem
import os
os.chdir("../")

from vocabtool import core


class TestCoreInitLoadConfig(unittest.TestCase):
    """Test case for the core class initializing process"""

    def setUp(self):
        valid_config_string = """{
                                    "dictionaries": {
                                        "test_dict": {
                                            "base_url": "Test base_url",
                                            "dictionary_name": "Test Dict",
                                            "enable": true,
                                            "id": "test_dict",
                                            "lang": "en"
                                        }
                                    }
                                 }
                              """
        with open("valid_config", "wb") as f:
            f.write(valid_config_string.encode("utf8"))
        with open("non_utf8", "wb") as f:
            f.write("测试".encode("gb2312"))
        with open("invalid_json", "wb") as f:
            f.write("test".encode("utf8"))
        temp_dict = """
# -*- coding: utf-8 -*-
from vocabtool.dict import base_class

class TestDict(base_class.SuperEntry):

    def __init__(self, dict_info, word_text):
        base_class.SuperEntry.__init__(self, dict_info["id"],
                                       dict_info["dictionary_name"],
                                       word_text)
        self.base_url = dict_info["base_url"]

    def lookup(self):
        pass

    def show_no_style(self):
        return "pass"

    show_with_style = show_no_style


def lookup(dict_info, word_text):
    result = TestDict(dict_info, word_text)
    result.lookup()
    return result

"""
        with open("dict/test_dict.py", "w") as f:
            f.write(temp_dict)

    def tearDown(self):
        os.remove("valid_config")
        os.remove("non_utf8")
        os.remove("invalid_json")
        os.remove("dict/test_dict.py")

    def test_init_with_existing_config_file(self):
        instance = core.VocabTool(config_filename="valid_config")
        self.assertIn("dictionaries", instance.config.keys())

    def test_init_with_non_existing_config_file(self):
        self.assertRaisesRegex(core.ConfigError,
                               "Configuration file not found",
                               core.VocabTool,
                               config_filename="no file")

    def test_init_with_config_file_of_non_utf8_encoding(self):
        self.assertRaisesRegex(core.ConfigError,
                               "Config file is not encoded with utf-8",
                               core.VocabTool,
                               config_filename="non_utf8")

    def test_init_with_config_file_of_invalid_json_format(self):
        self.assertRaisesRegex(core.ConfigError,
                               "Configuration is not valid json format",
                               core.VocabTool,
                               config_filename="invalid_json")


class TestCoreConfig(unittest.TestCase):
    """Test case for the config components of core"""

    def setUp(self):
        valid_config_string = """{
                                    "dictionaries": {
                                        "test_dict": {
                                            "base_url": "Test base_url",
                                            "dictionary_name": "Test Dict",
                                            "enable": true,
                                            "id": "test_dict",
                                            "lang": "en"
                                        }
                                    }
                                 }
                              """

        with open("valid_config", "wb") as f:
            f.write(valid_config_string.encode("utf8"))
        temp_dict = """
# -*- coding: utf-8 -*-
from vocabtool.dict import base_class

class TestDict(base_class.SuperEntry):

    def __init__(self, dict_info, word_text):
        base_class.SuperEntry.__init__(self, dict_info["id"],
                                       dict_info["dictionary_name"],
                                       word_text)
        self.base_url = dict_info["base_url"]

    def lookup(self):
        pass

    def show_no_style(self):
        return "pass"

    show_with_style = show_no_style


def lookup(dict_info, word_text):
    result = TestDict(dict_info, word_text)
    result.lookup()
    return result

"""
        with open("dict/test_dict.py", "w") as f:
            f.write(temp_dict)
        self.vt = core.VocabTool(config_filename="valid_config")

    def tearDown(self):
        os.remove("valid_config")
        os.remove("dict/test_dict.py")

    def test_read_config_valid(self):
        self.assertEqual(self.vt.read_config("dictionaries.test_dict.lang"),
                         "en")

    def test_read_config_invalid(self):
        self.assertRaisesRegex(core.ConfigError,
                               "Configuration does not exist",
                               self.vt.read_config,
                               "dictionaries.test_dict.some_config")

    def test_write_config_valid(self):
        self.vt.write_config("dictionaries.test_dict.lang", "de")
        self.assertEqual(self.vt.config["dictionaries"]["test_dict"]["lang"],
                         "de")


class TestCoreLookUp(unittest.TestCase):
    """Test case for core's components related to looking up words"""

    def setUp(self):
        valid_config_string = """{
                                    "dictionaries": {
                                        "test_dict": {
                                            "base_url": "foo bar",
                                            "dictionary_name": "Test Dict",
                                            "enable": true,
                                            "id": "test_dict",
                                            "lang": "en"
                                        }
                                    }
                                 }
                              """
        with open("valid_config", "wb") as f:
            f.write(valid_config_string.encode("utf8"))
        temp_dict = """
# -*- coding: utf-8 -*-
from vocabtool.dict import base_class

class TestDict(base_class.SuperEntry):

    def __init__(self, dict_info, word_text):
        base_class.SuperEntry.__init__(self, dict_info["id"],
                                       dict_info["dictionary_name"],
                                       word_text)
        self.base_url = dict_info["base_url"]

    def lookup(self):
        pass

    def show_no_style(self):
        return "pass"

    show_with_style = show_no_style


def lookup(dict_info, word_text):
    result = TestDict(dict_info, word_text)
    result.lookup()
    return result

"""
        with open("dict/test_dict.py", "w") as f:
            f.write(temp_dict)
        self.instance = core.VocabTool(config_filename="valid_config")

    def tearDown(self):
        os.remove("valid_config")
        os.remove("dict/test_dict.py")

    def test_lookup_invalid_word(self):
        result = self.instance.look_up_word("ttt", "en")
        self.assertEqual(result[0].show_no_style(), "pass")

    def test_lookup_invalid_language(self):
        result = self.instance.look_up_word("ttt", "aa")
        self.assertFalse(result)

    def test_lookup_empty_source_list(self):
        result = self.instance.look_up_word("ttt", "en", [])
        self.assertEqual(result[0].show_no_style(), "pass")

    def test_lookup_source_list_not_match(self):
        result = self.instance.look_up_word("ttt", "en", ["foo"])
        self.assertFalse(result)


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
