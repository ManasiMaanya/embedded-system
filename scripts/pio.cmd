@echo off
REM Generic PlatformIO front-end. Project: PIO_PROJECT (default firmware\).
REM Examples:
REM   scripts\pio.cmd run
REM   scripts\pio.cmd run -t upload
REM   scripts\pio.cmd device monitor
REM   scripts\pio.cmd run -e esp32dev
call "%~dp0_lib.cmd"
if errorlevel 1 exit /b 1
if "%~1"=="" (
  echo usage: scripts\pio.cmd ^<platformio arguments^>
  echo   scripts\pio.cmd run
  echo   scripts\pio.cmd run -t upload
  echo   scripts\pio.cmd device monitor
  echo Override project: set PIO_PROJECT=path ^& scripts\pio.cmd run
  exit /b 2
)
if not exist "%PIO_PROJECT%\platformio.ini" (
  echo No platformio.ini in "%PIO_PROJECT%"
  exit /b 1
)
cd /d "%PIO_PROJECT%"
%PIO% %*
exit /b %ERRORLEVEL%
