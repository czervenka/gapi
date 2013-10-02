#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='GaPi',
    version='1.0',
    description='Google API for Google app engine',
    author='Robin Gottfried',
    author_email='google@kebet.cz',
    url='https://github.com/czervenka/gapi',
    packages=['gapi'],
    scripts=['convert_key.py'],
    data_files=[
        ('tests', ('tests/test_generated_key.pem', 'tests/test_google_bundle.p12'))
    ],
    requires=['pycrypto'],
)
