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
if not defined version (echo 'version' parameter not provided) & goto ErrorExit

set cli=C:/Program Files/CAST/8.3/CAST-MS-cli.exe
set log=c:/cast/logs/%app%

set snapshot=%date:~-4%%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2%%time:~6,2%
set snapshot2=%snapshot: =0%
rem 8.0 uses YYYYMMDDHHMMSS format for the capture date
rem 8.2 and above uses yyyyMMddHHmm format (no seconds)
set capture=%date:~-4%%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2%
set capture2=%capture: =0%

"%cli%" GenerateSnapshot -connectionProfile %profile% -appli %app% -snapshot "Computed on %snapshot2%" -captureDate %capture2% -version "%version%" -logRootPath %log%
exit /b %ERRORLEVEL%

:ErrorExit
exit /b 1
