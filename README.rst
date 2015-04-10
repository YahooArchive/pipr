pipr
******************************
Tool to pip install missing imports and more

Build Status
============
.. image:: https://img.shields.io/travis/yahoo/pipr.svg
        :target: https://travis-ci.org/yahoo/pipr

.. image:: https://coveralls.io/repos/yahoo/pipr/badge.svg
  :target: https://coveralls.io/r/yahoo/pipr

.. image:: https://pypip.in/download/pipr/badge.svg
    :target: https://pypi.python.org/pypi/pipr/
    
.. image:: https://pypip.in/version/pipr/badge.svg
   :target: https://pypi.python.org/pypi/pipr

.. image:: https://pypip.in/py_versions/pipr/badge.svg
    :target: https://pypi.python.org/pypi/pipr/

.. image:: https://pypip.in/license/pipr/badge.svg
    :target: https://pypi.python.org/pypi/pipr/

.. image:: https://readthedocs.org/projects/pipr/badge/?version=latest
    :target: http://pipr.readthedocs.org/en/latest/
    :alt: Documentation Status
 
Description
===========
pipr can install missing dependencies for any Python file and generate a requirements.txt file, so that YOU don't have to worry about searching for and installing the dependencies manually

Requirements
============
pipr currently requires Python 2.7, but we are working on supporting Python 3

Installation
============

To install pipr, simply:

.. code-block::

    $ pip install pipr

Usage
=====

.. code-block::

    $ pipr -h
    usage: pipr [-h] [-r] [-d] filepath

    positional arguments:
    filepath            The path to the Python file
    
    optional arguments:
        -h, --help          show this help message and exit
        -r, --requirements  Add --requirements to generate a requirements.txt
                            file in current directory
        -d, --debug         Add --debug to see debug output
        
.. code-block::

    $ cat test.py 
    import argparse
    import sshmap, redislite
    import urllib2
    import sbi
    # import commentimp
    from time import sleep
    '''
    import commentimp2
    '''
    
    $ pipr test.py -d -r
    Imported packages: argparse, sshmap, redislite, urllib2, sbi, time
    Missing packages installed: sshmap==0.6.90, sbi==0.0.7

Because we added -r, there will a requirements.txt file generated in the current directory.
   
More Information
================
* Free software: BSD license, see LICENSE.txt for details
* Documentation: https://pipr.readthedocs.org
* Contributing: We welcome pull requests! Please check CONTRIBUTING.md for requirements
* Contact information: ypython@yahoogroups.com
