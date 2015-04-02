#!/usr/bin/env python

# Copyright (c) 2015, Yahoo Inc.
# Copyrights licensed under the BSD
# See the accompanying LICENSE.txt file for terms.
"""
test_pipr
----------------------------------

Tests for `pipr` module.
"""
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
        (filepath, requirements, debug) = pipr.get_and_parse_args(args)
        self.assertEqual(filepath, './')
        self.assertFalse(filepath == 'abc')
        self.assertTrue(requirements)
        self.assertTrue(debug)

    def test_get_all_imports(self):
        """Create a tempfile with imports and make sure we get them"""
        code_file = tempfile.NamedTemporaryFile(delete=False)
        code_file.write("from x import y\n")
        code_file.write("import abc\n")
        code_file.write("# import world")
        code_file.close()
        imports = pipr.get_all_imports(code_file.name)
        os.remove(code_file.name)
        self.assertNotEqual(len(imports), 0)
        self.assertEqual(len(imports), 2)
        self.assertEqual(imports[0], 'x')
        self.assertEqual(imports[1], 'abc')


if __name__ == '__main__':
    unittest.main()
