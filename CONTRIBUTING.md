# 贡献指南

感谢你考虑为 DXF to KML 转换器做出贡献！

## 如何贡献

### 报告问题
- 使用 GitHub Issues 报告 bug 或提出新功能建议
- 提供详细的复现步骤和环境信息
- 附上相关的 DXF 文件（如果可能）

### 提交代码
1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/dwg2kml.git
cd dwg2kml

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# 安装依赖
pip install -r requirements.txt
```

## 代码规范

### Python 代码
- 遵循 PEP 8 代码风格
- 使用有意义的变量名和函数名
- 添加必要的注释和文档字符串

### 提交信息
- 使用清晰的提交信息
- 格式：`type: description`
- 例如：
  - `feat: 添加 UTM 投影支持`
  - `fix: 修复坐标转换精度问题`
  - `docs: 更新 README 文档`

## 功能建议

我们特别欢迎以下类型的贡献：

### 新增功能
- 支持更多 CAD 实体类型
- 支持其他坐标系（如地方坐标系）
- 改进 GUI 界面
- 性能优化

### 文档改进
- 修正文档错误
- 补充使用示例
- 翻译文档

### Bug 修复
- 修复已知问题
- 改进错误处理
- 增强兼容性

## 测试

提交代码前请确保：
- 所有现有功能正常工作
- 新增功能有测试用例
- 代码没有语法错误

## 许可证

通过贡献代码，你同意你的贡献遵循本项目的 MIT 许可证。

## 联系方式

如有问题，请通过 GitHub Issues 联系我们。
