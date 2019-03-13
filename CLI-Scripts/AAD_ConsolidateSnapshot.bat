@echo off

REM Parse passed in parameters
:parse
IF "%~1"=="" GOTO endparse
ECHO "%~1"| FIND /I "=" && SET "%~1"
SHIFT /1
GOTO parse
:endparse

if not defined measure (echo 'measure' parameter not provided) & goto ErrorExit
if not defined central (echo 'central' parameter not provided) & goto ErrorExit
if not defined password (echo 'password' parameter not provided) & goto ErrorExit

REM Setup CAST environment
SET mypath=%~dp0
SET currPath=%mypath:~0,-1%
call "%currPath%/setupCASTEnvironment.bat"

set cli=%CAST_HOME%/AAD/CLI/AadConsolidation.exe
set log=%CAST_LOG_ROOT%/%app%

"%cli%" -url %CAST_DB_URL% -schema %measure% -password %password% -remote_url %CAST_DB_URL% -remote_schema %central% -remote_password %password%"
exit /b %ERRORLEVEL%

:ErrorExit
exit /b 1