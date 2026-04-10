@echo off
chcp 65001 >nul
title Test GUI
echo Testing DWG2KML GUI...
echo.

C:\Users\wnp\AppData\Local\CoPaw\python.exe -c "import dwg2kml_gui; import tkinter as tk; root = tk.Tk(); app = dwg2kml_gui.DWG2KMLGUI(root); print('GUI created successfully!'); root.mainloop()" 2>&1

echo.
echo Exit code: %ERRORLEVEL%
pause
