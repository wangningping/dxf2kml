#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建示例 DXF 文件
用于测试 DXF to KML 转换器
"""

import ezdxf
from ezdxf import units

def create_sample_dxf(filename, description="Sample DXF for testing"):
    """创建一个包含基本实体的 DXF 文件"""
    
    # 创建新文档
    doc = ezdxf.new()
    
    # 设置元数据
    doc.header['$INSUNITS'] = 6  # Meters
    
    # 获取模型空间
    msp = doc.modelspace()
    
    # 添加一些示例实体（使用 CGCS2000 坐标 - 北京地区）
    # 坐标原点附近，方便测试
    
    # 1. 添加直线
    msp.add_line((0, 0), (100, 100), dxfattribs={'color': 1})
    msp.add_line((0, 100), (100, 0), dxfattribs={'color': 2})
    
    # 2. 添加矩形
    msp.add_lwpolyline([
        (200, 0),
        (300, 0),
        (300, 100),
        (200, 100),
        (200, 0)
    ], dxfattribs={'color': 3})
    
    # 3. 添加圆
    msp.add_circle((150, 50), radius=30, dxfattribs={'color': 4})
    
    # 4. 添加圆弧
    msp.add_arc((400, 50), radius=40, start_angle=0, end_angle=180, dxfattribs={'color': 5})
    
    # 5. 添加点
    msp.add_point((500, 50), dxfattribs={'color': 6})
    msp.add_point((500, 100), dxfattribs={'color': 6})
    msp.add_point((500, 150), dxfattribs={'color': 6})
    
    # 6. 添加文字
    msp.add_text(
        "DXF to KML Test Drawing",
        dxfattribs={
            'height': 10,
            'color': 7,
            'insert': (50, 200),
        }
    )
    
    # 7. 添加多段线（模拟道路或河流）
    points = [
        (600, 0),
        (620, 20),
        (640, 10),
        (660, 30),
        (680, 20),
        (700, 40)
    ]
    msp.add_lwpolyline(points, dxfattribs={'color': 1, 'lineweight': 25})
    
    # 8. 添加注释块
    block = doc.blocks.new(name='ANNOTATION')
    block.add_circle((0, 0), radius=5, dxfattribs={'color': 1})
    block.add_text("★", dxfattribs={'height': 8, 'color': 1})
    
    # 在模型空间中插入块
    msp.add_blockref('ANNOTATION', (400, 200))
    
    # 保存文件
    doc.saveas(filename)
    print(f"[OK] Created sample DXF file: {filename}")
    print(f"  - Entities: {len(msp)}")
    print(f"  - Coordinate range: X(0-700), Y(0-200)")
    print(f"  - Coordinate system: CGCS2000 (Beijing area, Central Meridian 117 deg E)")
    print(f"  - Units: Meters")


def create_grid_dxf(filename, grid_size=1000, spacing=100):
    """创建网格 DXF 文件"""
    
    doc = ezdxf.new()
    doc.header['$INSUNITS'] = 6  # Meters
    msp = doc.modelspace()
    
    # 创建网格
    for i in range(0, grid_size + 1, spacing):
        # 垂直线
        msp.add_line((i, 0), (i, grid_size), dxfattribs={'color': 8})
        # 水平线
        msp.add_line((0, i), (grid_size, i), dxfattribs={'color': 8})
    
    # 添加边界
    msp.add_lwpolyline([
        (0, 0),
        (grid_size, 0),
        (grid_size, grid_size),
        (0, grid_size),
        (0, 0)
    ], dxfattribs={'color': 1, 'lineweight': 35})
    
    # 保存
    doc.saveas(filename)
    print(f"[OK] Created grid DXF file: {filename}")
    print(f"  - Grid size: {grid_size}m x {grid_size}m")
    print(f"  - Grid spacing: {spacing}m")


def main():
    """Main function"""
    print("=" * 60)
    print("  Creating DXF to KML Converter Sample Files")
    print("=" * 60)
    print()
    
    # Create sample files
    create_sample_dxf("examples/sample_basic.dxf")
    print()
    
    # Create grid file
    create_grid_dxf("examples/sample_grid.dxf", grid_size=500, spacing=50)
    print()
    
    print("=" * 60)
    print("  Sample files created successfully!")
    print("=" * 60)
    print()
    print("Usage examples:")
    print("  python dwg2kml.py examples/sample_basic.dxf -o output.kml")
    print("  python dwg2kml.py examples/sample_basic.dxf -o output.kml --cgcs2000-3deg 39")
    print()
    print("Or use GUI:")
    print("  python dwg2kml_gui.py")
    print()


if __name__ == '__main__':
    main()
