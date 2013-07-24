#!/usr/bin/env python

from distutils.core import setup

setup(name='GaPi',
      version='1.0',
      description='Google API for Google app engine',
      author='Robin Gottfried',
      author_email='google@kebet.cz',
      url='https://github.com/czervenka/gapi',
      packages=['gapi'],
      scripts=['convert_key.py'],
      requires=['PyCrypto'],
     )
