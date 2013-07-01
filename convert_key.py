#!/usr/bin/env python
#
# Copyright 2007 Robin Gottfried <copyright@kebet.cz>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
__author__ = 'Robin Gottfried <google@kebet.cz>'

from os.path import basename
import sys

try:
    from OpenSSL.crypto import load_pkcs12, dump_privatekey, FILETYPE_PEM
except ImportError:
    print """OpenSSL library not found. Please install pyOpenSSL."""
    try:
        import pip
    except ImportError:
        pass
    else:
        print "I found that you have pip installed, would you like me to install pyOpenSSL for you? [y/n]"
        answer = raw_input()
        if answer.lower() in ['y', 'yes', 'yeah', 'yeah!']:
            pip.main(['install', 'pyOpenSSL'])
            print "\n\n\nOpenSSL library installed.\n\n\n"
        else:
            print "Exitting.\n\nYou must install pyOpenSSL manually to use this utility.\n(ie. by running `pip install pyOpenSSL`\n\n"

def _usage():
    print """USAGE: %s <pkcs12_file> [<pem_file>]
    pkcs12_file ... the key you downloaded from Google Console
    pem_file    ... the key to be used in this library

    If no pem_file is specified as argument, it will be written to std out.
""" % basename(sys.argv[0])

def _main():
    if len(sys.argv) < 2:
        _usage()
        sys.exit(1)
    archive = load_pkcs12(open(sys.argv[1], 'rb').read(), 'notasecret')
    key = archive.get_privatekey()
    pem = dump_privatekey(FILETYPE_PEM, key)
    if len(sys.argv) > 2:
        f = open(sys.argv[2], 'wb')
        f.write(pem)
        f.close()
    else:
        print pem

if __name__ == '__main__':
    _main()
