@echo off
START /B /wait scripts/python-3.10.0.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 InstallLauncherAllUsers=0
START inject.pyw
exit