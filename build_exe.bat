@echo off
echo ================================
echo Building Check_All_Stage.exe
echo ================================
echo.

REM Clean previous build
echo [1/4] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Check_All_Stage.exe del /f Check_All_Stage.exe
echo Done!
echo.

REM Install/Update required packages
echo [2/4] Installing/Updating required packages...
pip install --upgrade pyinstaller pillow qrcode oracledb cx_Oracle
echo Done!
echo.

REM Build with PyInstaller
echo [3/4] Building executable with PyInstaller...
pyinstaller --clean Check_All_Stage.spec
echo Done!
echo.

REM Copy exe to root folder
echo [4/4] Copying executable to root folder...
if exist dist\Check_All_Stage.exe (
    copy dist\Check_All_Stage.exe Check_All_Stage.exe
    echo Done!
    echo.
    echo ================================
    echo BUILD SUCCESSFUL!
    echo ================================
    echo.
    echo Executable location: Check_All_Stage.exe
    echo Size: 
    dir Check_All_Stage.exe | find "Check_All_Stage.exe"
    echo.
) else (
    echo ERROR: Build failed! Check the output above for errors.
    echo.
)

echo Press any key to exit...
pause > nul
