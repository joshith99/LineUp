@echo off
echo Building LineUp Professor App...
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM Build the executable
pyinstaller --onefile --windowed --name "LineUpProfessor" --icon=NONE professor_app.py

echo.
echo Build complete!
echo Executable location: dist\LineUpProfessor.exe
echo.
pause
