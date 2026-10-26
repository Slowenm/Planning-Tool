@echo off
cd /d "%~dp0"
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\internal\_tool_env.bat"
call "%TOOL_ROOT%\windows\internal\_set_outlook_tz.bat"
call "%TOOL_ROOT%\windows\internal\_conda_run.bat" python -m alm_planning_tool.cli --tasks examples\alm_task_export.csv --calendar none --report alm_schedule.md --ics alm_schedule.ics --planned-csv examples\alm_task_export_planned.csv
pause
