@echo off
REM Open a Markdown file in your browser (KaTeX + mermaid). Default: architecture.md
cd /d "%~dp0.."
if "%~1"=="" (
  python scripts\preview_md.py docs\architecture.md
) else (
  python scripts\preview_md.py %*
)
exit /b %ERRORLEVEL%
