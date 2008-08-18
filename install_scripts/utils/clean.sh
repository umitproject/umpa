#!/bin/bash

echo
echo "##################"
echo "     cleaning     "
echo "##################"
echo

old_pwd=`pwd`

script_dir=`pwd`/$0
script_dir=`dirname $script_dir`

cd $script_dir/../..
echo "Removing MANIFEST.."
rm -f MANIFEST
echo "Removing build directory.."
rm -rf build
echo "Removing dist directory.."
rm -rf dist
cd $old_pwd

echo "Done."
