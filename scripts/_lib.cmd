@echo off
REM Shared env for every scripts\*.cmd. Call, do not run:
REM   call "%~dp0_lib.cmd"
REM   if errorlevel 1 exit /b 1
REM
REM Sets (override before call if you want):
REM   REPO         repo root
REM   PY           python launcher  (py -3 | python | python3)
REM   PIO          platformio       (pio | %PY% -m platformio)
REM   PIO_PROJECT  firmware dir     (%REPO%\firmware)
REM
REM Extra args on p0 / pio / preview wrappers are forwarded unchanged.

for %%I in ("%~dp0..") do set "REPO=%%~fI"

if not defined PY (
  set "PY="
  where py >nul 2>&1
  if not errorlevel 1 set "PY=py -3"
)
if not defined PY (
  where python >nul 2>&1
  if not errorlevel 1 set "PY=python"
)
if not defined PY (
  where python3 >nul 2>&1
  if not errorlevel 1 set "PY=python3"
)
if not defined PY (
  echo Python not found. Install Python 3 and retry, or set PY before calling this script.
  exit /b 1
)

if not defined PIO_PROJECT set "PIO_PROJECT=%REPO%\firmware"

if not defined PIO (
  set "PIO="
  where pio >nul 2>&1
  if not errorlevel 1 set "PIO=pio"
)
if not defined PIO set "PIO=%PY% -m platformio"

exit /b 0
