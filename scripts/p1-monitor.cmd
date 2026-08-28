@echo off
REM Alias: serial. Extra args: scripts\p1-monitor.cmd --port COM3 --baud 115200
call "%~dp0pio.cmd" device monitor %*
exit /b %ERRORLEVEL%
