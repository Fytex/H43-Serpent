@echo off
setlocal EnableDelayedExpansion

set NO_PYTHON=F

python --version 2>NUL
if errorlevel 1 (
    set NO_PYTHON=T
) else (
    for /f "delims=" %%i in ('python -c "import sys; print(int(sys.version_info >= (3, 7)))"') do set PYTHON_VERSION=%%i
    if !PYTHON_VERSION!==0 set NO_PYTHON=T
)

if "%NO_PYTHON%"=="T" (
    reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set FILE=scripts/python-installer.exe || set FILE=scripts/python-installer-amd64.exe
    START /B /wait "" !FILE! /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 InstallLauncherAllUsers=0
) 


:: After python instalation we need to open PowerShell and get the new environment variables to call python
powershell "$Env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User'); start pythonw -Args inject.pyw"
exit