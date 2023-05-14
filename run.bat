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
    START /B /wait "" scripts/python-3.10.0.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 InstallLauncherAllUsers=0
) 

START pythonw inject.pyw
exit