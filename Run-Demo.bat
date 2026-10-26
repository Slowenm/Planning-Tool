@echo off
cd /d "%~dp0"
set "TOOL_ROOT=%CD%"
call "%TOOL_ROOT%\windows\run\run-demo.bat"
