#!/bin/bash

old_pwd=`pwd`
cur=`pwd`/$0
cur=`dirname $cur`
cd /tmp

rm -f .coverage 2>/dev/null
if [ $? -eq 1 ]; then
	echo "#### ERROR ####"
	echo "Can't remove /tmp/.coverage"
	echo "Please remove it manually first"
	echo "#### ERROR ####"
	exit 1
fi

if [ $# -gt 0 ]  && [ $1 == "-m" ]; then
	m=$1
	shift
else
	m=""
fi

echo "#### TESTS FOR UMPA [ START ] ####"
$cur/tests/coverage.py -x /usr/bin/py.test $* $cur/tests
echo "#### TESTS FOR UMPA [ FINISH ] ####"

echo "#### STATS FOR UMPA [ START ] ####"
$cur/tests/coverage.py -r $m --omit=/usr/lib,$cur/tests,$cur/py
echo "#### STATS FOR UMPA [ FINISH ] ####"
cd $old_pwd
