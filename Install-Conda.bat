@echo off
rem 双击运行；路径含空格时请勿在 cmd 里裸写路径，请先 cd /d "解压目录" 或双击本文件
cd /d "%~dp0"
call "%~dp0windows\install-conda.bat"
