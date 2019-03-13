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

REM Setup CAST environment
SET mypath=%~dp0
SET currPath=%mypath:~0,-1%
echo Current directory: "%currPath%"

call "%currPath%/setupCASTEnvironment.bat"
set cli=%CAST_HOME%/CAST-MS-cli.exe
set log=%CAST_LOG_ROOT%/%app%

"%cli%" AutomateDelivery -connectionProfile %profile% -appli %app% -fromVersion "%fromVersion%" -version "%version%" -logRootPath "%log%"
exit /b %ERRORLEVEL%

:ErrorExit
exit /b 1
