#!/usr/bin/env python

# Copyright (c) 2015, Yahoo Inc.
# Copyrights licensed under the BSD license
# See the accompanying LICENSE.txt file for terms.

from __future__ import absolute_import

import argparse
import ast
import logging
import os
import sys

import pkg_resources
import six


class PipMissingException(Exception):
    """Exception to be raised when pip is missing"""
    pass


# try importing pip
try:
    import pip
except ImportError:
    pip_url = "http://pip.readthedocs.org/en/latest/installing.html"
    raise PipMissingException("Please install pip first! You can follow the "
                              "directions here: {0}".format(pip_url))

PIP_VERSION = pkg_resources.parse_version(pkg_resources.get_distribution("pip").version)
# since pip 6.1.0, error output is in stderr instead of stdout
STDERR_PIP_VERSION = pkg_resources.parse_version("6.1.0")

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class WritableObject(object):
    """Object to redirect output (stdout and stderr) to"""

    def __init__(self):
        self.content = []

    def write(self, string):
        self.content.append(string)

    def flush(self):
        pass


class ImportParser(ast.NodeVisitor):
    """Object to parse a code file and collect all imports"""

    def __init__(self):
        # create a list to store all the imports we find
        self.imports = []

    def visit_Import(self, statement):
        """Find 'import x(,y)' types of statements"""
        for alias in statement.names:
            self.imports.append(alias.name)
        # continue parsing
        super(ImportParser, self).generic_visit(statement)

    def visit_ImportFrom(self, statement):
        """Find 'from x import y' types of statements"""
        # from x.y import z, then module is x
        if '.' in statement.module:
            module_name = statement.module.split('.')[0]
            self.imports.append(module_name)
        # from x import y, then module is x
        else:
            self.imports.append(statement.module)
        # continue parsing
        super(ImportParser, self).generic_visit(statement)


def get_and_parse_args(parser_args=None):
    """Setup and parse arguments"""
    # setup argparser and arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="The path to the Python file",
                        type=str, default=None)
    parser.add_argument("-r", "--requirements",
                        help=("Add --requirements to generate a "
                              "requirements.txt file in current directory"),
                        action="store_true")
    parser.add_argument("-d", "--debug",
                        help="Add --debug to see debug output",
                        action="store_true")
    parser.add_argument("-R", "--recursive",
                        help="Add --recursive to handle project-wide dependency",
                        action="store_true")
    # parse and save user arguments
    args = None
    if parser_args:
        args = parser.parse_args(parser_args)
    else:
        args = parser.parse_args()

    filepath = args.filepath
    requirements = args.requirements
    debug = args.debug
    recursive = args.recursive

    return (filepath, requirements, debug, recursive)


def get_all_imports(filepath):
    """Find all the imports in the user-specified file"""
    import_parser = ImportParser()
    with open(filepath) as code_file:
        code_node = ast.parse(code_file.read())
        import_parser.visit(code_node)

    logger.debug("Imported packages: " + ", ".join(import_parser.imports))

    return import_parser.imports


def install_missing_pkgs(imports):
    """Try to import all imports and pip install missing ones"""
    failed_pkgs = {}
    installed_pkgs = []

    # try to import every package needed
    # if we get ImportError, pip install the package
    for pkg in imports:
        try:
            __import__(pkg)
        except ImportError as imp_err:
            missing_module = imp_err.args[0].split()[-1].strip("'")

            # redirect stdout and stderr
            stdout_write_obj = WritableObject()
            stderr_write_obj = WritableObject()
            sys.stdout = stdout_write_obj
            sys.stderr = stderr_write_obj

            pip_ret = pip.main(["install", missing_module, "--upgrade",
                                "--quiet"])

            # return to default
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            # check pip return value
            if pip_ret:
                # remember this as a failed pkg and save reason
                # assuming last line of pip output is the error
                # since pip 6.1.0, error output is in stderr instead of stdout
                if PIP_VERSION >= STDERR_PIP_VERSION:
                    failed_pkgs[pkg] = stderr_write_obj.content[-1].strip(" \n")
                else:
                    failed_pkgs[pkg] = stdout_write_obj.content[-1].strip(" \n")
            else:
                version = pkg_resources.get_distribution(pkg).version
                installed_pkgs.append(missing_module + "==" + version)
        except Exception:  # ignore potential errors in imported packages
            continue

    return (failed_pkgs, installed_pkgs)


def report_failed_pkgs(failed_pkgs):
    """Report failed packages"""
    for pkg, reason in six.iteritems(failed_pkgs):
        logger.info("Failed to handle package \"{pkg}\" "
                    "because \"{reason}\"".format(pkg=pkg, reason=reason))


def report_installed_pkgs(installed_pkgs, requirements):
    """Report packages installed, create requirements.txt if user requested"""
    if installed_pkgs:
        logger.info("Missing packages installed: " + ", ".join(installed_pkgs))
        if requirements:  # user requested requirements.txt to be generated
            with open("requirements.txt", "w") as req_file:
                for pkg in installed_pkgs:
                    req_file.write(pkg + "\n")
    else:
        if requirements:
            logger.info("Did not install any new packages. Thus a "
                        "requirements.txt file was not generated")
        else:
            logger.info("Did not install any new packages")


if __name__ == "__main__":
    filepath, requirements, debug, recursive = get_and_parse_args()

    # set logger level
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if recursive:
        imports = []
        for root, subFolders, files in os.walk(filepath):
            for file in files:
                if file.endswith('.py'):
                    imports.extend(get_all_imports(os.path.join(root,file)))
    else:
        imports = get_all_imports(filepath)
    failed_pkgs, installed_pkgs = install_missing_pkgs(set(imports))
    report_failed_pkgs(failed_pkgs)
    report_installed_pkgs(installed_pkgs, requirements)
