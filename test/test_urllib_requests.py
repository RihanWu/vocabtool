# -*- coding: utf-8 -*-
"""Testing urllib_requests module

Only supports Python 3.x now"""

import unittest
from vocabtool import urllib_requests


class TestUrllibRequestsGet(unittest.TestCase):
    """Test case for urllib_requests get method"""

    def setUp(self):
        base_url = "https://s3.amazonaws.com/python.test/"

        # Response headers don't contain charset
        self.url_big5 = base_url + "big5.txt"
        self.url_sjis = base_url + "sjis.txt"
        self.url_utf8 = base_url + "utf8.txt"

        # Response headers contain charset
        self.url_big5_given = base_url + "big5_given.txt"
        self.url_sjis_given = base_url + "sjis_given.txt"
        self.url_utf8_given = base_url + "utf8_given.txt"

        # Response header contain wrong charset
        self.url_sjis_wrong_header = base_url + "sjis_wrong_header.txt"

    def tearDown(self):
        pass

    def test_get_specified(self):
        self.assertEqual(urllib_requests.get(self.url_big5, codec="big5"),
                         "這是一段繁中文字\n")
        self.assertEqual(urllib_requests.get(self.url_sjis, codec="sjis"),
                         "これは日本語です。\n")
        self.assertEqual(urllib_requests.get(self.url_utf8, codec="utf-8"),
                         "这是个UTF-8测试\n")

    def test_get_unspecified(self):
        self.assertRaises(UnicodeDecodeError,
                          urllib_requests.get,
                          self.url_big5)
        self.assertRaises(UnicodeDecodeError,
                          urllib_requests.get,
                          self.url_sjis)
        self.assertEqual(urllib_requests.get(self.url_utf8),
                         "这是个UTF-8测试\n")

    def test_get_given(self):
        self.assertEqual(urllib_requests.get(self.url_big5_given),
                         "這是一段繁中文字\n")
        self.assertEqual(urllib_requests.get(self.url_sjis_given),
                         "これは日本語です。\n")
        self.assertEqual(urllib_requests.get(self.url_utf8_given),
                         "这是个UTF-8测试\n")

    def test_get_wrong_header(self):
        self.assertRaises(UnicodeDecodeError,
                          urllib_requests.get,
                          self.url_sjis_wrong_header)

    def test_get_sjis_ignore_wrong_header(self):
        self.assertEqual(urllib_requests.get(self.url_sjis_wrong_header,
                                             codec="sjis"),
                         "これは日本語です。\n")


class TestUrllibRequestUnzip(unittest.TestCase):
    """Test case for urllib_requests unzipping methods

    Includes:
        _gunzip
        _inflate"""

    def setUp(self):
        import gzip
        import zlib

        self.test_string_binary = "This is the test string.".encode("utf-8")
        self.compressed_gzip = gzip.compress(self.test_string_binary)
        self.compressed_zlib = zlib.compress(self.test_string_binary)

    def tearDown(self):
        pass

    def test__gunzip(self):
        self.assertEqual(urllib_requests._gunzip(self.compressed_gzip),
                         self.test_string_binary)

    def test__gunzip_type_error_string(self):
        self.assertRaises(TypeError, urllib_requests._gunzip, "Test")

    def test__inflate(self):
        self.assertEqual(urllib_requests._inflate(self.compressed_zlib),
                         self.test_string_binary)

    def test__inflate_type_error_string(self):
        self.assertRaises(TypeError, urllib_requests._inflate, "Test")


if __name__ == "__main__":
    unittest.main()
