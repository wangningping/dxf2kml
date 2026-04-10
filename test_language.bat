@echo off
chcp 65001 >nul
title Test Language Switch

echo ========================================
echo DXF to KML Converter - Language Test
echo ========================================
echo.
echo Starting GUI in Chinese mode...
echo.

start "" "C:\Users\wnp\AppData\Local\CoPaw\python.exe" dwg2kml_gui.py

echo GUI started!
echo.
echo Please test language switching:
echo 1. Click "Language / 语言" menu
echo 2. Select "English" or "简体中文"
echo 3. Check if all text changes
echo.
echo Window title and menu should now update correctly!
echo.
pause
