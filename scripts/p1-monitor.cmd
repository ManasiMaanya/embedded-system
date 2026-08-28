@echo off
cd /d "%~dp0..\firmware"
where pio >nul 2>&1
if %ERRORLEVEL%==0 (
  pio device monitor
  exit /b %ERRORLEVEL%
)
python -m platformio device monitor
exit /b %ERRORLEVEL%
