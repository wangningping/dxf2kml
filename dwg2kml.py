#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DWG/DXF to KML Converter
将 AutoCAD DWG/DXF 文件转换为 Google Earth KML 文件

支持坐标系：
- CGCS2000（中国大地坐标系 2000）
- UTM（通用横轴墨卡托投影）
- 简单基准点转换

作者：AI Assistant
日期：2026-04-09
"""

import os
import sys
import argparse
import math
from pathlib import Path

# 尝试导入必要的库
try:
    import ezdxf
    EZDXF_AVAILABLE = True
except ImportError:
    EZDXF_AVAILABLE = False
    print("Warning: ezdxf not installed. Please run: pip install ezdxf")

try:
    import simplekml
    SIMPLEKML_AVAILABLE = True
except ImportError:
    SIMPLEKML_AVAILABLE = False
    print("Warning: simplekml not installed. Please run: pip install simplekml")

try:
    from pyproj import Transformer
    PYPROJ_AVAILABLE = True
except ImportError:
    PYPROJ_AVAILABLE = False
    print("Note: pyproj not installed. CGCS2000/UTM conversion will not be available.")
    print("      Please run: pip install pyproj")


# CGCS2000 高斯 - 克吕格投影 EPSG 代码（按 3 度带）
# EPSG:4511 = 带 25 (75°E), EPSG:4512 = 带 26 (78°E), ...
# 公式：EPSG = 4486 + 带号
CGCS2000_3DEG_EPSG = {
    zone: 4486 + zone for zone in range(25, 46)
}

# CGCS2000 高斯 - 克吕格投影 EPSG 代码（按 6 度带）
# EPSG:4488 = 带 13 (75°E), EPSG:4489 = 带 14 (81°E), ...
# 公式：EPSG = 4475 + 带号
CGCS2000_6DEG_EPSG = {
    zone: 4475 + zone for zone in range(13, 46)
}

# CGCS2000 地理坐标系（经纬度）
CGCS2000_GEOG = 4490


class DWG2KMLConverter:
    """DWG/DXF 到 KML 的转换器"""
    
    def __init__(self, output_file="output.kml"):
        """
        初始化转换器
        
        Args:
            output_file: 输出的 KML 文件路径
        """
        self.output_file = output_file
        self.kml = None
        self.doc = None
        self.entities_count = 0
        
    def create_kml_document(self, name="CAD Drawing", description="Converted from DWG/DXF"):
        """创建 KML 文档"""
        if not SIMPLEKML_AVAILABLE:
            raise ImportError("simplekml not installed")
            
        self.kml = simplekml.Kml()
        # 直接设置根 Document 的名称和描述
        self.kml.document.name = name
        self.kml.document.description = description
        print(f"[OK] Created KML document: {name}")
        
    def convert_dxf_to_kml(self, dxf_file, coordinate_transform=None):
        """将 DXF 文件转换为 KML"""
        if not EZDXF_AVAILABLE:
            raise ImportError("ezdxf not installed")
        if not SIMPLEKML_AVAILABLE:
            raise ImportError("simplekml not installed")
            
        print(f"\nConverting: {dxf_file}")
        
        # 读取 DXF 文件
        doc = ezdxf.readfile(dxf_file)
        msp = doc.modelspace()
        
        # 如果没有指定坐标转换，使用默认转换
        if coordinate_transform is None:
            coordinate_transform = self.default_coordinate_transform
            
        # 遍历所有实体
        for entity in msp:
            try:
                self._convert_entity(entity, coordinate_transform)
            except Exception as e:
                print(f"  Skip entity {entity.dxftype()}: {e}")
                
        # 保存 KML 文件
        self.kml.save(self.output_file)
        print(f"\n[OK] Conversion complete! Output: {self.output_file}")
        print(f"     Entities converted: {self.entities_count}")
        
    def _convert_entity(self, entity, transform_func):
        """转换单个实体"""
        entity_type = entity.dxftype()
        
        if entity_type == 'LINE':
            self._convert_line(entity, transform_func)
        elif entity_type == 'POLYLINE' or entity_type == 'LWPOLYLINE':
            self._convert_polyline(entity, transform_func)
        elif entity_type == 'CIRCLE':
            self._convert_circle(entity, transform_func)
        elif entity_type == 'ARC':
            self._convert_arc(entity, transform_func)
        elif entity_type == 'POINT':
            self._convert_point(entity, transform_func)
        elif entity_type == 'TEXT' or entity_type == 'MTEXT':
            self._convert_text(entity, transform_func)
        elif entity_type == 'INSERT':
            self._convert_insert(entity, transform_func)
        else:
            pass
            
    def _convert_line(self, entity, transform_func):
        """转换 LINE 实体"""
        start = entity.dxf.start
        end = entity.dxf.end
        
        lat1, lon1 = transform_func(start.x, start.y)
        lat2, lon2 = transform_func(end.x, end.y)
        
        ls = self.kml.newlinestring(
            name=f"Line_{self.entities_count}",
            description=f"CAD Line from ({start.x:.2f}, {start.y:.2f}) to ({end.x:.2f}, {end.y:.2f})"
        )
        ls.coords = [(lon1, lat1), (lon2, lat2)]
        ls.style.linestyle.color = simplekml.Color.red
        ls.style.linestyle.width = 2
        
        self.entities_count += 1
        
    def _convert_polyline(self, entity, transform_func):
        """转换 POLYLINE/LWPOLYLINE 实体"""
        points = []
        cad_points = []
        
        try:
            if hasattr(entity, 'get_points'):
                raw_points = list(entity.get_points())
                for p in raw_points:
                    if len(p) >= 2:
                        cad_points.append((p[0], p[1]))
            else:
                for vertex in entity.vertices:
                    loc = vertex.dxf.location
                    cad_points.append((loc.x, loc.y))
        except Exception as e:
            print(f"  Polyline error: {e}")
            return
        
        for point in cad_points:
            try:
                x, y = point[0], point[1]
                lat, lon = transform_func(x, y)
                points.append((lon, lat))
            except Exception as e:
                continue
        
        if len(points) >= 2:
            ls = self.kml.newlinestring(
                name=f"Polyline_{self.entities_count}",
                description=f"CAD Polyline with {len(points)} points"
            )
            ls.coords = points
            ls.style.linestyle.color = simplekml.Color.blue
            ls.style.linestyle.width = 2
            
            self.entities_count += 1
            
    def _convert_circle(self, entity, transform_func):
        """转换 CIRCLE 实体"""
        center = entity.dxf.center
        radius = entity.dxf.radius
        
        lat, lon = transform_func(center.x, center.y)
        
        # 创建圆（多边形近似）
        points = []
        num_segments = 36
        for i in range(num_segments + 1):
            angle = math.radians(i * 360 / num_segments)
            delta_lat = (radius * math.sin(angle)) / 111320
            delta_lon = (radius * math.cos(angle)) / (111320 * math.cos(math.radians(lat)))
            points.append((lon + delta_lon, lat + delta_lat))
        
        poly = self.kml.newpolygon(
            name=f"Circle_{self.entities_count}",
            description=f"CAD Circle at ({center.x:.2f}, {center.y:.2f}), radius={radius:.2f}"
        )
        poly.outerboundaryis = points
        poly.style.linestyle.color = simplekml.Color.green
        poly.style.polystyle.color = '5000ff00'
        
        self.entities_count += 1
        
    def _convert_arc(self, entity, transform_func):
        """转换 ARC 实体"""
        center = entity.dxf.center
        radius = entity.dxf.radius
        start_angle = entity.dxf.start_angle
        end_angle = entity.dxf.end_angle
        
        lat, lon = transform_func(center.x, center.y)
        
        points = []
        num_segments = int(abs(end_angle - start_angle) / math.radians(5)) + 1
        num_segments = max(num_segments, 10)
        
        for i in range(num_segments + 1):
            angle = start_angle + (end_angle - start_angle) * i / num_segments
            delta_lat = (radius * math.sin(angle)) / 111320
            delta_lon = (radius * math.cos(angle)) / (111320 * math.cos(math.radians(lat)))
            points.append((lon + delta_lon, lat + delta_lat))
        
        if len(points) >= 2:
            ls = self.kml.newlinestring(
                name=f"Arc_{self.entities_count}",
                description=f"CAD Arc at ({center.x:.2f}, {center.y:.2f}), radius={radius:.2f}"
            )
            ls.coords = points
            ls.style.linestyle.color = simplekml.Color.yellow
            ls.style.linestyle.width = 2
            
            self.entities_count += 1
            
    def _convert_point(self, entity, transform_func):
        """转换 POINT 实体"""
        try:
            location = entity.dxf.location
            if hasattr(location, 'x'):
                x, y = location.x, location.y
            elif isinstance(location, (tuple, list)):
                x, y = location[0], location[1]
            else:
                return
            
            lat, lon = transform_func(x, y)
            
            pnt = self.kml.newpoint(
                name=f"Point_{self.entities_count}",
                description=f"CAD Point at ({x:.2f}, {y:.2f})"
            )
            pnt.coords = [(lon, lat)]
            
            self.entities_count += 1
        except Exception as e:
            print(f"  POINT error: {e}")
        
    def _convert_text(self, entity, transform_func):
        """转换 TEXT/MTEXT 实体"""
        try:
            insert = entity.dxf.insert
            if hasattr(insert, 'x'):
                x, y = insert.x, insert.y
            elif isinstance(insert, (tuple, list)):
                x, y = insert[0], insert[1]
            else:
                return
            
            text = entity.dxf.text if hasattr(entity.dxf, 'text') else str(entity)
            lat, lon = transform_func(x, y)
            
            pnt = self.kml.newpoint(
                name=f"Text_{self.entities_count}",
                description=text
            )
            pnt.coords = [(lon, lat)]
            
            self.entities_count += 1
        except Exception as e:
            print(f"  TEXT error: {e}")
            
    def _convert_insert(self, entity, transform_func):
        """转换 INSERT (块引用) 实体"""
        try:
            insert = entity.dxf.insert
            if hasattr(insert, 'x'):
                x, y = insert.x, insert.y
            elif isinstance(insert, (tuple, list)):
                x, y = insert[0], insert[1]
            else:
                return
            
            lat, lon = transform_func(x, y)
            
            pnt = self.kml.newpoint(
                name=f"Block_{entity.dxf.name}_{self.entities_count}",
                description=f"Block: {entity.dxf.name} at ({x:.2f}, {y:.2f})"
            )
            pnt.coords = [(lon, lat)]
            
            self.entities_count += 1
        except Exception as e:
            print(f"  INSERT error: {e}")
        
    def default_coordinate_transform(self, x, y):
        """默认坐标转换函数（简单基准点）"""
        base_lat = 39.9042
        base_lon = 116.4074
        lat = base_lat + y / 111320
        lon = base_lon + x / (111320 * math.cos(math.radians(base_lat)))
        return lat, lon


def create_cgcs2000_transformer(zone_3deg=None, zone_6deg=None, use_geog=False, central_meridian=None):
    """
    创建 CGCS2000 到 WGS84 的转换函数
    
    Args:
        zone_3deg: 3 度带带号 (25-45)
        zone_6deg: 6 度带带号 (13-45)
        use_geog: 是否使用地理坐标系（经纬度）
        central_meridian: 中央经线（度），优先使用此参数
        
    Returns:
        坐标转换函数 (easting, northing) -> (lon, lat)
    """
    if not PYPROJ_AVAILABLE:
        print("Error: pyproj not installed. Cannot create CGCS2000 transformer.")
        return None
    
    try:
        if use_geog:
            # CGCS2000 地理坐标系 -> WGS84
            transformer = Transformer.from_crs("EPSG:4490", "EPSG:4326", always_xy=True)
            print("[OK] Using CGCS2000 Geographic Coordinate System (EPSG:4490)")
            return lambda x, y: transformer.transform(x, y)  # x=easting(经度), y=northing(纬度)
            
        # 计算中央经线
        if central_meridian is None:
            if zone_3deg:
                central_meridian = zone_3deg * 3  # 3 度带
                print(f"[OK] Using CGCS2000 3-degree Gauss-Kruger zone {zone_3deg} (Central Meridian: {central_meridian}°E)")
            elif zone_6deg:
                central_meridian = zone_6deg * 6 - 3  # 6 度带
                print(f"[OK] Using CGCS2000 6-degree Gauss-Kruger zone {zone_6deg} (Central Meridian: {central_meridian}°E)")
            else:
                print("Error: Must specify zone_3deg, zone_6deg, central_meridian, or use_geog")
                return None
        
        # 使用 PROJ 字符串定义 CGCS2000 高斯 - 克吕格投影
        # CGCS2000 使用 GRS80 椭球
        proj_string = (
            f"+proj=tmerc +lat_0=0 +lon_0={central_meridian} +k=1 +x_0=500000 +y_0=0 "
            f"+ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        )
        
        transformer = Transformer.from_crs(proj_string, "EPSG:4326", always_xy=True)
        print(f"[OK] Central Meridian: {central_meridian}°E")
        # always_xy=True: 输入 (easting, northing), 输出 (lon, lat)
        # DXF 中：x=easting (东坐标), y=northing (北坐标)
        # 所以调用：transformer.transform(x, y) -> (lon, lat)
        # 返回 (lat, lon) 给调用者
        return lambda x, y: (lambda lon, lat: (lat, lon))(*transformer.transform(x, y))
            
    except Exception as e:
        print(f"Error creating CGCS2000 transformer: {e}")
        return None


def create_utm_transformer(zone_number, is_northern=True):
    """创建 UTM 坐标到 WGS84 的转换函数"""
    if not PYPROJ_AVAILABLE:
        print("Error: pyproj not installed.")
        return None
    
    try:
        epsg = 32600 + zone_number if is_northern else 32700 + zone_number
        transformer = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=False)
        print(f"[OK] Using UTM zone {zone_number} {'N' if is_northern else 'S'} (EPSG:{epsg})")
        return lambda x, y: transformer.transform(x, y)
    except Exception as e:
        print(f"Error creating UTM transformer: {e}")
        return None


def create_simple_transform(base_lat, base_lon):
    """创建简单坐标转换函数"""
    import math
    def transform(x, y):
        lat = base_lat + y / 111320
        lon = base_lon + x / (111320 * math.cos(math.radians(base_lat)))
        return lat, lon
    return transform


def batch_convert(input_folder, output_folder=None, coordinate_transform=None):
    """批量转换文件夹中的所有 DXF 文件"""
    input_path = Path(input_folder)
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path
        
    dxf_files = list(input_path.glob("*.dxf")) + list(input_path.glob("*.DXF"))
    
    if not dxf_files:
        print(f"No DXF files found in {input_folder}")
        return
        
    print(f"Found {len(dxf_files)} DXF files")
    
    for dxf_file in dxf_files:
        output_file = output_path / f"{dxf_file.stem}.kml"
        converter = DWG2KMLConverter(str(output_file))
        converter.create_kml_document(name=dxf_file.stem)
        converter.convert_dxf_to_kml(str(dxf_file), coordinate_transform)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='DWG/DXF to KML Converter - Convert AutoCAD files to Google Earth KML format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Coordinate System Options:

  CGCS2000 (China Geodetic Coordinate System 2000):
    --cgcs2000-3deg ZONE     Use 3-degree Gauss-Kruger zone (25-45)
    --cgcs2000-6deg ZONE     Use 6-degree Gauss-Kruger zone (13-45)
    --cgcs2000-geog          Use geographic coordinates (lat/lon)

  UTM (Universal Transverse Mercator):
    --utm-zone ZONE          UTM zone number
    --southern               Southern hemisphere (default: northern)

  Simple (for local coordinates in meters):
    --base-lat LAT           Base latitude (default: 39.9042)
    --base-lon LON           Base longitude (default: 116.4074)

Examples:
  python dwg2kml.py input.dxf -o output.kml
  python dwg2kml.py input.dxf --cgcs2000-3deg 39  # Beijing area
  python dwg2kml.py input.dxf --cgcs2000-6deg 20
  python dwg2kml.py input.dxf --utm-zone 50
  python dwg2kml.py --batch ./dxf_files --cgcs2000-3deg 39

Note:
  DWG is a proprietary format. Convert to DXF first using:
  - AutoCAD: DXFOUT command
  - ODA File Converter: https://www.opendesign.com/guestfiles/oda_file_converter
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input DXF file path')
    parser.add_argument('-o', '--output', default='output.kml', help='Output KML file path')
    parser.add_argument('-n', '--name', default='CAD Drawing', help='KML document name')
    parser.add_argument('--batch', help='Batch convert all DXF files in folder')
    
    # CGCS2000 options
    cgcs_group = parser.add_argument_group('CGCS2000 Options')
    cgcs_group.add_argument('--cgcs2000-3deg', type=int, metavar='ZONE',
                           help='CGCS2000 3-degree Gauss-Kruger zone (25-45)')
    cgcs_group.add_argument('--cgcs2000-6deg', type=int, metavar='ZONE',
                           help='CGCS2000 6-degree Gauss-Kruger zone (13-45)')
    cgcs_group.add_argument('--cgcs2000-geog', action='store_true',
                           help='CGCS2000 geographic coordinates (lat/lon)')
    
    # UTM options
    utm_group = parser.add_argument_group('UTM Options')
    utm_group.add_argument('--utm-zone', type=int, metavar='ZONE',
                          help='UTM zone number')
    utm_group.add_argument('--southern', action='store_true',
                          help='Southern hemisphere')
    
    # Simple options
    simple_group = parser.add_argument_group('Simple Options')
    simple_group.add_argument('--base-lat', type=float, default=39.9042,
                             help='Base latitude for simple conversion')
    simple_group.add_argument('--base-lon', type=float, default=116.4074,
                             help='Base longitude for simple conversion')
    
    args = parser.parse_args()
    
    # Check required libraries
    if not EZDXF_AVAILABLE:
        print("\nError: ezdxf not installed")
        print("Please run: pip install ezdxf")
        sys.exit(1)
        
    if not SIMPLEKML_AVAILABLE:
        print("\nError: simplekml not installed")
        print("Please run: pip install simplekml")
        sys.exit(1)
    
    # Batch mode
    if args.batch:
        transform_func = None
        
        if args.cgcs2000_3deg:
            # 3 度带：中央经线 = 带号 × 3
            central_meridian = args.cgcs2000_3deg * 3
            transform_func = create_cgcs2000_transformer(central_meridian=central_meridian)
        elif args.cgcs2000_6deg:
            # 6 度带：中央经线 = 带号 × 6 - 3
            central_meridian = args.cgcs2000_6deg * 6 - 3
            transform_func = create_cgcs2000_transformer(central_meridian=central_meridian)
        elif args.cgcs2000_geog:
            transform_func = create_cgcs2000_transformer(use_geog=True)
        elif args.utm_zone:
            transform_func = create_utm_transformer(args.utm_zone, not args.southern)
        else:
            transform_func = create_simple_transform(args.base_lat, args.base_lon)
            print(f"[OK] Using simple conversion (base: {args.base_lat}N, {args.base_lon}E)")
            
        if transform_func is None:
            print("Error: Failed to create coordinate transformer")
            sys.exit(1)
            
        batch_convert(args.batch, args.output if args.output != 'output.kml' else None, transform_func)
        return
    
    # Single file mode
    if not args.input:
        parser.print_help()
        print("\nError: Please specify input file or --batch option")
        sys.exit(1)
        
    # Determine transform function
    transform_func = None
    
    if args.cgcs2000_3deg:
        # 3 度带：中央经线 = 带号 × 3
        central_meridian = args.cgcs2000_3deg * 3
        transform_func = create_cgcs2000_transformer(central_meridian=central_meridian)
    elif args.cgcs2000_6deg:
        # 6 度带：中央经线 = 带号 × 6 - 3
        central_meridian = args.cgcs2000_6deg * 6 - 3
        transform_func = create_cgcs2000_transformer(central_meridian=central_meridian)
    elif args.cgcs2000_geog:
        transform_func = create_cgcs2000_transformer(use_geog=True)
    elif args.utm_zone:
        transform_func = create_utm_transformer(args.utm_zone, not args.southern)
    else:
        transform_func = create_simple_transform(args.base_lat, args.base_lon)
        print(f"[OK] Using simple conversion (base: {args.base_lat}N, {args.base_lon}E)")
    
    if transform_func is None:
        print("Error: Failed to create coordinate transformer")
        sys.exit(1)
    
    # Execute conversion
    converter = DWG2KMLConverter(args.output)
    converter.create_kml_document(name=args.name)
    
    input_lower = args.input.lower()
    if input_lower.endswith('.dxf'):
        converter.convert_dxf_to_kml(args.input, transform_func)
    elif input_lower.endswith('.dwg'):
        print("\nWarning: DWG is a proprietary format and must be converted to DXF first")
        print("Options:")
        print("  1. Use AutoCAD DXFOUT command to export as DXF")
        print("  2. Use ODA File Converter: https://www.opendesign.com/guestfiles/oda_file_converter")
        print(f"\nThen run: python dwg2kml.py your_file.dxf -o {args.output}")
        sys.exit(1)
    else:
        print(f"\nError: Unsupported file format: {args.input}")
        print("Supported formats: .dxf")
        sys.exit(1)


if __name__ == '__main__':
    main()
