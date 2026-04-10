# GitHub 发布检查清单

## 📋 发布前准备

### 1. 代码质量检查
- [ ] 所有 Python 文件语法正确
- [ ] 导入测试通过 (`python -c "import dwg2kml"`)
- [ ] CLI 帮助正常显示 (`python dwg2kml.py --help`)
- [ ] GUI 可以正常启动 (`python dwg2kml_gui.py`)
- [ ] 中英文切换功能正常
- [ ] 坐标转换精度验证通过

### 2. 文档检查
- [x] README.md 完整且格式正确
- [x] README_EN.md 英文版本完整
- [x] LICENSE 文件存在（MIT）
- [x] CONTRIBUTING.md 贡献指南
- [x] .gitignore 配置正确
- [x] requirements.txt 包含所有依赖
- [x] pyproject.toml 项目配置

### 3. 示例和测试
- [ ] examples/ 目录包含示例 DXF 文件
- [ ] docs/screenshots/ 包含 GUI 截图
- [ ] 测试文件已清理（verify_*.py 等）
- [ ] __pycache__ 已删除

### 4. GitHub 配置
- [x] .github/workflows/ci-cd.yml CI/CD 配置
- [ ] GitHub 用户名已替换（README 中的 USER 占位符）
- [ ] 仓库描述准备

---

## 🚀 发布步骤

### 步骤 1: 运行上传脚本

```bash
# 在项目根目录
upload-to-github.bat
```

输入你的 GitHub 用户名，脚本会自动：
- 替换所有 README 中的 USER 占位符
- 初始化 Git 仓库
- 提交所有文件

### 步骤 2: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写信息：
   - **Repository name**: `dwg2kml`
   - **Description**: `Convert DXF files to KML format with CGCS2000 support`
   - **Visibility**: ✅ Public
   - **☑️ 不要勾选** "Add a README file"
   - **☑️ 不要勾选** ".gitignore"
   - **☑️ 不要勾选** "License"
3. 点击 **"Create repository"**

### 步骤 3: 推送代码

根据上传脚本的提示，执行推送命令：

```bash
# HTTPS 方式（推荐新手）
git remote add origin https://github.com/YOUR_USERNAME/dwg2kml.git
git branch -M main
git push -u origin main

# 或 SSH 方式（如果配置了 SSH 密钥）
git remote add origin git@github.com:YOUR_USERNAME/dwg2kml.git
git branch -M main
git push -u origin main
```

### 步骤 4: 验证仓库

- [ ] 访问 https://github.com/YOUR_USERNAME/dwg2kml
- [ ] 确认所有文件已上传
- [ ] README 显示正常（无 USER 占位符）
- [ ] CI/CD Actions 自动触发

### 步骤 5: 创建第一个 Release

1. 访问 https://github.com/YOUR_USERNAME/dwg2kml/releases/new
2. 填写信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**: 
     ```markdown
     ## 🎉 首次发布

     ### 功能特性
     - ✅ DXF 到 KML 转换
     - ✅ CGCS2000 坐标系支持
     - ✅ UTM 投影支持
     - ✅ GUI + CLI 双模式
     - ✅ 中英文双语界面
     - ✅ 批量转换
     - ✅ 中央子午线配置（度分秒）
     - ✅ 专业参数（假东、假北、投影面高程）

     ### 安装
     ```bash
     pip install dwg2kml
     ```

     ### 使用
     ```bash
     python dwg2kml_gui.py
     ```

     ### 文档
     - [快速使用指南](docs/guides/快速使用指南.md)
     - [CGCS2000 指南](docs/guides/CGCS2000 指南.md)
     ```
   - **☑️ Set as the latest release**
3. 点击 **"Publish release"**

### 步骤 6: 配置 PyPI（可选）

如果要发布到 PyPI：

1. 在 https://pypi.org/manage/account/token/ 创建 API token
2. 在 GitHub 仓库 Settings → Secrets and variables → Actions 添加：
   - **Name**: `PYPI_API_TOKEN`
   - **Value**: `pypi-xxxxx...`
3. 创建 Release 时会自动发布到 PyPI

---

## ✅ 发布后验证

### 1. 仓库页面
- [ ] README 显示正常
- [ ] 徽章显示正确（CI/CD、License、Python 版本）
- [ ] 文件结构清晰
- [ ] 截图正常显示

### 2. GitHub Actions
- [ ] CI/CD workflow 自动运行
- [ ] 所有测试通过
- [ ] 构建成功

### 3. 功能验证
- [ ] 可以从 GitHub 克隆项目
- [ ] 可以安装依赖
- [ ] GUI 可以启动
- [ ] CLI 可以运行
- [ ] 转换功能正常

---

## 📊 推广建议

### 1. 社交媒体
- [ ] 分享到 Twitter/X
- [ ] 分享到 LinkedIn
- [ ] 分享到知乎
- [ ] 分享到相关技术社区

### 2. 技术社区
- [ ] GitHub Topics 添加标签：`dxf`, `kml`, `gis`, `cad`, `cgcs2000`, `china`
- [ ] 提交到 Python 相关目录
- [ ] 分享到 CAD/GIS 论坛

### 3. 文档完善
- [ ] 添加更多示例文件
- [ ] 录制使用视频
- [ ] 编写详细 API 文档
- [ ] 添加常见问题解答

---

## 🎯 后续版本规划

### v1.1.0
- [ ] 支持更多 CAD 实体类型
- [ ] 添加图层过滤功能
- [ ] 支持颜色映射
- [ ] 添加坐标系自动检测

### v1.2.0
- [ ] Web 界面支持
- [ ] 在线转换服务
- [ ] 支持更多坐标系
- [ ] 添加坐标系预览

### v2.0.0
- [ ] 支持 DWG 直接读取（通过 ODA）
- [ ] 3D 实体支持
- [ ] 纹理映射
- [ ] 批量坐标系统一转换

---

## 📧 联系方式

- **开发者**: Wang Ningping
- **Email**: 174367449@qq.com
- **GitHub**: https://github.com/YOUR_USERNAME

---

**祝发布顺利！🎉**
