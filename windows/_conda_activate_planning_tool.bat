@echo off
set "ENV_NAME=planning-tool"

if exist "%~dp0..\.conda-base" set /p CONDA_BASE=<"%~dp0..\.conda-base"
if not defined CONDA_BASE for /f "delims=" %%G in ('conda info --base 2^>nul') do set "CONDA_BASE=%%G"
if not defined CONDA_BASE exit /b 1

if not exist "%CONDA_BASE%\Scripts\activate.bat" exit /b 1
call "%CONDA_BASE%\Scripts\activate.bat" %ENV_NAME%
if errorlevel 1 exit /b 1
exit /b 0
