@echo off
rem Default: Outlook COM naive times follow PC system zone, then convert to East 8 for scheduling.
set "PLANNING_OUTLOOK_NAIVE_TZ=system"
if exist "%~dp0..\.outlook-tz" (
  set /p PLANNING_OUTLOOK_NAIVE_TZ=<"%~dp0..\.outlook-tz"
)
exit /b 0
