@echo off
call "%~dp0_ensure_tool_root.bat"
set "CONDA_BASE="
if exist "%TOOL_ROOT%\.miniforge-base" set /p CONDA_BASE=<"%TOOL_ROOT%\.miniforge-base"
if not defined CONDA_BASE if exist "%TOOL_ROOT%\.conda-base" set /p CONDA_BASE=<"%TOOL_ROOT%\.conda-base"
if not defined CONDA_BASE (
  where conda >nul 2>nul
  if not errorlevel 1 for /f "delims=" %%G in ('conda info --base 2^>nul') do set "CONDA_BASE=%%G"
)
if not defined CONDA_BASE if exist "%USERPROFILE%\miniforge3\Scripts\conda.exe" set "CONDA_BASE=%USERPROFILE%\miniforge3"
if not defined CONDA_BASE if exist "%USERPROFILE%\Miniforge3\Scripts\conda.exe" set "CONDA_BASE=%USERPROFILE%\Miniforge3"
if not defined CONDA_BASE if exist "%LOCALAPPDATA%\miniforge3\Scripts\conda.exe" set "CONDA_BASE=%LOCALAPPDATA%\miniforge3"
if not defined CONDA_BASE if exist "C:\ProgramData\miniforge3\Scripts\conda.exe" set "CONDA_BASE=C:\ProgramData\miniforge3"
if not defined CONDA_BASE if exist "%USERPROFILE%\mambaforge\Scripts\conda.exe" set "CONDA_BASE=%USERPROFILE%\mambaforge"
if not defined CONDA_BASE if exist "%USERPROFILE%\Mambaforge\Scripts\conda.exe" set "CONDA_BASE=%USERPROFILE%\Mambaforge"
exit /b 0
