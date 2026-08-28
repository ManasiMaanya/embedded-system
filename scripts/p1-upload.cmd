@echo off
REM Alias: flash. Extra args: scripts\p1-upload.cmd --upload-port COM3
call "%~dp0pio.cmd" run -t upload %*
exit /b %ERRORLEVEL%
