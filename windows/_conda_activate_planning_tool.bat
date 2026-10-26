@echo off
set "ENV_NAME=planning-tool"
call "%~dp0_find_conda_base.bat"
if not defined CONDA_BASE exit /b 1
if not exist "%CONDA_BASE%\Scripts\activate.bat" exit /b 1
call "%CONDA_BASE%\Scripts\activate.bat" %ENV_NAME%
if errorlevel 1 exit /b 1
exit /b 0
