@echo off
title Video Player App
color 0A

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if required directories exist
if not exist "static\content" mkdir "static\content"
if not exist "static\subtitles" mkdir "static\subtitles"

:: Check if required packages are installed
python -c "import flask" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installing required packages...
    pip install flask
)

echo Starting Video Player App...
echo Server will be available at http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

:: Start the Flask app
python app.py

pause 