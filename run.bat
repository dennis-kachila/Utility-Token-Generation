@echo off
REM Utility Token Generation runner script for Windows
REM This script activates the virtual environment and provides a menu to run different components

cd /d "%~dp0"
call utility\Scripts\activate.bat

:MENU
cls
echo ==========================================
echo   Utility Token Generation Project Runner
echo ==========================================
echo.
echo 1. Generate a Token
echo 2. Generate a Decoder Key
echo 3. Decrypt a Token
echo 4. Process Raw Token Data
echo 5. Visualize Token Data
echo 6. Run Component Tests
echo 7. Launch GUI Interface
echo 8. Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" (
    echo.
    echo Running Token Generator...
    echo.
    python main.py token
    echo.
    pause
    goto MENU
)

if "%choice%"=="2" (
    echo.
    echo Running Decoder Key Generator...
    echo.
    python main.py key
    echo.
    pause
    goto MENU
)

if "%choice%"=="3" (
    echo.
    echo Running Token Decrypter...
    echo.
    python main.py decrypt
    echo.
    pause
    goto MENU
)

if "%choice%"=="4" (
    echo.
    echo Running Data Cleaning...
    echo.
    python main.py clean
    echo.
    echo Data processed and saved to cleaned_meter_data.csv and cleaned_meter_data.xlsx
    echo.
    pause
    goto MENU
)

if "%choice%"=="5" (
    echo.
    echo Running Token Visualizer...
    echo.
    python main.py visualize
    echo.
    echo Visualization complete. Check the generated image files.
    echo.
    pause
    goto MENU
)

if "%choice%"=="6" (
    echo.
    echo Running Component Tests...
    echo.
    python main.py test
    echo.
    pause
    goto MENU
)

if "%choice%"=="7" (
    echo.
    echo Launching GUI Interface...
    echo.
    python main.py gui
    goto MENU
)

if "%choice%"=="8" (
    echo Exiting...
    rem Kill any running Python processes started by this script
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq Token.py" 2>nul
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq DKGA02.py" 2>nul
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq TokenDecrypter.py" 2>nul
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq data-cleaning.py" 2>nul
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq TokenVisualizer.py" 2>nul
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq test_components.py" 2>nul
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq UtilityTokenGUI.py" 2>nul
    call deactivate
    exit /b
)

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MENU
