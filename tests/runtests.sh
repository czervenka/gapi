#!/bin/sh

cd $(dirname $0)
nosetests -c nose.cfg "$@"
