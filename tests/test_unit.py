#!/usr/bin/env python

# Copyright (c) 2015, Yahoo Inc.
# Copyrights licensed under the BSD
# See the accompanying LICENSE.txt file for terms.
"""
test_pipr
----------------------------------

Tests for `pipr` module.
"""
from __future__ import absolute_import

import os
import tempfile
import unittest

import pipr


# Any methods of the class below that begin with "test" will be executed
# when the the class is run (by calling unittest.main()
class TestPipr(unittest.TestCase):
    """This class has functions to test the pipr module"""

    def test_parse_args(self):
        """Make sure we parse user arguments correctly"""
        args = ['./', '-r', '-d']
        (filepath, requirements, debug, recursive) = pipr.get_and_parse_args(args)
        self.assertEqual(filepath, './')
        self.assertFalse(filepath == 'abc')
        self.assertTrue(requirements)
        self.assertTrue(debug)
        self.assertFalse(recursive)
        (filepath, requirements, debug) = None, None, None
        try:
            (filepath, requirements, debug, recursive) = pipr.get_and_parse_args()
        except:
            self.assertFalse(requirements)
            self.assertFalse(debug)

    def test_get_all_imports(self):
        """Create a tempfile with imports and make sure we get them"""
        code_file = tempfile.NamedTemporaryFile(delete=False)
        code_file.write(
            "from x import y\n".encode('utf-8')
        )
        code_file.write(
            "from p.q import r\n".encode('utf-8')
        )
        code_file.write(
            "import abc\n".encode('utf-8')
        )
        code_file.write(
            "# import world".encode('utf-8')
        )
        code_file.close()
        imports = pipr.get_all_imports(code_file.name)
        os.remove(code_file.name)
        self.assertNotEqual(len(imports), 0)
        self.assertEqual(len(imports), 3)
        self.assertEqual(imports[0], 'x')
        self.assertEqual(imports[1], 'p')
        self.assertEqual(imports[2], 'abc')

    def test_install_missing_pkgs(self):
        """Make sure installed and un-installed packages are returned"""
        (failed_pkgs, installed_pkgs) = pipr.install_missing_pkgs(['nomodule'])
        self.assertTrue(isinstance(failed_pkgs, dict))
        self.assertTrue(isinstance(installed_pkgs, list))
        self.assertFalse(isinstance(installed_pkgs, dict))
        self.assertFalse(isinstance(failed_pkgs, list))
        self.assertEqual(len(failed_pkgs), 1)
        self.assertEqual(len(installed_pkgs), 0)


if __name__ == '__main__':
    unittest.main()
