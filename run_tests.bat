@ echo off

cd %temp%
IF  Exist "coverage". (
	del /a:R coverage
)else (
	echo ERROR !!! Can't remove coverage.
	exit 1
)

IF %1 EQU -m (
	set m=%1
)else (
	set m=""
)

echo "#### TESTS FOR UMPA [ START ] ####"
%cur%/tests/coverage.py -x %cur%/py/bin/py.test %* %cur%/tests
echo "#### TESTS FOR UMPA [ FINISH ] ####"
%cur%/tests/coverage.py -r %m --omit=/usr/lib,%cur%/tests,%cur%/py 
echo "#### STATS FOR UMPA [ FINISH ] ####"
cd %cur%
