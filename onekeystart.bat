@echo off
chcp 65001 >nul
title DWG2KML Converter
echo Starting DWG/DXF to KML Converter...
echo.

REM 使用 CoPaw Python 环境
set PYTHON_EXE=C:\Users\wnp\AppData\Local\CoPaw\python.exe

if exist "%PYTHON_EXE%" (
    "%PYTHON_EXE%" dwg2kml_gui.py
) else (
    python dwg2kml_gui.py
)

if errorlevel 1 (
    echo.
    echo Failed to start. Missing dependencies?
    echo Please run install.bat first
    echo.
    pause
)
