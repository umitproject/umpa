#!/bin/sh

old_pwd=`pwd`

script_dir=`pwd`/$0
script_dir=`dirname $script_dir`

cd $script_dir/../..

rm -fr docs/API/*
epydoc -v --html -o docs/API -n UMPA -u http://umpa.umitproject.org umpa

cd $old_pwd
