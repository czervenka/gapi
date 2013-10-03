#!/usr/bin/env python
VERSION = (1, 0, 1)
from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def run(self):
        res = _install.run(self)
        print '''
Do not forget to enable pycrypto library in your app.yaml:

    libraries:
    - name: pycrypto
      version: latest
'''
        return res

setup(
    cmdclass={'install': install},

    name='GaPi',
    version='.'.join(map(str, VERSION)),
    description='Google API for Google app engine',
    author='Robin Gottfried',
    author_email='google@kebet.cz',
    url='https://github.com/czervenka/gapi',
    packages=['gapi'],
    install_requires=[
        'pycrypto',
    ],
    scripts=['convert_key.py'],
    data_files=[
        ('tests', ('tests/test_generated_key.pem', 'tests/test_google_bundle.p12'))
    ],
)
