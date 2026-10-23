@echo off
title Save conda path for double-click runs
cd /d "%~dp0\.."
where conda >nul 2>nul
if errorlevel 1 (
  echo Open this from Anaconda Prompt, then run again.
  pause
  exit /b 1
)
for /f "delims=" %%G in ('conda info --base') do echo %%G> "%CD%\.conda-base"
echo Saved to .conda-base:
type "%CD%\.conda-base"
pause
