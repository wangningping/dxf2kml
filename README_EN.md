# DXF to KML Converter

<div align="center">

[![CI/CD](https://github.com/wangningping/dxf2kml/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/wangningping/dxf2kml/actions/workflows/ci-cd.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub release](https://img.shields.io/github/v/release/wangningping/dxf2kml)](https://github.com/wangningping/dxf2kml/releases)

**Professional tool for converting DXF files to Google Earth KML format**

English | [简体中文](README.md)

</div>

---

## 📋 Features

- �?**DXF Direct Conversion** - Support AutoCAD DXF format
- �?**Multiple CAD Entities** - LINE, POLYLINE, CIRCLE, ARC, POINT, TEXT, INSERT
- �?**CGCS2000 Coordinate System** - Full support for China Geodetic Coordinate System 2000
- �?**UTM Projection** - Universal Transverse Mercator support
- �?**Batch Conversion** - Process multiple files at once
- �?**Bilingual Interface** - Chinese/English one-click switch
- �?**GUI + CLI** - Both graphical and command-line interfaces
- �?**Professional Parameters** - Central meridian, false easting, false northing, elevation

---

## 🚀 Quick Start

### Method 1: One-Click Launch (Windows)

```bash
# After downloading the project
onekeystart.bat
```

### Method 2: Install via pip

```bash
# Install
pip install dxf2kml

# Use command-line tool
dxf2kml input.dxf -o output.kml
```

### Method 3: Run from Source

```bash
# Clone repository
git clone https://github.com/wangningping/dxf2kml.git
cd dxf2kml

# Install dependencies
pip install -r requirements.txt

# Launch GUI
python dxf2kml_gui.py
```

---

## 💻 Usage

### Graphical Interface (GUI)

```bash
python dxf2kml_gui.py
```

**Features:**
- 📁 File picker
- 🌐 Coordinate system configuration (CGCS2000/UTM)
- 📍 Central meridian setting (DMS format)
- 📊 Real-time conversion log
- 🌍 Chinese/English switch

![GUI Screenshot](docs/screenshots/gui_main.png)

### Command Line (CLI)

```bash
# Single file conversion
python dxf2kml.py input.dxf -o output.kml

# Batch conversion
python dxf2kml.py --batch ./dxf_folder -o ./kml_output

# Using CGCS2000 (Beijing area)
python dxf2kml.py input.dxf -o output.kml --cgcs2000-3deg 39

# Using UTM
python dxf2kml.py input.dxf -o output.kml --utm --zone 50

# View help
python dxf2kml.py --help
```

---

## 🌍 Coordinate Systems

### CGCS2000 (Recommended for China)

| City | 3° Zone | 6° Zone | Central Meridian |
|------|---------|---------|------------------|
| Beijing | Zone 39 | Zone 20 | 117°E |
| Shanghai | Zone 41 | Zone 21 | 123°E |
| Guangzhou | Zone 38 | Zone 20 | 114°E |
| Shenzhen | Zone 38 | Zone 20 | 114°E |
| Hangzhou | Zone 40 | Zone 21 | 120°E |
| Zhejiang Jinhua | Zone 40 | Zone 20 | 119°45′E |

**Formulas:**
- 3° Zone: Central Meridian = Zone Number × 3
- 6° Zone: Central Meridian = Zone Number × 6 - 3

### UTM (Global)

Supports North and South hemispheres, zones 1-60.

---

## 📁 Project Structure

```
dxf2kml/
├── dxf2kml.py              # Command-line tool
├── dxf2kml_gui.py          # Graphical interface
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── LICENSE                # MIT License
├── README.md              # 中文说明
├── README_EN.md           # English README
├── onekeystart.bat        # Windows one-click launch
├── install.bat            # Windows install script
├── docs/
�?  ├── guides/            # wangningping guides
�?  �?  ├── CGCS2000 指南.md
�?  �?  ├── 快速使用指�?md
�?  �?  └── 功能说明.md
�?  └── screenshots/       # Screenshots
├── examples/              # Example files
└── .github/
    └── workflows/         # GitHub Actions
        └── ci-cd.yml      # CI/CD configuration
```

---

## 🔧 Dependencies

```txt
ezdxf>=1.0.0      # DXF file reading/writing
simplekml>=1.3.6  # KML file generation
pyproj>=3.0.0     # Coordinate transformation
```

---

## 📖 Documentation

- [**CGCS2000 Guide**](docs/guides/CGCS2000 指南.md) - Detailed coordinate system explanation
- [**Quick Start Guide**](docs/guides/快速使用指�?md) - 5-minute tutorial
- [**Features**](docs/guides/功能说明.md) - Complete feature list
- [**Contributing**](CONTRIBUTING.md) - How to contribute

---

## 🎯 FAQ

### Q: Can DWG files be converted directly?
A: No. DWG is Autodesk proprietary format. Export to DXF using `DXFOUT` command in AutoCAD, or use ODA File Converter.

### Q: Large position offset after conversion?
A: Check if the central meridian is set correctly. For China, use CGCS2000 Gauss-Kruger projection with the correct zone number.

### Q: How to know which coordinate system to use?
A: Check the title block of the CAD drawing or consult the project surveyor.

### Q: Which CAD entities are supported?
A: LINE, POLYLINE, CIRCLE, ARC, POINT, TEXT, INSERT. Other entity types will be skipped and logged.

---

## 🤝 Contributing

Contributions welcome! Code, issues, suggestions - all appreciated.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

See [Contributing Guide](CONTRIBUTING.md) for details.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 📧 Contact

- **Developer**: Wang Ningping
- **Email**: 174367449@qq.com
- **GitHub**: [@wangningping](https://github.com/wangningping)

---

## 🙏 Acknowledgments

Thanks to these open-source projects:

- [ezdxf](https://github.com/ezdxf/ezdxf) - DXF file reading/writing
- [simplekml](https://github.com/kml4python/simplekml) - KML file generation
- [pyproj](https://github.com/pyproj4/pyproj) - Coordinate transformation

---

<div align="center">

**If this project helps you, please give it a ⭐️ Star!**

Made with ❤️ by Wang Ningping

</div>
