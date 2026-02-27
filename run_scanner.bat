@echo off
setlocal

:: VULNETT SECURITY SYSTEMS - RUNTIME GATEWAY
title Vulnett Scanner

echo [*] Starting Vulnett Security Gateway...

:: Check for venv
if not exist ".venv\Scripts\python.exe" (
    echo [!] Virtual environment not found. Running setup first...
    call setup.bat
)

:: Run scanner using the venv python
echo [*] Activating environment and launching scanner...
".venv\Scripts\python.exe" scanner.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Scanner exited with code %ERRORLEVEL%.
    pause
)
