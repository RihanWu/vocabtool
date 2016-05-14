# -*- coding: utf-8 -*-
"""Testing CLI module

Only supports Python 3.x now"""

import unittest

# Resolve import problem
import os
os.chdir("../")

from vocabtool import core


class TestCoreInit(unittest.TestCase):
    """Test case for the core class initializing process"""

    def setUp(self):
        valid_config_string = """{
                                    "dictionaries":
                                    [
                                        {
                                            "base_url": "http://dict.cn/",
                                            "dictionary_name": "海词词典",
                                            "enable": true,
                                            "id": "dict_cn",
                                            "lang": "en"
                                        }
                                    ]
                                 }
                              """
        with open("valid_config", "wb") as f:
            f.write(valid_config_string.encode("utf8"))
        with open("non_utf8", "wb") as f:
            f.write("测试".encode("gb2312"))
        with open("invalid_json", "wb") as f:
            f.write("test".encode("utf8"))

    def tearDown(self):
        os.remove("valid_config")
        os.remove("non_utf8")
        os.remove("invalid_json")

    def test_init_with_existing_config_file(self):
        instance = core.VocabTool(config_filename="valid_config")
        self.assertIn("dictionaries", instance.config.keys())

    def test_init_with_non_existing_config_file(self):
        self.assertRaisesRegex(core.ConfigError,
                               "Invalid config file name",
                               core.VocabTool, config_filename="no file")

    def test_init_with_config_file_of_non_utf8_encoding(self):
        self.assertRaisesRegex(core.ConfigError,
                               "Config file is not encoded with utf-8",
                               core.VocabTool, config_filename="non_utf8")

    def test_init_with_config_file_of_invalid_json_format(self):
        self.assertRaisesRegex(core.ConfigError,
                               "Configuration is not valid json format",
                               core.VocabTool, config_filename="invalid_json")

    def test_init_with_valid_config_string(self):
        config_string = """{
                                "dictionaries":
                                [
                                    {
                                        "base_url": "http://dict.cn/",
                                        "dictionary_name": "海词词典",
                                        "enable": true,
                                        "id": "dict_cn",
                                        "lang": "en"
                                    }
                                ]
                            }
                        """
        instance = core.VocabTool(config_string=config_string)
        self.assertIn("dictionaries", instance.config.keys())

    def test_init_with_invalid_json_config_string(self):
        config_string = "Invalid json string"
        self.assertRaisesRegex(core.ConfigError,
                               "Configuration is not valid json format",
                               core.VocabTool, config_string=config_string)


class TestCoreConfigLoadFromFile(unittest.TestCase):
    """Test case for the config components of core"""

    def setUp(self):
        self.instance = core.VocabTool()

    def tearDown(self):
        pass

    def test_load_config_from_file(self):
        self.instance.load_config(config_filename="sample-config.json")

        self.assertIn("dictionaries", self.instance.config.keys())
        self.assertFalse("Non Existing Item" in self.instance.config.keys())

    def test_load_config_no_input(self):
        self.assertRaisesRegex(core.ConfigError,
                               "No configuration provided",
                               self.instance.load_config)

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
