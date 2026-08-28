@echo off
REM P0: closed-form T(v) sim. Run from anywhere; uses repo root.
cd /d "%~dp0.."
python sim\adaptive_threshold.py
exit /b %ERRORLEVEL%
