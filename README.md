# 🎯 Android APK 下载链接捕获工具

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

一个强大的工具集，专门用于抓取和分析 Android 应用的网络请求，特别是阿里云盘等云存储服务的下载链接。

## ✨ 主要特性

🚀 **一键启动** - 集成化界面，新手友好  
📱 **Android 支持** - 完美适配 Android 模拟器  
🔐 **HTTPS 抓取** - 支持 HTTPS/HTTP 双协议抓取  
🔗 **智能提取** - 自动识别和提取真实下载链接  
📊 **数据分析** - 强大的日志分析和搜索功能  
🎨 **彩色界面** - 美观的彩色控制台输出  
⚡ **实时监控** - 实时显示网络请求  
💾 **数据持久化** - 自动保存 JSON 和文本日志

## 🎬 效果展示

```
🎯 阿里云盘下载链接捕获工具
============================================================
📱 抓取APK应用的下载请求
🔗 自动提取真实下载链接
✅ 验证链接有效性
💾 保存结果到文件
```

> **注意**: 本项目仅用于学习和研究目的，请遵守相关法律法规。

## 📋 系统要求

- **操作系统**: macOS 10.14+ (已在 macOS 24.3.0 测试)
- **Python**: 3.7 或更高版本
- **Android 模拟器**: Android Studio AVD、Genymotion 等
- **网络**: 支持 HTTP 代理的网络环境

## 🚀 快速开始

### 1️⃣ 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/listen_i4k_api.git
cd listen_i4k_api
```

### 2️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 3️⃣ 一键启动 (推荐)

```bash
python start_capture.py
```

选择菜单选项 1，工具会自动：

- 启动代理服务器
- 提供模拟器配置指导
- 实时捕获网络请求
- 分析提取下载链接

### 4️⃣ 配置 Android 模拟器

1. **设置代理**: `10.0.2.2:8080`
2. **安装证书**: 访问 `mitm.it` 下载证书
3. **执行操作**: 在 APK 中点击下载按钮

## 📚 详细使用指南

### 🛠️ 手动启动模式

如果需要更精细的控制：

```bash
# 启动代理服务器
python start_proxy.py

# 分析现有日志
python download_link_extractor.py

# 测试提取的链接
python test_download_link.py
```

### 📊 数据分析工具

```bash
# 分析所有请求日志
python log_analyzer.py

# 分析URL结构
python url_analyzer.py
```

### 📁 项目结构

```
listen_i4k_api/
├── start_capture.py          # 🎯 一键启动工具 (推荐)
├── proxy_interceptor.py      # 🔐 HTTPS代理拦截器
├── download_link_extractor.py # 🔗 下载链接提取器
├── test_download_link.py     # ✅ 链接有效性测试
├── url_analyzer.py          # 📊 URL结构分析
├── log_analyzer.py          # 📈 日志分析工具
├── start_proxy.py           # 🚀 代理服务器启动
├── setup_android_proxy.py   # 📱 Android配置助手
├── requirements.txt         # 📦 Python依赖
├── README.md               # 📖 项目说明
├── USAGE_GUIDE.md          # 📋 详细使用指南
└── logs/                   # 📁 日志文件目录
```

## 🔧 配置说明

### 代理设置

- **代理端口**: 8080
- **模拟器配置**: `10.0.2.2:8080`
- **证书安装**: 访问 `http://mitm.it`

### 日志文件

抓取的数据保存在 `logs/` 目录：

- `api_requests_*.json` - 完整请求响应数据
- `console_log_*.txt` - 控制台输出日志
- `extracted_download_links.json` - 提取的下载链接

## 🎯 核心功能详解

### 🔗 下载链接提取

工具能自动识别和提取：

- 阿里云盘分享链接
- 真实下载 URL
- 临时访问令牌
- 文件元数据信息

### 📊 智能分析

- **URL 结构解析**: 分析云存储 URL 的组成
- **参数解码**: 自动解码 Base64 和 URL 编码
- **有效性检测**: 测试链接是否可用
- **过期时间**: 显示链接过期时间

## ⚠️ 注意事项

- 🔒 本工具仅用于**学习研究**，请遵守法律法规
- 📱 需要 Android 模拟器支持代理设置
- 🔐 HTTPS 需要安装证书才能抓取
- ⏰ 下载链接通常有时效性限制

## 🛠️ 故障排除

### 常见问题

**Q: 无法抓取 HTTPS 请求**

```bash
# 检查证书是否安装
# 访问 http://mitm.it 重新安装证书
```

**Q: 模拟器连接失败**

```bash
# 检查ADB连接
adb devices
```

**Q: 代理无法启动**

```bash
# 检查端口是否被占用
lsof -i :8080
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [mitmproxy](https://mitmproxy.org/) - 强大的 HTTPS 代理工具
- [colorama](https://pypi.org/project/colorama/) - 跨平台彩色终端文本
- [requests](https://requests.readthedocs.io/) - 优雅的 HTTP 库

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
