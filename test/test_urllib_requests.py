# -*- coding: utf-8 -*-
"""Testing urllib_requests module

Only supports Python 3.x now"""

import unittest
from vocabtool import urllib_requests


class TestUrllibRequestsGet(unittest.TestCase):
    """Test case for urllib_requests get method"""

    def test_get_big5_specified(self):
        test_url = "https://s3.amazonaws.com/python.test/big5.txt"
        self.assertEqual(urllib_requests.get(test_url, codec="big5"),
                         "這是一段繁中文字\n")

    def test_get_big5_given(self):
        test_url = "https://s3.amazonaws.com/python.test/big5_given.txt"
        self.assertEqual(urllib_requests.get(test_url),
                         "這是一段繁中文字\n")

    def test_get_sjis_specified(self):
        test_url = "https://s3.amazonaws.com/python.test/sjis.txt"
        self.assertEqual(urllib_requests.get(test_url, codec="sjis"),
                         "これは日本語です。\n")

    def test_get_sjis_given(self):
        test_url = "https://s3.amazonaws.com/python.test/sjis_given.txt"
        self.assertEqual(urllib_requests.get(test_url),
                         "これは日本語です。\n")

    def test_get_sjis_wrong_header(self):
        test_url = "https://s3.amazonaws.com/python.test/sjis_wrong_header.txt"
        self.assertRaises(UnicodeDecodeError,
                          urllib_requests.get,
                          test_url)

    def test_get_sjis_ignore_wrong_header(self):
        test_url = "https://s3.amazonaws.com/python.test/sjis_wrong_header.txt"
        self.assertEqual(urllib_requests.get(test_url, codec="sjis"),
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
