@echo off
SET mypath=%~dp0
echo %mypath:~0,-1%
call %~dp0\venv\Scripts\activate && %~dp0\venv\Scripts\python -m pos-tagged
pause