#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DWG/DXF to KML Converter - GUI 版本
提供图形界面，方便非技术用户使用

支持坐标系：
- CGCS2000（中国大地坐标系 2000）
- UTM（通用横轴墨卡托投影）
- 简单基准点转换
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading

# 导入转换核心
try:
    from dwg2kml import (
        DWG2KMLConverter, 
        create_utm_transformer, 
        create_cgcs2000_transformer,
        create_simple_transform
    )
    import math
except ImportError:
    print("错误：无法导入 dwg2kml 模块")
    print("请确保 dwg2kml.py 在同一目录下")
    sys.exit(1)


# ========== 语言包 ==========
LANGUAGES = {
    'zh_CN': {
        # 菜单
        'menu_file': '文件',
        'menu_lang': 'Language / 语言',
        'menu_help': '帮助',
        'menu_open': '打开 DXF...',
        'menu_exit': '退出',
        'menu_help_usage': '使用说明',
        'menu_help_coord': '坐标系参考',
        'menu_help_about': '关于',
        
        # 标题
        'title_main': 'DXF to KML 转换器 - 支持 CGCS2000',
        'title_label': 'DXF to KML 转换器',
        'title_data': '数据信息',
        'title_coord': '坐标系信息',
        'title_output': '输出设置',
        'title_log': '转换日志',
        
        # 数据信息
        'label_path': '数据路径:',
        'label_coord_source': '坐标系来源:',
        'radio_custom': '自定义配置',
        'button_browse': '选择',
        
        # 坐标系信息
        'label_proj_type': '投影类型:',
        'radio_gauss': '高斯克吕格 (Gauss-Kruger)',
        'radio_utm': 'UTM',
        'label_ellipsoid': '椭球参数:',
        'label_coord_system': '坐标系:',
        'label_central_meridian': '中央子午线:',
        'label_degree': '度°',
        'label_minute': '分′',
        'label_second': '秒″',
        'label_elevation': '投影面高程:',
        'label_false_easting': '假东:',
        'label_false_northing': '假北:',
        'label_meter': '米',
        'button_apply_meridian': '→',
        
        # 输出设置
        'label_output_file': '输出文件:',
        'label_kml_name': 'KML 名称:',
        'button_browse_output': '浏览...',
        
        # 按钮
        'button_start': '开始转换',
        
        # 消息
        'msg_no_file': '请选择要转换的 DXF 文件',
        'msg_converting': '正在转换...',
        'msg_complete': '转换成功完成！',
        'msg_error': '转换失败',
        'msg_confirm_exit': '确定要退出吗？',
        
        # 帮助窗口
        'help_title': '使用说明',
        'help_content': '''
╔══════════════════════════════════════════════════════════════════╗
║                    DXF to KML 转换器 - 使用说明                   ║
╚══════════════════════════════════════════════════════════════════╝

一、快速开始
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 选择 DXF 文件
   点击"选择"按钮，选择要转换的 DXF 文件

2. 配置坐标系
   - 投影类型：选择高斯克吕格（中国地区）或 UTM
   - 椭球参数：选择"国家 2000 (CGCS2000)"
   - 中央子午线：根据项目位置设置（见"坐标系参考"）

3. 设置输出
   - 输出文件：选择 KML 保存位置
   - KML 名称：填写项目名称（在 Google Earth 中显示）

4. 开始转换
   点击"开始转换"按钮，等待完成


二、中央子午线设置
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

方法 1：从坐标系下拉框选择
   选择预设的坐标系，自动填充中央子午线

方法 2：直接输入度分秒
   度°：输入整数部分（如 119）
   分′：输入 0-59（如 45）
   秒″：输入 0.00-59.99（如 0.00）
   
   点击"→"按钮可从中央子午线计算带号

方法 3：选择城市快速设置
   在坐标系下拉框中选择对应城市的预设


三、主要城市中央经线参考
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

城市           3 度带    6 度带    带号
─────────────────────────────────────────
北京           117°E    117°E    39/20
上海           123°E    123°E    41/21
广州           114°E    117°E    38/20
深圳           114°E    117°E    38/20
杭州           120°E    123°E    40/21
浙江金华       119°45′E 117°E    40/20


四、常见问题
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: DWG 文件可以直接转换吗？
A: 不能。需先在 AutoCAD 中导出为 DXF。

Q: 转换后位置偏移很大？
A: 检查中央子午线是否正确。

Q: 如何知道用什么坐标系？
A: 查看 CAD 图纸标题栏或咨询测量负责人。
''',
        'help_coord_ref': '坐标系参考表',
        'help_about': '关于',
        'button_close': '关闭',
    },
    'en_US': {
        # 菜单
        'menu_file': 'File',
        'menu_lang': 'Language / 语言',
        'menu_help': 'Help',
        'menu_open': 'Open DXF...',
        'menu_exit': 'Exit',
        'menu_help_usage': 'Usage Guide',
        'menu_help_coord': 'Coordinate Reference',
        'menu_help_about': 'About',
        
        # 标题
        'title_main': 'DXF to KML Converter - CGCS2000 Support',
        'title_label': 'DXF to KML Converter',
        'title_data': 'Data Information',
        'title_coord': 'Coordinate System',
        'title_output': 'Output Settings',
        'title_log': 'Conversion Log',
        
        # 数据信息
        'label_path': 'File Path:',
        'label_coord_source': 'Coordinate Source:',
        'radio_custom': 'Custom Configuration',
        'button_browse': 'Browse',
        
        # 坐标系信息
        'label_proj_type': 'Projection Type:',
        'radio_gauss': 'Gauss-Kruger',
        'radio_utm': 'UTM',
        'label_ellipsoid': 'Ellipsoid:',
        'label_coord_system': 'Coordinate System:',
        'label_central_meridian': 'Central Meridian:',
        'label_degree': '°',
        'label_minute': '\'',
        'label_second': '"',
        'label_elevation': 'Elevation:',
        'label_false_easting': 'False Easting:',
        'label_false_northing': 'False Northing:',
        'label_meter': 'm',
        'button_apply_meridian': '→',
        
        # 输出设置
        'label_output_file': 'Output File:',
        'label_kml_name': 'KML Name:',
        'button_browse_output': 'Browse...',
        
        # 按钮
        'button_start': 'Start Conversion',
        
        # 消息
        'msg_no_file': 'Please select a DXF file to convert',
        'msg_converting': 'Converting...',
        'msg_complete': 'Conversion completed successfully!',
        'msg_error': 'Conversion failed',
        'msg_confirm_exit': 'Are you sure you want to exit?',
        
        # 帮助窗口
        'help_title': 'Usage Guide',
        'help_content': '''
╔══════════════════════════════════════════════════════════════════╗
║              DXF to KML Converter - Usage Guide                  ║
╚══════════════════════════════════════════════════════════════════╝

I. Quick Start
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Select DXF File
   Click "Browse" button to select DXF file

2. Configure Coordinate System
   - Projection Type: Gauss-Kruger (for China) or UTM
   - Ellipsoid: Select "CGCS2000 (China 2000)"
   - Central Meridian: Set according to project location

3. Set Output
   - Output File: Select KML save location
   - KML Name: Enter project name (displayed in Google Earth)

4. Start Conversion
   Click "Start Conversion" button and wait


II. Central Meridian Setting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method 1: Select from Dropdown
   Choose preset coordinate system, auto-fill central meridian

Method 2: Input Degrees/Minutes/Seconds
   Degrees (°): Enter integer part (e.g., 119)
   Minutes ('): Enter 0-59 (e.g., 45)
   Seconds ("): Enter 0.00-59.99 (e.g., 0.00)
   
   Click "→" to calculate zone number from central meridian

Method 3: Quick City Selection
   Select corresponding city from dropdown


III. Major Cities Central Meridian Reference
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

City           3° Zone   6° Zone   Zone No
─────────────────────────────────────────────
Beijing        117°E     117°E     39/20
Shanghai       123°E     123°E     41/21
Guangzhou      114°E     117°E     38/20
Shenzhen       114°E     117°E     38/20
Hangzhou       120°E     123°E     40/21
Zhejiang Jinhua 119°45′E 117°E     40/20


IV. FAQ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: Can DWG files be converted directly?
A: No. Export to DXF in AutoCAD first.

Q: Large position offset after conversion?
A: Check if central meridian is correct.

Q: How to know which coordinate system to use?
A: Check CAD drawing title block or consult surveyor.
''',
        'help_coord_ref': 'Coordinate Reference Table',
        'help_about': 'About',
        'button_close': 'Close',
    }
}


# 椭球参数选项 - 中英文
ELLIPSOID_OPTIONS = {
    'zh_CN': [
        "国家 2000 (CGCS2000)",
        "WGS 84",
        "北京 54",
        "西安 80",
    ],
    'en_US': [
        "CGCS2000 (China 2000)",
        "WGS 84",
        "Beijing 54",
        "Xian 80",
    ]
}

# 坐标系预设（3 度带）- 中英文
COORD_SYSTEMS_3DEG = {
    'zh_CN': [
        "国家 2000 高斯三度分带 中央经线 75°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 78°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 81°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 84°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 87°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 90°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 93°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 96°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 99°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 102°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 105°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 108°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 111°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 114°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 117°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 120°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 123°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 126°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 129°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 132°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 135°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 138°E (坐标不含分带)",
        "国家 2000 高斯三度分带 中央经线 141°E (坐标不含分带)",
    ],
    'en_US': [
        "CGCS2000 Gauss 3° Zone Central Meridian 75°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 78°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 81°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 84°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 87°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 90°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 93°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 96°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 99°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 102°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 105°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 108°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 111°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 114°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 117°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 120°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 123°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 126°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 129°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 132°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 135°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 138°E (coords without zone)",
        "CGCS2000 Gauss 3° Zone Central Meridian 141°E (coords without zone)",
    ]
}

# 坐标系预设（6 度带）- 中英文
COORD_SYSTEMS_6DEG = {
    'zh_CN': [
        "国家 2000 高斯六度分带 中央经线 69°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 75°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 81°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 87°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 93°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 99°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 105°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 111°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 117°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 123°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 129°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 135°E (坐标不含分带)",
        "国家 2000 高斯六度分带 中央经线 141°E (坐标不含分带)",
    ],
    'en_US': [
        "CGCS2000 Gauss 6° Zone Central Meridian 69°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 75°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 81°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 87°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 93°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 99°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 105°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 111°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 117°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 123°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 129°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 135°E (coords without zone)",
        "CGCS2000 Gauss 6° Zone Central Meridian 141°E (coords without zone)",
    ]
}


def meridian_to_zone_3deg(meridian):
    """3 度带：中央子午线转带号"""
    return round(meridian / 3)


def meridian_to_zone_6deg(meridian):
    """6 度带：中央子午线转带号"""
    return int((meridian + 3) / 6)


def parse_dms(degrees, minutes, seconds):
    """解析度分秒为十进制度"""
    try:
        d = float(degrees) if degrees else 0
        m = float(minutes) if minutes else 0
        s = float(seconds) if seconds else 0
        return d + m / 60 + s / 3600
    except ValueError:
        return None


def dms_from_meridian(meridian):
    """从中央子午线获取度分秒"""
    d = int(meridian)
    m = int((meridian - d) * 60)
    s = ((meridian - d) * 60 - m) * 60
    return d, m, s


class DWG2KMLGUI:
    """DWG2KML 转换器图形界面"""
    
    def __init__(self, root):
        # 语言设置（必须在最前面，因为其他地方要用）
        self.current_lang = 'zh_CN'
        self.lang = LANGUAGES[self.current_lang]
        
        self.root = root
        self.root.title(self.lang['title_main'])
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # 设置菜单
        self.setup_menu()
        
        # 文件变量
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar(value="output.kml")
        self.kml_name = tk.StringVar(value="CAD Drawing")
        
        # 坐标系配置变量
        self.coord_source = tk.StringVar(value="custom")  # custom 或 auto
        self.proj_type = tk.StringVar(value="gauss_kruger")  # gauss_kruger 或 utm
        self.ellipsoid = tk.StringVar(value="国家 2000 (CGCS2000)")
        self.coord_system = tk.StringVar()
        
        # 中央子午线（度分秒）
        self.meridian_deg = tk.StringVar(value="117")
        self.meridian_min = tk.StringVar(value="0")
        self.meridian_sec = tk.StringVar(value="0.00")
        
        # 投影参数
        self.proj_height = tk.StringVar(value="0.00")
        self.false_easting = tk.StringVar(value="500000.00")
        self.false_northing = tk.StringVar(value="0.00")
        
        # 简单转换参数
        self.base_lat = tk.StringVar(value="39.9042")
        self.base_lon = tk.StringVar(value="116.4074")
        self.utm_zone = tk.StringVar(value="50")
        self.is_northern = tk.BooleanVar(value=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # 标题
        title_label = ttk.Label(self.main_frame, text=self.lang['title_label'], 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=row, column=0, columnspan=3, pady=5)
        row += 1
        
        # ===== 数据信息区域 =====
        data_frame = ttk.LabelFrame(self.main_frame, text=f"  {self.lang['title_data']}  ", padding="10")
        data_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        data_frame.columnconfigure(1, weight=1)
        
        # 数据路径
        ttk.Label(data_frame, text=self.lang['label_path']).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        path_frame = ttk.Frame(data_frame)
        path_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        path_frame.columnconfigure(0, weight=1)
        
        self.input_entry = ttk.Entry(path_frame, textvariable=self.input_file)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.browse_button = ttk.Button(path_frame, text=self.lang['button_browse'], command=self.browse_input)
        self.browse_button.grid(row=0, column=1)
        
        row += 1
        
        # ===== 坐标系信息区域 =====
        coord_frame = ttk.LabelFrame(self.main_frame, text=f"  {self.lang['title_coord']}  ", padding="10")
        coord_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        coord_frame.columnconfigure(1, weight=1)
        
        # 投影类型
        ttk.Label(coord_frame, text=self.lang['label_proj_type']).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        proj_frame = ttk.Frame(coord_frame)
        proj_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        self.gauss_radio = ttk.Radiobutton(
            proj_frame, text=self.lang['radio_gauss'], 
            variable=self.proj_type, value="gauss_kruger",
            command=self.on_proj_type_changed
        )
        self.gauss_radio.pack(side=tk.LEFT, padx=5)
        
        self.utm_radio = ttk.Radiobutton(
            proj_frame, text=self.lang['radio_utm'], 
            variable=self.proj_type, value="utm",
            command=self.on_proj_type_changed
        )
        self.utm_radio.pack(side=tk.LEFT, padx=20)
        
        # 右侧工具按钮（预留）
        tool_frame = ttk.Frame(coord_frame)
        tool_frame.grid(row=0, column=2, sticky=tk.E, pady=5)
        
        # 椭球参数
        ttk.Label(coord_frame, text=self.lang['label_ellipsoid']).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.ellipsoid_combo = ttk.Combobox(
            coord_frame, 
            textvariable=self.ellipsoid,
            values=ELLIPSOID_OPTIONS[self.current_lang],
            width=40,
            state="readonly"
        )
        self.ellipsoid_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 坐标系
        ttk.Label(coord_frame, text=self.lang['label_coord_system']).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.coord_combo = ttk.Combobox(
            coord_frame,
            textvariable=self.coord_system,
            values=COORD_SYSTEMS_3DEG[self.current_lang],
            width=60,
            state="readonly"
        )
        self.coord_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self.coord_combo.bind('<<ComboboxSelected>>', self.on_coord_system_selected)
        
        # 中央子午线
        ttk.Label(coord_frame, text=self.lang['label_central_meridian']).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        dms_frame = ttk.Frame(coord_frame)
        dms_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        self.meridian_deg_entry = ttk.Entry(dms_frame, textvariable=self.meridian_deg, width=8)
        self.meridian_deg_entry.pack(side=tk.LEFT)
        ttk.Label(dms_frame, text=self.lang['label_degree']).pack(side=tk.LEFT, padx=2)
        
        self.meridian_min_entry = ttk.Entry(dms_frame, textvariable=self.meridian_min, width=6)
        self.meridian_min_entry.pack(side=tk.LEFT, padx=(10, 0))
        ttk.Label(dms_frame, text=self.lang['label_minute']).pack(side=tk.LEFT, padx=2)
        
        self.meridian_sec_entry = ttk.Entry(dms_frame, textvariable=self.meridian_sec, width=8)
        self.meridian_sec_entry.pack(side=tk.LEFT, padx=(10, 0))
        ttk.Label(dms_frame, text=self.lang['label_second']).pack(side=tk.LEFT, padx=2)
        
        # 转换按钮
        ttk.Button(dms_frame, text=self.lang['button_apply_meridian'], width=2, 
                  command=self.calculate_from_meridian).pack(side=tk.LEFT, padx=10)
        
        # 投影参数
        param_frame = ttk.Frame(coord_frame)
        param_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(param_frame, text=self.lang['label_elevation']).pack(side=tk.LEFT)
        self.proj_height_entry = ttk.Entry(param_frame, textvariable=self.proj_height, width=10)
        self.proj_height_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(param_frame, text=self.lang['label_meter']).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(param_frame, text=self.lang['label_false_easting']).pack(side=tk.LEFT, padx=(10, 0))
        self.false_easting_entry = ttk.Entry(param_frame, textvariable=self.false_easting, width=12)
        self.false_easting_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(param_frame, text=self.lang['label_meter']).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(param_frame, text=self.lang['label_false_northing']).pack(side=tk.LEFT, padx=(10, 0))
        self.false_northing_entry = ttk.Entry(param_frame, textvariable=self.false_northing, width=10)
        self.false_northing_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(param_frame, text=self.lang['label_meter']).pack(side=tk.LEFT)
        
        row += 1
        
        # ===== 输出设置区域 =====
        output_frame = ttk.LabelFrame(self.main_frame, text=f"  {self.lang['title_output']}  ", padding="10")
        output_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text=self.lang['label_output_file']+":").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        out_path_frame = ttk.Frame(output_frame)
        out_path_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        out_path_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(out_path_frame, textvariable=self.output_file)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(out_path_frame, text=self.lang['button_browse_output'], command=self.browse_output).grid(row=0, column=1)
        
        ttk.Label(output_frame, text=self.lang['label_kml_name']+":").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.kml_name, width=50).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        row += 1
        
        # ===== 转换按钮 =====
        self.convert_btn = ttk.Button(self.main_frame, text=self.lang['button_start'], command=self.start_conversion)
        self.convert_btn.grid(row=row, column=0, columnspan=3, pady=10)
        row += 1
        
        # 进度条
        self.progress = ttk.Progressbar(self.main_frame, mode='indeterminate')
        self.progress.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # ===== 日志区域 =====
        ttk.Label(self.main_frame, text=self.lang['title_log']+":", font=('Arial', 10, 'bold')).grid(row=row, column=0, 
                                                                                 sticky=tk.W)
        row += 1
        
        self.log_text = scrolledtext.ScrolledText(self.main_frame, height=12, width=80)
        self.log_text.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.main_frame.rowconfigure(row, weight=1)
        
        # 绑定日志输出
        self.setup_logging()
        
        # 初始化 UI 状态
        self.on_proj_type_changed()
        
    def setup_menu(self):
        """设置菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang['menu_file'], menu=file_menu)
        file_menu.add_command(label=self.lang['menu_open'], command=self.browse_input, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label=self.lang['menu_exit'], command=self.root.quit, accelerator="Alt+F4")
        
        # 语言菜单
        lang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang['menu_lang'], menu=lang_menu)
        if not hasattr(self, 'lang_var'):
            self.lang_var = tk.StringVar(value='zh_CN')
        lang_menu.add_radiobutton(
            label='🇨🇳 简体中文', 
            value='zh_CN', 
            variable=self.lang_var,
            command=self.switch_language
        )
        lang_menu.add_radiobutton(
            label='🇺🇸 English', 
            value='en_US', 
            variable=self.lang_var,
            command=self.switch_language
        )
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang['menu_help'], menu=help_menu)
        help_menu.add_command(label=self.lang['menu_help_usage'], command=self.show_help, accelerator="F1")
        help_menu.add_command(label=self.lang['menu_help_coord'], command=self.show_coord_reference)
        help_menu.add_separator()
        help_menu.add_command(label=self.lang['menu_help_about'], command=self.show_about)
        
        # 绑定快捷键
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<Control-o>', lambda e: self.browse_input())
    
    def switch_language(self):
        """切换语言"""
        new_lang = self.lang_var.get()
        if new_lang != self.current_lang:
            self.current_lang = new_lang
            self.lang = LANGUAGES[self.current_lang]
            
            # 更新下拉框选项
            self.ellipsoid_combo['values'] = ELLIPSOID_OPTIONS[self.current_lang]
            if self.proj_type.get() == 'gauss_kruger':
                self.coord_combo['values'] = COORD_SYSTEMS_3DEG[self.current_lang]
            else:
                self.coord_combo['values'] = COORD_SYSTEMS_6DEG[self.current_lang]
            
            # 重建 UI
            self.update_ui_language()
    
    def update_ui_language(self):
        """更新界面语言 - 通过重建 UI"""
        # 更新窗口标题
        self.root.title(self.lang['title_main'])
        
        # 更新菜单文本
        self.setup_menu()
        
        # 清除当前 UI
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # 重新创建 UI
        self.setup_ui()
    
    def show_help(self):
        """显示帮助对话框"""
        help_window = tk.Toplevel(self.root)
        help_window.title(self.lang['help_title'])
        help_window.geometry("700x600")
        help_window.transient(self.root)
        help_window.grab_set()
        
        # 创建文本框
        text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=('Microsoft YaHei', 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 根据当前语言显示帮助内容
        help_content = self.lang['help_content']
        text.insert('1.0', help_content)
        text.config(state='disabled')
        
        # 关闭按钮
        btn_frame = ttk.Frame(help_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text=self.lang['button_close'], command=help_window.destroy).pack(side=tk.RIGHT)
    
    def show_coord_reference(self):
        """显示坐标系参考表"""
        ref_window = tk.Toplevel(self.root)
        ref_window.title("坐标系参考表")
        ref_window.geometry("600x450")
        ref_window.transient(self.root)
        ref_window.grab_set()
        
        # 创建表格
        columns = ('city', 'zone3', 'zone6', 'meridian3', 'meridian6')
        tree = ttk.Treeview(ref_window, columns=columns, show='headings', height=20)
        
        # 设置列标题
        tree.heading('city', text='城市')
        tree.heading('zone3', text='3 度带带号')
        tree.heading('zone6', text='6 度带带号')
        tree.heading('meridian3', text='3 度带中央经线')
        tree.heading('meridian6', text='6 度带中央经线')
        
        # 设置列宽
        tree.column('city', width=100, anchor='center')
        tree.column('zone3', width=80, anchor='center')
        tree.column('zone6', width=80, anchor='center')
        tree.column('meridian3', width=100, anchor='center')
        tree.column('meridian6', width=100, anchor='center')
        
        # 添加数据
        cities = [
            ("北京", "39", "20", "117°E", "117°E"),
            ("天津", "39", "20", "117°E", "117°E"),
            ("上海", "41", "21", "123°E", "123°E"),
            ("广州", "38", "20", "114°E", "117°E"),
            ("深圳", "38", "20", "114°E", "117°E"),
            ("杭州", "40", "21", "120°E", "123°E"),
            ("南京", "40", "20", "120°E", "117°E"),
            ("武汉", "38", "20", "114°E", "117°E"),
            ("成都", "35", "18", "105°E", "105°E"),
            ("重庆", "36", "18", "108°E", "105°E"),
            ("西安", "36", "19", "108°E", "111°E"),
            ("沈阳", "41", "21", "123°E", "123°E"),
            ("哈尔滨", "42", "22", "126°E", "129°E"),
            ("昆明", "34", "17", "102°E", "99°E"),
            ("拉萨", "30", "16", "90°E", "93°E"),
            ("乌鲁木齐", "29", "15", "87°E", "87°E"),
        ]
        
        for city in cities:
            tree.insert('', tk.END, values=city)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(ref_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 关闭按钮
        btn_frame = ttk.Frame(ref_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="关闭", command=ref_window.destroy).pack(side=tk.RIGHT)
    
    def show_about(self):
        """显示关于对话框"""
        about_window = tk.Toplevel(self.root)
        about_window.title("关于")
        about_window.geometry("400x300")
        about_window.transient(self.root)
        about_window.grab_set()
        about_window.resizable(False, False)
        
        # 居中显示
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() - 400) // 2
        y = (about_window.winfo_screenheight() - 300) // 2
        about_window.geometry(f"400x300+{x}+{y}")
        
        # 内容框架
        content_frame = ttk.Frame(about_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            content_frame,
            text="DXF to KML 转换器",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=10)
        
        # 版本
        version_label = ttk.Label(
            content_frame,
            text="版本 1.0",
            font=('Arial', 10)
        )
        version_label.pack(pady=5)
        
        # 描述
        desc_label = ttk.Label(
            content_frame,
            text="支持 CGCS2000 / UTM 坐标系转换",
            font=('Arial', 9),
            foreground='gray'
        )
        desc_label.pack(pady=5)
        
        # 分隔线
        ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # 开发者信息
        dev_label = ttk.Label(
            content_frame,
            text="开发者：Wang Ningping",
            font=('Arial', 9)
        )
        dev_label.pack(pady=5)
        
        email_label = ttk.Label(
            content_frame,
            text="📧 174367449@qq.com",
            font=('Arial', 9),
            foreground='blue',
            cursor="hand2"
        )
        email_label.pack(pady=2)
        
        # 分隔线
        ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # 版权信息
        copyright_label = ttk.Label(
            content_frame,
            text="© 2026 Wang Ningping. All rights reserved.",
            font=('Arial', 8),
            foreground='gray'
        )
        copyright_label.pack(pady=5)
        
        # 关闭按钮
        ttk.Button(content_frame, text="关闭", command=about_window.destroy).pack(pady=10)
        
    def setup_logging(self):
        """设置日志输出到文本框"""
        class TextHandler:
            def __init__(self, text_widget):
                self.text_widget = text_widget
                
            def write(self, text):
                self.text_widget.insert(tk.END, text)
                self.text_widget.see(tk.END)
                self.text_widget.update()
                
            def flush(self):
                pass
        
        # 添加 log 方法到类实例
        def log(text):
            self.log_text.insert(tk.END, text)
            self.log_text.see(tk.END)
            self.log_text.update()
        
        self.log = log
        sys.stdout = TextHandler(self.log_text)
        sys.stderr = TextHandler(self.log_text)
        
    def on_proj_type_changed(self):
        """投影类型改变时的处理"""
        if self.proj_type.get() == "gauss_kruger":
            self.coord_combo['values'] = COORD_SYSTEMS_3DEG[self.current_lang]
            values = COORD_SYSTEMS_3DEG[self.current_lang]
            if values and len(values) > 14:
                self.coord_combo.set(values[14])  # 默认 117°E
        else:  # UTM
            self.coord_combo['values'] = COORD_SYSTEMS_6DEG[self.current_lang]
            values = COORD_SYSTEMS_6DEG[self.current_lang]
            if values and len(values) > 8:
                self.coord_combo.set(values[8])  # 默认 117°E
        
    def on_coord_system_selected(self, event):
        """坐标系选择改变时的处理"""
        coord_str = self.coord_system.get()
        # 从字符串中提取中央经线度数
        try:
            # 格式："国家 2000 高斯三度分带 中央经线 117°E (坐标不含分带)"
            if "中央经线" in coord_str and "°E" in coord_str:
                parts = coord_str.split("中央经线")
                if len(parts) > 1:
                    meridian_part = parts[1].split("°E")[0]
                    meridian = float(meridian_part)
                    d, m, s = dms_from_meridian(meridian)
                    self.meridian_deg.set(str(d))
                    self.meridian_min.set(str(m))
                    self.meridian_sec.set(f"{s:.2f}")
        except Exception as e:
            pass
        
    def calculate_from_meridian(self):
        """从中央子午线计算带号并更新坐标系"""
        try:
            deg = float(self.meridian_deg.get())
            if self.proj_type.get() == "gauss_kruger":
                zone = meridian_to_zone_3deg(deg)
                # 根据语言输出日志
                if self.current_lang == 'zh_CN':
                    self.log(f"3 度带：中央经线{deg}°E → 带号{zone}\n")
                else:
                    self.log(f"3° Zone: Central Meridian {deg}°E → Zone {zone}\n")
                # 更新坐标系选择
                target_str = f"国家 2000 高斯三度分带 中央经线{int(deg)}°E (坐标不含分带)"
                if target_str in COORD_SYSTEMS_3DEG['zh_CN']:
                    self.coord_combo.set(target_str)
            else:
                zone = meridian_to_zone_6deg(deg)
                if self.current_lang == 'zh_CN':
                    self.log(f"6 度带：中央经线{deg}°E → 带号{zone}\n")
                else:
                    self.log(f"6° Zone: Central Meridian {deg}°E → Zone {zone}\n")
        except ValueError:
            messagebox.showerror("错误" if self.current_lang == 'zh_CN' else "Error", 
                                "请输入有效的度数值" if self.current_lang == 'zh_CN' else "Please enter a valid degree value")
    
    def update_labels(self):
        """更新所有标签文本"""
        # 数据信息区域
        if hasattr(self, 'path_label'):
            self.path_label.config(text=self.lang['label_path'])
        
        # 坐标系信息区域
        for widget in self.coord_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                text = widget.cget('text')
                if '投影类型' in text:
                    widget.config(text=self.lang['label_proj_type'])
                elif '椭球参数' in text:
                    widget.config(text=self.lang['label_ellipsoid'])
                elif '坐标系' in text and '中央' not in text:
                    widget.config(text=self.lang['label_coord_system'])
                elif '中央子午线' in text:
                    widget.config(text=self.lang['label_central_meridian'])
                elif '投影面高程' in text:
                    widget.config(text=self.lang['label_elevation'])
                elif '假东' in text:
                    widget.config(text=self.lang['label_false_easting'])
                elif '假北' in text:
                    widget.config(text=self.lang['label_false_northing'])
    
    def update_buttons(self):
        """更新所有按钮文本"""
        if hasattr(self, 'browse_button'):
            self.browse_button.config(text=self.lang['button_browse'])
        
        # 更新开始转换按钮
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                if '转换' in widget.cget('text') or 'Conversion' in widget.cget('text'):
                    widget.config(text=self.lang['button_start'])
        
    def browse_input(self):
        """浏览输入文件"""
        filename = filedialog.askopenfilename(
            title="选择 DXF 文件",
            filetypes=[("DXF 文件", "*.dxf *.DXF"), ("所有文件", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # 自动设置输出文件名
            if not self.output_file.get() or self.output_file.get() == "output.kml":
                base = Path(filename).stem
                self.output_file.set(f"{base}.kml")
                
    def browse_output(self):
        """浏览输出文件"""
        filename = filedialog.asksaveasfilename(
            title="保存 KML 文件",
            defaultextension=".kml",
            filetypes=[("KML 文件", "*.kml"), ("所有文件", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
            
    def start_conversion(self):
        """开始转换（在新线程中）"""
        input_file = self.input_file.get()
        output_file = self.output_file.get()
        
        if not input_file:
            if self.current_lang == 'zh_CN':
                messagebox.showerror("错误", "请选择输入文件！")
            else:
                messagebox.showerror("Error", "Please select an input file!")
            return
            
        if not os.path.exists(input_file):
            if self.current_lang == 'zh_CN':
                messagebox.showerror("错误", f"文件不存在：{input_file}")
            else:
                messagebox.showerror("Error", f"File does not exist: {input_file}")
            return
            
        # 禁用按钮
        self.convert_btn.state(['disabled'])
        self.progress.start()
        
        # 在新线程中执行转换
        thread = threading.Thread(target=self.do_conversion, 
                                 args=(input_file, output_file))
        thread.daemon = True
        thread.start()
        
    def do_conversion(self, input_file, output_file):
        """执行转换"""
        try:
            self.log(f"\n{'='*60}\n")
            # 根据语言输出日志
            if self.current_lang == 'zh_CN':
                self.log(f"开始转换：{input_file}\n")
                self.log(f"{'='*60}\n")
                
                # 检查文件类型
                if input_file.lower().endswith('.dwg'):
                    self.log("⚠ 警告：DWG 是专有格式，需要先转换为 DXF\n")
                    self.log("建议:\n")
                    self.log("  1. 在 AutoCAD 中使用 DXFOUT 命令导出为 DXF\n")
                    self.log("  2. 或使用 ODA File Converter\n")
                    self.on_conversion_complete(False, "DWG 格式需要先转换为 DXF")
                    return
                    
                if not input_file.lower().endswith('.dxf'):
                    self.log(f"⚠ 错误：不支持的文件格式：{input_file}\n")
                    self.on_conversion_complete(False, "不支持的文件格式")
                    return
                
                # 解析中央子午线
                meridian = parse_dms(
                    self.meridian_deg.get(),
                    self.meridian_min.get(),
                    self.meridian_sec.get()
                )
                
                if meridian is None:
                    self.log("⚠ 错误：中央子午线格式无效\n")
                    self.on_conversion_complete(False, "中央子午线格式无效")
                    return
                
                self.log(f"坐标系配置:\n")
                self.log(f"  椭球参数：{self.ellipsoid.get()}\n")
                self.log(f"  投影类型：{'高斯克吕格' if self.proj_type.get() == 'gauss_kruger' else 'UTM'}\n")
                self.log(f"  中央子午线：{meridian:.4f}°E\n")
                self.log(f"  投影面高程：{self.proj_height.get()} 米\n")
                self.log(f"  假东：{self.false_easting.get()} 米\n")
                self.log(f"  假北：{self.false_northing.get()} 米\n\n")
            else:
                self.log(f"Starting Conversion: {input_file}\n")
                self.log(f"{'='*60}\n")
                
                if input_file.lower().endswith('.dwg'):
                    self.log("⚠ Warning: DWG is proprietary format, convert to DXF first\n")
                    self.log("Suggestions:\n")
                    self.log("  1. Use DXFOUT command in AutoCAD\n")
                    self.log("  2. Or use ODA File Converter\n")
                    self.on_conversion_complete(False, "DWG format needs conversion to DXF")
                    return
                    
                if not input_file.lower().endswith('.dxf'):
                    self.log(f"⚠ Error: Unsupported file format: {input_file}\n")
                    self.on_conversion_complete(False, "Unsupported format")
                    return
                
                meridian = parse_dms(
                    self.meridian_deg.get(),
                    self.meridian_min.get(),
                    self.meridian_sec.get()
                )
                
                if meridian is None:
                    self.log("⚠ Error: Invalid central meridian format\n")
                    self.on_conversion_complete(False, "Invalid meridian format")
                    return
                
                self.log(f"Coordinate System Configuration:\n")
                self.log(f"  Ellipsoid: {self.ellipsoid.get()}\n")
                self.log(f"  Projection: {'Gauss-Kruger' if self.proj_type.get() == 'gauss_kruger' else 'UTM'}\n")
                self.log(f"  Central Meridian: {meridian:.4f}°E\n")
                self.log(f"  Elevation: {self.proj_height.get()} m\n")
                self.log(f"  False Easting: {self.false_easting.get()} m\n")
                self.log(f"  False Northing: {self.false_northing.get()} m\n\n")
            
            # 创建转换器
            converter = DWG2KMLConverter(output_file)
            converter.create_kml_document(name=self.kml_name.get())
            
            # 确定坐标转换函数
            transform_func = None
            
            if self.proj_type.get() == "gauss_kruger":
                # 高斯克吕格投影（CGCS2000）- 直接使用中央经线
                if self.current_lang == 'zh_CN':
                    self.log(f"✓ 使用 CGCS2000 高斯克吕格 (中央经线：{meridian:.4f}°E)\n")
                else:
                    self.log(f"✓ Using CGCS2000 Gauss-Kruger (Central Meridian: {meridian:.4f}°E)\n")
                transform_func = create_cgcs2000_transformer(central_meridian=meridian)
            else:
                # UTM 投影
                zone = meridian_to_zone_6deg(meridian)
                if self.current_lang == 'zh_CN':
                    self.log(f"✓ 使用 UTM {zone}带 (中央经线：{meridian:.2f}°E)\n")
                else:
                    self.log(f"✓ Using UTM Zone {zone} (Central Meridian: {meridian:.2f}°E)\n")
                transform_func = create_utm_transformer(zone, True)
            
            if transform_func is None:
                if self.current_lang == 'zh_CN':
                    self.log("⚠ 错误：无法创建坐标转换器，请检查 pyproj 是否安装\n")
                    self.on_conversion_complete(False, "pyproj 未安装")
                else:
                    self.log("⚠ Error: Cannot create coordinate transformer, check pyproj installation\n")
                    self.on_conversion_complete(False, "pyproj not installed")
                return
            
            # 执行转换
            converter.convert_dxf_to_kml(input_file, transform_func)
            
            self.log(f"\n{'='*60}\n")
            if self.current_lang == 'zh_CN':
                self.log("✓ 转换成功完成！\n")
                self.log(f"输出文件：{output_file}\n")
                self.log(f"{'='*60}\n")
            else:
                self.log("✓ Conversion completed successfully!\n")
                self.log(f"Output file: {output_file}\n")
                self.log(f"{'='*60}\n")
            
            self.on_conversion_complete(True, output_file)
            
        except Exception as e:
            if self.current_lang == 'zh_CN':
                self.log(f"\n❌ 转换失败：{str(e)}\n")
            else:
                self.log(f"\n❌ Conversion failed: {str(e)}\n")
            import traceback
            self.log(traceback.format_exc())
            self.on_conversion_complete(False, str(e))
        
    def on_conversion_complete(self, success, result):
        """转换完成回调"""
        self.progress.stop()
        self.convert_btn.state(['!disabled'])
        
        if success:
            if self.current_lang == 'zh_CN':
                self.root.after(100, lambda: messagebox.showinfo(
                    "成功", 
                    f"转换完成！\n\n输出文件：{result}\n\n可以用 Google Earth 打开查看"
                ))
            else:
                self.root.after(100, lambda: messagebox.showinfo(
                    "Success", 
                    f"Conversion completed!\n\nOutput file: {result}\n\nCan be opened in Google Earth"
                ))
        else:
            if self.current_lang == 'zh_CN':
                self.root.after(100, lambda: messagebox.showerror("失败", f"转换失败：{result}"))
            else:
                self.root.after(100, lambda: messagebox.showerror("Error", f"Conversion failed: {result}"))


def main():
    """主函数"""
    root = tk.Tk()
    app = DWG2KMLGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
