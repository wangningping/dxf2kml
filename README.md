# DXF to KML Converter

<div align="center">

[![CI/CD](https://github.com/wangningping/dxf2kml/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/wangningping/dxf2kml/actions/workflows/ci-cd.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub release](https://img.shields.io/github/v/release/wangningping/dxf2kml)](https://github.com/wangningping/dxf2kml/releases)

**将 DXF 文件转换为 Google Earth KML 格式的专业工具**

[English](README_EN.md) | 简体中文

</div>

---

## 📋 功能特性

- ✅ **DXF 文件直接转换** - 支持 AutoCAD DXF 格式
- ✅ **多种 CAD 实体** - LINE, POLYLINE, CIRCLE, ARC, POINT, TEXT, INSERT
- ✅ **CGCS2000 坐标系支持** - 中国大地坐标系 2000 完美支持
- ✅ **UTM 坐标转换** - 全球通用 UTM 投影
- ✅ **批量转换** - 一次处理多个文件
- ✅ **双语界面** - 中英文一键切换
- ✅ **GUI + CLI** - 图形界面和命令行双模式
- ✅ **专业参数配置** - 中央子午线、假东、假北、投影面高程

---

## 🚀 快速开始

### 方法 1: 一键启动（Windows）

```bash
# 下载项目后
onekeystart.bat
```

### 方法 2: 使用 pip 安装

```bash
# 安装
pip install dxf2kml

# 使用命令行工具
dxf2kml input.dxf -o output.kml
```

### 方法 3: 从源码运行

```bash
# 克隆仓库
git clone https://github.com/wangningping/dxf2kml.git
cd dxf2kml

# 安装依赖
pip install -r requirements.txt

# 启动 GUI
python dwg2kml_gui.py
```

---

## 💻 使用方式

### 图形界面（GUI）

```bash
python dwg2kml_gui.py
```

**功能特点：**
- 📁 文件选择器
- 🌐 坐标系配置（CGCS2000/UTM）
- 📍 中央子午线设置（度分秒格式）
- 📊 实时转换日志
- 🌍 中英文切换

![GUI Screenshot](docs/screenshots/gui_main.png)

### 命令行（CLI）

```bash
# 单个文件转换
python dwg2kml.py input.dxf -o output.kml

# 批量转换
python dwg2kml.py --batch ./dxf_folder -o ./kml_output

# 使用 CGCS2000 坐标系（北京地区）
python dwg2kml.py input.dxf -o output.kml --cgcs2000-3deg 39

# 使用 UTM 坐标系
python dwg2kml.py input.dxf -o output.kml --utm --zone 50

# 查看帮助
python dwg2kml.py --help
```

---

## 🌍 坐标系支持

### CGCS2000（中国地区推荐）

| 城市 | 3 度带 | 6 度带 | 中央经线 |
|------|--------|--------|----------|
| 北京 | 39 带 | 20 带 | 117°E |
| 上海 | 41 带 | 21 带 | 123°E |
| 广州 | 38 带 | 20 带 | 114°E |
| 深圳 | 38 带 | 20 带 | 114°E |
| 杭州 | 40 带 | 21 带 | 120°E |
| 浙江金华 | 40 带 | 20 带 | 119°45′E |

**计算公式：**
- 3 度带：中央经线 = 带号 × 3
- 6 度带：中央经线 = 带号 × 6 - 3

### UTM（全球通用）

支持北半球和南半球，带号 1-60。

---

## 📁 项目结构

```
dxf2kml/
├── dwg2kml.py              # 命令行工具
├── dwg2kml_gui.py          # 图形界面
├── requirements.txt        # Python 依赖
├── pyproject.toml         # 项目配置
├── LICENSE                # MIT 许可证
├── README.md              # 中文说明
├── README_EN.md           # English README
├── onekeystart.bat        # Windows 一键启动
├── install.bat            # Windows 安装脚本
├── docs/
│   ├── guides/            # 使用指南
│   │   ├── CGCS2000 指南.md
│   │   ├── 快速使用指南.md
│   │   └── 功能说明.md
│   └── screenshots/       # 界面截图
├── examples/              # 示例文件
└── .github/
    └── workflows/         # GitHub Actions
        └── ci-cd.yml      # CI/CD 配置
```

---

## 🔧 依赖项

```txt
ezdxf>=1.0.0      # DXF 文件读写
simplekml>=1.3.6  # KML 文件生成
pyproj>=3.0.0     # 坐标转换
```

---

## 📖 文档

- [**CGCS2000 使用指南**](docs/guides/CGCS2000 指南.md) - 坐标系详细说明
- [**快速使用指南**](docs/guides/快速使用指南.md) - 5 分钟上手教程
- [**功能说明**](docs/guides/功能说明.md) - 完整功能列表
- [**贡献指南**](CONTRIBUTING.md) - 如何参与项目开发

---

## 🎯 常见问题

### Q: DWG 文件可以直接转换吗？
A: 不能。DWG 是 Autodesk 专有格式。需先在 AutoCAD 中使用 `DXFOUT` 命令导出为 DXF，或使用 ODA File Converter 转换。

### Q: 转换后位置偏移很大？
A: 检查中央子午线设置是否正确。中国地区通常使用 CGCS2000 高斯克吕格投影，根据项目位置选择正确的带号。

### Q: 如何知道使用什么坐标系？
A: 查看 CAD 图纸标题栏的坐标系信息，或咨询项目测量负责人。

### Q: 支持哪些 CAD 实体？
A: LINE, POLYLINE, CIRCLE, ARC, POINT, TEXT, INSERT。其他实体类型会跳过并记录日志。

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

详见 [贡献指南](CONTRIBUTING.md)。

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 📧 联系方式

- **开发者**: Wang Ningping
- **Email**: 174367449@qq.com
- **GitHub**: [@wangningping](https://github.com/wangningping)

---

## 🙏 致谢

感谢以下开源项目：

- [ezdxf](https://github.com/ezdxf/ezdxf) - DXF 文件读写
- [simplekml](https://github.com/kml4python/simplekml) - KML 文件生成
- [pyproj](https://github.com/pyproj4/pyproj) - 坐标转换

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by Wang Ningping

</div>
