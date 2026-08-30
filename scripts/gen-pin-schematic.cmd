@echo off
call "%~dp0_lib.cmd"
if errorlevel 1 exit /b 1
%PY% "%REPO%\docs\images\circuit\gen_pin_schematic.py" %*
