@echo off
REM Browser preview of any Markdown file. Extra args go to preview_md.py (--help).
call "%~dp0_lib.cmd"
if errorlevel 1 exit /b 1
cd /d "%REPO%"
if "%~1"=="" (
  %PY% scripts\preview_md.py docs\architecture.md
) else (
  %PY% scripts\preview_md.py %*
)
exit /b %ERRORLEVEL%
