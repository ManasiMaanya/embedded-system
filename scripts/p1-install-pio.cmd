@echo off
REM One-time: install PlatformIO CLI with the Python on PATH.
python -m pip install --user platformio
echo.
echo Then close this window, open a new cmd, and run scripts\p1-build.cmd
echo If pio is still missing, try: python -m platformio run -d firmware
exit /b %ERRORLEVEL%
