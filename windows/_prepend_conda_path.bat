@echo off
rem Makes conda available when .bat is double-clicked (Explorer PATH often lacks conda)
if exist "%~dp0..\.conda-base" (
  set /p _CB=<"%~dp0..\.conda-base"
  if exist "!_CB!\Scripts\conda.exe" (
    set "PATH=!_CB!;!_CB!\Scripts;!_CB!\Library\bin;!_CB!\condabin;!PATH!"
  )
)
exit /b 0
