@echo off
echo ================================================
echo Building ALL executables
echo ================================================
echo.

REM Clean previous build
echo [1/5] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Check_All_Stage.exe del /f Check_All_Stage.exe
if exist update_script.exe del /f update_script.exe
echo Done!
echo.

REM Install/Update required packages
echo [2/5] Installing/Updating required packages...
pip install --upgrade pyinstaller pillow qrcode oracledb cx_Oracle
echo Done!
echo.

REM Build Check_All_Stage.exe
echo [3/5] Building Check_All_Stage.exe...
pyinstaller --clean Check_All_Stage.spec
if exist dist\Check_All_Stage.exe (
    copy dist\Check_All_Stage.exe Check_All_Stage.exe
    echo Check_All_Stage.exe - OK
) else (
    echo Check_All_Stage.exe - FAILED
    goto :error
)
echo.

REM Build update_script.exe
echo [4/5] Building update_script.exe...
pyinstaller --clean update_script.spec
if exist dist\update_script.exe (
    copy dist\update_script.exe update_script.exe
    echo update_script.exe - OK
) else (
    echo update_script.exe - FAILED
    goto :error
)
echo.

REM Summary
echo [5/5] Build summary...
echo.
echo ================================================
echo BUILD SUCCESSFUL - ALL FILES READY!
echo ================================================
echo.
echo Check_All_Stage.exe:
dir Check_All_Stage.exe | find "Check_All_Stage.exe"
echo.
echo update_script.exe:
dir update_script.exe | find "update_script.exe"
echo.
echo Note: Copy update_script.exe to program directory
echo Example: C:\Check_All_Stage\update_script.exe
echo.
goto :end

:error
echo.
echo ================================================
echo BUILD FAILED!
echo ================================================
echo Check the output above for errors.
echo.

:end
echo Press any key to exit...
pause > nul
