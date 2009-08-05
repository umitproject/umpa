#!/bin/sh

old_pwd=`pwd`

script_dir=`pwd`/$0
script_dir=`dirname $script_dir`

cd $script_dir/..

echo "Generating API docs..."
rm -fr docs/API/*
epydoc -v --html -o docs/API -n UMPA -u http://umpa.umitproject.org umit

echo "\nGenerating tutorials..."
rm -fr docs/tutorials/*
sphinx-build -b html -d docs/doctrees docs/tutorials-src docs/tutorials

cd $old_pwd
