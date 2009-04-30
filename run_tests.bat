@ echo off

mode con: cols=150 lines=50
cls

rem cd %temp%
rem IF  Exist "coverage". (
rem 	del /a:R coverage
rem )else (
rem 	echo ERROR !!! Can't remove coverage.
rem	exit 1
rem )

rem IF %1 EQU -m (
rem 	set m=%1
rem )else (
rem 	set m=""
rem )

echo "#### TESTS FOR UMPA [ START ] ####"
rem %cur%/tests/coverage.py -x %cur%/py/bin/py.test %* %cur%/tests
py\bin\win32\py.test tests
echo "#### TESTS FOR UMPA [ FINISH ] ####"

rem echo "#### STATS FOR UMPA [ START ] ####"
rem %cur%/tests/coverage.py -r %m --omit=/usr/lib,%cur%/tests,%cur%/py 
rem echo "#### STATS FOR UMPA [ FINISH ] ####"
rem cd %cur%
