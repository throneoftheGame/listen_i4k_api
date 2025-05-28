# 🚀 Android HTTPS API 抓取工具 - 使用指南

## 📋 系统已就绪状态

✅ **依赖已安装** - mitmproxy 10.1.6 和相关库已成功安装  
✅ **ADB 已配置** - Android Debug Bridge 可正常使用  
✅ **模拟器已检测** - 1 个 Android 模拟器正在运行  
✅ **代理服务器已测试** - 可正常在端口 8080 监听

## 🎯 完整操作流程

### 步骤 1️⃣：启动一键配置工具

```bash
python quick_start.py
```

这将为您提供一个友好的菜单界面。

### 步骤 2️⃣：配置 Android 模拟器代理

在一键配置工具中选择 `1. 配置模拟器代理设置`

或者直接运行：

```bash
python setup_android_proxy.py
```

这将自动配置您的 Android 模拟器使用代理 `10.0.2.2:8080`

### 步骤 3️⃣：安装 HTTPS 证书

#### 3.1 启动代理服务器

在一键配置工具中选择 `2. 启动代理服务器`

或者直接运行：

```bash
python start_proxy.py
```

#### 3.2 在模拟器中安装证书

1. 在 Android 模拟器中打开浏览器
2. 访问：`http://mitm.it`
3. 点击 "Get mitmproxy-ca-cert.pem" 下载证书
4. 在 Android 设置中安装证书：
   - 设置 → 安全 → 加密和凭据 → 从存储设备安装
   - 选择下载的证书文件
   - 为证书命名（如：mitmproxy）
   - 选择用途：VPN 和应用

### 步骤 4️⃣：开始抓取 API

现在一切就绪！在模拟器中打开您的 APK 应用：

1. **登录操作** - 当您点击登录时，将看到：

   ```
   📤 [请求] POST https://api.example.com/login
   ⏰ 时间: 2024-01-01T12:00:00.123456
   📦 请求体: {"username": "user", "password": "pass"}

   📥 [响应] 200 OK
   📄 响应体预览: {"token": "abc123", "user_id": 456}
   ```

2. **其他操作** - 所有 HTTPS 请求都会被实时显示和记录

### 步骤 5️⃣：分析抓取数据

#### 5.1 实时查看

所有 API 调用都会在代理服务器的控制台实时显示。

#### 5.2 分析历史数据

```bash
python log_analyzer.py
```

分析工具提供：

- **总览统计** - 域名分布、方法统计、状态码分析
- **搜索过滤** - 按关键词、方法、状态码搜索
- **详细查看** - 查看单个请求的完整信息
- **导出功能** - 导出分析结果

## 📁 数据存储位置

所有抓取的数据保存在 `logs/` 目录：

```
logs/
├── api_requests_20240101_120000.json    # 完整API数据
└── console_log_20240101_120000.txt      # 控制台日志
```

## 🔧 常用命令

```bash
# 启动一键工具
python quick_start.py

# 直接启动代理
python start_proxy.py

# 配置模拟器代理
python setup_android_proxy.py

# 重置代理设置
python setup_android_proxy.py reset

# 查看证书安装指南
python setup_android_proxy.py cert

# 分析日志
python log_analyzer.py
```

## 📊 数据格式说明

抓取的数据采用 JSON 格式：

```json
{
  "request": {
    "timestamp": "2024-01-01T12:00:00.123456",
    "method": "POST",
    "url": "https://api.example.com/login",
    "host": "api.example.com",
    "path": "/login",
    "headers": {
      "Content-Type": "application/json",
      "User-Agent": "MyApp/1.0"
    },
    "query_params": {},
    "body": {
      "username": "testuser",
      "password": "testpass"
    }
  },
  "response": {
    "status_code": 200,
    "status_text": "OK",
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "success": true,
      "token": "abc123xyz",
      "user_id": 12345
    }
  }
}
```

## 🎯 实际使用示例

### 抓取登录接口

1. 启动代理服务器
2. 在 APK 中点击登录按钮
3. 立即在终端看到：

```
📤 [请求] POST https://api.myapp.com/auth/login
⏰ 时间: 2024-01-01T15:30:25.123456
📦 请求体: {
  "email": "user@example.com",
  "password": "mypassword",
  "device_id": "android_123456"
}

📥 [响应] 200 OK
📄 响应体预览: {
  "success": true,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "def456...",
  "expires_in": 3600,
  "user": {
    "id": 12345,
    "name": "Test User",
    "email": "user@example.com"
  }
}
```

### 抓取 API 调用

当您在 APK 中执行任何操作时，所有相关的 API 请求都会被捕获：

- 获取用户信息
- 上传文件
- 发送消息
- 数据同步
- 等等...

## 🛠 故障排除

### 问题 1：无法抓取 HTTPS 流量

**解决方案**：

- 确保已正确安装 mitmproxy 证书
- 检查 Android 模拟器代理设置
- 重启模拟器后重新设置

### 问题 2：代理服务器启动失败

**解决方案**：

- 检查端口 8080 是否被占用：`lsof -i :8080`
- 重新安装依赖：`pip install -r requirements.txt`

### 问题 3：模拟器无法连接代理

**解决方案**：

- 确保使用正确的代理地址：`10.0.2.2:8080`
- 检查 ADB 连接：`adb devices`
- 重新配置代理：`python setup_android_proxy.py`

## 🔒 安全提醒

⚠️ **重要**：

- 本工具仅用于合法的应用调试和开发
- 请遵守相关法律法规
- 不要用于非法获取他人数据

## 🎉 开始使用

现在您可以开始抓取 APK 的 HTTPS 接口了！

1. 运行 `python quick_start.py`
2. 按照步骤操作
3. 在模拟器中使用您的 APK
4. 观察并分析 API 调用

祝您使用愉快！🚀
