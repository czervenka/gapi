#!/bin/sh

cd $(dirname $0)
NOSE='nosetests -c nose.cfg'
nosetests -c nose.cfg "$@"
