##!/bin/sh

echo
echo "###################"
echo " building packages "
echo "###################"
echo

old_pwd=`pwd`

script_dir=`pwd`/$0
script_dir=`dirname $script_dir`

cd $script_dir/../..
echo "Creating API documentation..."
sh install_scripts/utils/create_docs.sh
echo "Building source packages..."
python setup.py sdist --formats=gztar,zip,bztar
echo "Building binary packages..."
python setup.py bdist --formats=gztar,zip,bztar,wininst
rm MANIFEST
cd $old_pwd
