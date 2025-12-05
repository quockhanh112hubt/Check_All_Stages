@echo off
echo ========================================
echo Building update_script.exe
echo ========================================
echo.

REM Clean previous build
echo [1/3] Cleaning previous build...
if exist build\update_script rmdir /s /q build\update_script
if exist dist\update_script.exe del /f dist\update_script.exe
echo Done!
echo.

REM Build with PyInstaller
echo [2/3] Building update_script.exe with PyInstaller...
pyinstaller --clean update_script.spec
echo Done!
echo.

REM Check result
echo [3/3] Checking build result...
if exist dist\update_script.exe (
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Executable location: dist\update_script.exe
    echo Size: 
    dir dist\update_script.exe | find "update_script.exe"
    echo.
    echo Note: Copy this file to program directory
    echo Recommended: C:\Check_All_Stage\update_script.exe
    echo.
) else (
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo.
    echo Check the output above for errors.
    echo.
)

echo Press any key to exit...
pause > nul
