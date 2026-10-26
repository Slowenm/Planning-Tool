@echo off
setlocal EnableExtensions EnableDelayedExpansion
call "%~dp0_ensure_tool_root.bat"
set "CONDA_BASE="

if exist "%TOOL_ROOT%\.miniforge-base" set /p CONDA_BASE=<"%TOOL_ROOT%\.miniforge-base"
if defined CONDA_BASE if exist "!CONDA_BASE!\envs\planning-tool\python.exe" goto :done
set "CONDA_BASE="
if exist "%TOOL_ROOT%\.conda-base" set /p CONDA_BASE=<"%TOOL_ROOT%\.conda-base"
if defined CONDA_BASE if exist "!CONDA_BASE!\envs\planning-tool\python.exe" goto :done
set "CONDA_BASE="

where conda >nul 2>nul
if not errorlevel 1 for /f "delims=" %%G in ('conda info --base 2^>nul') do set "CONDA_BASE=%%G"
if defined CONDA_BASE if exist "!CONDA_BASE!\envs\planning-tool\python.exe" goto :done
set "CONDA_BASE="

if exist "%USERPROFILE%\miniforge3\envs\planning-tool\python.exe" set "CONDA_BASE=%USERPROFILE%\miniforge3" & goto :done
if exist "%USERPROFILE%\Miniforge3\envs\planning-tool\python.exe" set "CONDA_BASE=%USERPROFILE%\Miniforge3" & goto :done
if exist "%LOCALAPPDATA%\miniforge3\envs\planning-tool\python.exe" set "CONDA_BASE=%LOCALAPPDATA%\miniforge3" & goto :done
if exist "C:\ProgramData\miniforge3\envs\planning-tool\python.exe" set "CONDA_BASE=C:\ProgramData\miniforge3" & goto :done
if exist "C:\Program Files\Miniforge3\envs\planning-tool\python.exe" set "CONDA_BASE=C:\Program Files\Miniforge3" & goto :done

where conda >nul 2>nul
if not errorlevel 1 for /f "delims=" %%G in ('conda info --base 2^>nul') do set "CONDA_BASE=%%G"
if not defined CONDA_BASE if exist "%USERPROFILE%\miniforge3\Scripts\conda.exe" set "CONDA_BASE=%USERPROFILE%\miniforge3"
if not defined CONDA_BASE if exist "C:\Program Files\Miniforge3\Scripts\conda.exe" set "CONDA_BASE=C:\Program Files\Miniforge3"

:done
set "CB=!CONDA_BASE!"
endlocal & set "CONDA_BASE=%CB%"
exit /b 0
