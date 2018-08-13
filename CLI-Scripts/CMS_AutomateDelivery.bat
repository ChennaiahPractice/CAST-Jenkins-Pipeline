@echo off

REM Parse passed in parameters
:parse
IF "%~1"=="" GOTO endparse
ECHO "%~1"| FIND /I "=" && SET "%~1"
SHIFT /1
GOTO parse
:endparse

if not defined profile (echo 'profile' parameter not provided) & goto ErrorExit
if not defined app (echo 'app' parameter not provided) & goto ErrorExit
if not defined version (echo 'fromVersion' parameter not provided) & goto ErrorExit
if not defined version (echo 'version' parameter not provided) & goto ErrorExit

set cli=C:/Program Files/CAST/8.2.8/CAST-MS-cli.exe
set log=c:/cast/logs/%app%

"%cli%" AutomateDelivery -connectionProfile %profile% -appli %app% -fromVersion "%fromVersion%" -version "%version%" -logRootPath %log%
exit /b %ERRORLEVEL%

:ErrorExit
exit /b 1
