@echo off
REM P0: T(v) sim. Extra args go to sim\adaptive_threshold.py (try --help).
call "%~dp0_lib.cmd"
if errorlevel 1 exit /b 1
cd /d "%REPO%"
%PY% sim\adaptive_threshold.py %*
exit /b %ERRORLEVEL%
