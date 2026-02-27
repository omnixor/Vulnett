@echo off
setlocal enabledelayedexpansion

:: VULNETT SECURITY SYSTEMS - WINDOWS QUICK INSTALLER
title Vulnett Installer

echo ============================================================
echo      VULNETT SECURITY SYSTEMS - AUTOMATIC DEPLOYMENT
echo ============================================================
echo.

:: 1. Elevate if necessary (Optional, but helps with system installs)
:: Most users run as admin, but setup.ps1 handles many checks.

:: 2. Execute the PowerShell setup script with the correct bypass policy
echo [*] Launching PowerShell environment initialization...
powershell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Installation failed with error code %ERRORLEVEL%.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ============================================================
echo      INSTALLATION SUCCESSFUL
echo ============================================================
echo.
echo You can now start the scanner by running 'run_scanner.bat'
echo or by activating the environment in PowerShell.
echo.
pause
