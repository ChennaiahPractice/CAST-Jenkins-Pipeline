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
if not defined filepath (echo 'filepath' parameter not provided) & goto ErrorExit

REM Setup CAST environment
SET mypath=%~dp0
SET currPath=%mypath:~0,-1%
call "%currPath%/setupCASTEnvironment.bat"

set cli=%CAST_HOME%/CAST-MS-cli.exe
set log=%CAST_LOG_ROOT%/%app%

"%cli%" ImportAssessmentModel -connectionProfile %profile% -file "%filepath%" -logRootPath "%log%"
exit /b %ERRORLEVEL%

:ErrorExit
exit /b 1
