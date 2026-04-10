# 示例文件说明

本文件夹用于存放示例 DXF 文件和转换后的 KML 文件，帮助用户快速测试和理解软件功能。

## 建议的示例文件

### 1. basic_example.dxf
**说明**: 基础示例 - 包含基本 CAD 实体
**内容**:
- LINE（直线）
- POLYLINE（多段线）
- CIRCLE（圆）
- TEXT（文字）

**用途**: 测试基本转换功能

### 2. cgcs2000_beijing.dxf
**说明**: CGCS2000 北京地区示例
**坐标系**: CGCS2000 3 度带 39 带（中央经线 117°E）
**内容**: 北京天安门附近建筑轮廓

**用途**: 测试 CGCS2000 坐标转换
**转换命令**:
```bash
python dwg2kml.py cgcs2000_beijing.dxf -o cgcs2000_beijing.kml --cgcs2000-3deg 39
```

### 3. cgcs2000_zhejiang.dxf
**说明**: CGCS2000 浙江金华地区示例
**坐标系**: CGCS2000 3 度带 40 带（中央经线 119°45'E）
**内容**: 金华某工程项目平面图

**用途**: 测试不同中央经线的转换
**转换命令**:
```bash
python dwg2kml.py cgcs2000_zhejiang.dxf -o cgcs2000_zhejiang.kml --cgcs2000-3deg 40
```

### 4. utm_example.dxf
**说明**: UTM 投影示例
**坐标系**: UTM Zone 50N
**内容**: 某地区道路网络

**用途**: 测试 UTM 坐标转换
**转换命令**:
```bash
python dwg2kml.py utm_example.dxf -o utm_example.kml --utm-zone 50
```

### 5. complex_drawing.dxf
**说明**: 复杂图纸示例
**坐标系**: CGCS2000 3 度带 39 带
**内容**: 包含所有支持的实体类型
- LINE, POLYLINE, LWPOLYLINE
- CIRCLE, ARC
- POINT
- TEXT, MTEXT
- INSERT（块引用）

**用途**: 全面测试所有实体类型的转换
**转换命令**:
```bash
python dwg2kml.py complex_drawing.dxf -o complex_drawing.kml --cgcs2000-3deg 39
```

## 示例文件创建指南

### 使用 AutoCAD 创建
1. 新建 DWG 文件
2. 绘制示例图形
3. 设置正确的坐标系
4. 使用 `DXFOUT` 命令导出为 DXF（建议 DXF 2010 格式）

### 使用 Python 创建
```python
import ezdxf

# 创建新文档
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# 添加实体
msp.add_line((0, 0), (100, 100))
msp.add_circle((50, 50), 25)
msp.add_text("Hello World", dxfattribs={'height': 5}).set_pos((50, 50), align='CENTER')

# 保存
doc.saveas("example.dxf")
```

## 注意事项

1. **文件大小**: 示例文件应尽量小（< 1MB），便于下载和测试
2. **坐标范围**: 使用合理的坐标值，避免过大或过小
3. **坐标系信息**: 在文件名或说明中标注坐标系
4. **版权**: 确保示例文件没有版权问题，或使用自己创建的文件

## 目录结构建议

```
examples/
├── README.md                    # 本文件
├── basic_example.dxf
├── basic_example.kml
├── cgcs2000_beijing.dxf
├── cgcs2000_beijing.kml
├── cgcs2000_zhejiang.dxf
├── cgcs2000_zhejiang.kml
├── utm_example.dxf
├── utm_example.kml
├── complex_drawing.dxf
└── complex_drawing.kml
```

---

**更新日期**: 2026-04-10
