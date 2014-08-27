@echo off

cls

cd %HOMEPATH%\workspace\titan

del /s /q build

"c:\Python27\python.exe" setup.py build --compiler=mingw32
if %errorlevel% neq 0 exit /b %errorlevel%

copy build\lib.win32-2.7\*.* lib
