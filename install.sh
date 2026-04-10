#!/bin/bash
echo "========================================"
echo "DWG2KML Converter - 安装脚本"
echo "========================================"
echo ""

echo "[1/3] 安装 ezdxf (DXF 文件解析库)..."
pip install ezdxf -q
if [ $? -ne 0 ]; then
    echo "警告：ezdxf 安装失败，请手动运行：pip install ezdxf"
fi

echo "[2/3] 安装 simplekml (KML 文件生成库)..."
pip install simplekml -q
if [ $? -ne 0 ]; then
    echo "警告：simplekml 安装失败，请手动运行：pip install simplekml"
fi

echo "[3/3] 安装 pyproj (可选，用于 UTM 坐标转换)..."
pip install pyproj -q
if [ $? -ne 0 ]; then
    echo "提示：pyproj 安装失败，UTM 坐标转换功能将不可用"
    echo "如需要 UTM 转换，请手动运行：pip install pyproj"
fi

echo ""
echo "========================================"
echo "安装完成！"
echo "========================================"
echo ""
echo "使用方法:"
echo "  python dwg2kml.py input.dxf -o output.kml"
echo "  python dwg2kml.py --help 查看完整帮助"
echo ""
echo "注意：DWG 文件需要先在 AutoCAD 中导出为 DXF 格式"
echo "      或使用 ODA File Converter 转换"
echo ""
