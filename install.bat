@echo off
echo ========================================
echo DWG2KML Converter - Install Script
echo ========================================
echo.
echo [1/3] Installing ezdxf...
pip install ezdxf -q -i https://pypi.tuna.tsinghua.edu.cn/simple
echo [2/3] Installing simplekml...
pip install simplekml -q -i https://pypi.tuna.tsinghua.edu.cn/simple
echo [3/3] Installing pyproj (for CGCS2000/UTM)...
pip install pyproj -q -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
echo ========================================
echo Done!
echo ========================================
echo.
echo Usage:
echo   python dwg2kml.py input.dxf -o output.kml
echo   python dwg2kml.py input.dxf --cgcs2000-3deg 39
echo   python dwg2kml.py --help
echo.
echo Note: DWG files must be converted to DXF first
echo.
pause
