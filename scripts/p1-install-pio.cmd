@echo off
REM One-time PlatformIO CLI install. Extra args go to pip (e.g. --upgrade).
call "%~dp0_lib.cmd"
if errorlevel 1 exit /b 1
%PY% -m pip install --user platformio %*
echo.
echo Then open a new cmd so PATH picks up pio, or keep using:
echo   scripts\p1-build.cmd
echo ^(that wrapper already falls back to: %PY% -m platformio^)
exit /b %ERRORLEVEL%
