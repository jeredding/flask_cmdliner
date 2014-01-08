#cmdliner_tests.py
# WRITTEN FOR PYTHON3

import os
import cmdliner
import unittest
import tempfile


class CmdlinerTestCase(unittest.TestCase):
    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data
