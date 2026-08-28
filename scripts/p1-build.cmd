@echo off
REM Alias: compile firmware. Extra args: scripts\p1-build.cmd -e esp32dev
call "%~dp0pio.cmd" run %*
exit /b %ERRORLEVEL%
