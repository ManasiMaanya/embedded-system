@echo off
cd /d "%~dp0..\firmware"
where pio >nul 2>&1
if %ERRORLEVEL%==0 (
  pio run
  exit /b %ERRORLEVEL%
)
python -m platformio run
exit /b %ERRORLEVEL%
