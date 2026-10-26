@echo off
rem Put Miniforge/conda on PATH when Explorer double-clicks a .bat (needs EnableDelayedExpansion)
call "%~dp0_find_conda_base.bat"
if defined CONDA_BASE if exist "!CONDA_BASE!\Scripts\conda.exe" (
  set "PATH=!CONDA_BASE!;!CONDA_BASE!\Scripts;!CONDA_BASE!\Library\bin;!CONDA_BASE!\condabin;!PATH!"
)
exit /b 0
