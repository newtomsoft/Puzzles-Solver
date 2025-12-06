@echo off
echo ========================================
echo Building PuzzleSolver Executable
echo ========================================
echo.

REM Clean previous builds
if exist "dist\PuzzleSolver" (
    echo Cleaning previous build...
    rmdir /s /q "dist\PuzzleSolver"
)

if exist "build" (
    rmdir /s /q "build"
)

echo.
echo Building executable with PyInstaller...
pyinstaller --clean PuzzleGUI.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo ========================================
    echo.
    echo Executable location: dist\PuzzleSolver\PuzzleSolver.exe
    echo.
    echo IMPORTANT: Before running the executable, you need to:
    echo 1. Install Playwright browsers: playwright install chromium
    echo 2. Copy any necessary .ini configuration files
    echo.
) else (
    echo.
    echo ========================================
    echo Build FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
)

pause
