@echo off
pyinstaller --onefile -y --distpath ./build --icon=./icon.png main.pyw
del /F main.spec
cd build
copy /Y main.exe CherryBlossoms.scr
pause -1