# 🎙️ 语音对话功能 - 快速开始指南

欢迎使用 CGM Butler 的语音对话功能！本指南将帮助你在 **5 分钟内** 启动并测试语音对话。

---

## 📋 前提条件

### 必需软件
- ✅ **Node.js 18+** ([下载地址](https://nodejs.org/))
- ✅ **Python 3.11+** ([下载地址](https://www.python.org/downloads/))
- ✅ **PowerShell** (Windows 自带)

### 必需 API Keys
- 🔑 **Retell API Key** - 从 [Retell Dashboard](https://dashboard.retellai.com/) 获取
- 🔑 **OpenAI API Key** - 从 [OpenAI Platform](https://platform.openai.com/api-keys) 获取

---

## 🚀 快速开始（3 步）

### 第 1 步：配置环境变量

创建 `minerva/.env` 文件（如果不存在），添加以下内容：

```bash
# 🔴 必需：Retell API 配置
RETELL_API_KEY=your_retell_api_key_here
INTAKE_AGENT_ID=agent_c7d1cb2c279ec45bce38c95067
INTAKE_LLM_ID=llm_e54c307ce74090cdfd06f682523b

# 🔴 必需：OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# ✅ 已配置（无需修改）
CGM_BACKEND_URL=http://localhost:5000
MYSQL_DATABASE_URL=sqlite+aiosqlite:///./minerva_dev.db
SOP_MYSQL_DATABASE_URL=sqlite+aiosqlite:///./sop_dev.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**替换以下内容：**
- `your_retell_api_key_here` → 你的 Retell API Key
- `your_openai_api_key_here` → 你的 OpenAI API Key

---

### 第 2 步：安装依赖

```powershell
# 1. 安装前端依赖
cd cgm-avatar-app
npm install

# 2. 安装后端依赖（如果还没安装）
cd ..
pip install -r requirements.txt

# 3. 安装 Minerva 依赖
cd minerva
pip install -r requirements.txt
```

---

### 第 3 步：启动服务

**最简单的方式 - 一键启动：**

```powershell
# 回到项目根目录
cd "D:\cgm butler"

# 运行启动脚本（会自动启动 3 个服务）
.\start_services.ps1
```

**启动脚本会做什么？**
1. 🩺 启动 **CGM Butler 后端** (Flask, 端口 5000)
2. 🤖 启动 **Minerva 后端** (FastAPI, 端口 8000)
3. 📱 启动 **前端应用** (Vite, 端口 5173)

**等待启动完成** - 你会看到 3 个终端窗口打开。

---

## 🎤 开始使用

### 1. 访问应用
打开浏览器，访问：
```
http://localhost:5173
```

### 2. 导航到语音对话
1. 点击底部导航栏的 **"Olivia"** 标签
2. 点击 **"Voice Chat"** 按钮

### 3. 开始对话
1. 点击 **"Start Call"** 按钮
2. 🎤 **允许麦克风权限**（浏览器会提示）
3. 开始说话！AI 助手 Olivia 会回应你

### 4. 查看结果
- 📝 **通话中**: 实时转录显示在屏幕上
- 📊 **通话后**: 自动生成摘要和目标分析

---

## 🎯 测试对话示例

你可以尝试以下对话内容：

### 基础信息
```
Hi Olivia! I want to share my daily routine.
I wake up at 7 AM and go to bed at 11 PM.
For breakfast, I usually have oatmeal with berries at 8 AM.
```

### 饮食习惯
```
For lunch, I eat a salad with chicken at 12:30 PM.
Dinner is usually at 7 PM, I have fish or lean meat with vegetables.
I snack on fruits and nuts during the day.
```

### 运动和健康
```
I exercise 3 times a week, mostly cardio and light weights.
I drink about 8 glasses of water daily.
I don't smoke and only drink alcohol occasionally on weekends.
```

**结果**：通话结束后，你会看到：
- ✅ 结构化的摘要（饮食、运动、睡眠等）
- ✅ 目标达成分析和评分
- ✅ 个性化的健康建议

---

## 🔧 常见问题

### ❌ 问题 1: "Failed to create web call"
**原因**: Retell API Key 未配置或无效

**解决方案**:
1. 检查 `minerva/.env` 文件中的 `RETELL_API_KEY`
2. 确认 API Key 有效（访问 Retell Dashboard 检查）
3. 重启 Minerva 服务

### ❌ 问题 2: "Minerva backend not responding"
**原因**: Minerva 后端未启动或端口占用

**解决方案**:
```powershell
# 检查端口 8000 是否被占用
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

# 如果被占用，手动启动 Minerva
cd minerva
python -m uvicorn main:app --reload --port 8000
```

### ❌ 问题 3: "Microphone not working"
**原因**: 浏览器未授予麦克风权限

**解决方案**:
1. 点击浏览器地址栏左侧的 🔒 图标
2. 允许麦克风权限
3. 刷新页面（Ctrl + R）

### ❌ 问题 4: "Call summary taking too long"
**原因**: OpenAI API Key 未配置或网络问题

**解决方案**:
1. 检查 `minerva/.env` 中的 `OPENAI_API_KEY`
2. 检查网络连接
3. 查看 Minerva 终端窗口的错误日志

---

## 📁 文件结构

```
cgm-butler/
├── start_services.ps1           # ⭐ 主启动脚本
├── minerva/
│   ├── .env                     # ⭐ 后端配置（API Keys）
│   ├── main.py                  # FastAPI 应用
│   └── intake_phone_agent/      # 语音对话逻辑
│       ├── service.py           # 用户信息获取
│       └── webhook_handler.py   # Retell webhook
├── cgm-avatar-app/
│   ├── src/
│   │   ├── pages/VoiceChat/     # ⭐ 语音对话页面
│   │   ├── hooks/               # ⭐ Retell SDK Hooks
│   │   └── services/            # API 服务
│   └── vite.config.ts           # Vite 代理配置
└── dashboard/
    └── app.py                   # CGM Butler 后端
```

---

## 📖 进阶指南

如需了解更多信息：

- 📘 **完整集成指南**: [RETELL_WEB_CALL_INTEGRATION_GUIDE.md](./RETELL_WEB_CALL_INTEGRATION_GUIDE.md)
- 📗 **迁移方案**: [VOICE_CHAT_MIGRATION_PLAN.md](./VOICE_CHAT_MIGRATION_PLAN.md)
- 📙 **测试指南**: [TEST_GUIDE.md](./TEST_GUIDE.md)
- 📕 **进度追踪**: [MIGRATION_PROGRESS.md](./MIGRATION_PROGRESS.md)

---

## 🎉 成功标志

如果一切正常，你应该能：

- ✅ 打开 http://localhost:5173 看到 Olivia 主页
- ✅ 点击 "Voice Chat" 按钮进入语音对话页面
- ✅ 成功启动语音通话并听到 AI 回应
- ✅ 看到实时转录显示
- ✅ 通话结束后看到自动生成的摘要和分析

---

## 💡 提示

1. **首次使用** 建议使用 Chrome 或 Edge 浏览器（对 WebRTC 支持最好）
2. **麦克风测试** 可以先在浏览器设置中测试麦克风是否正常
3. **网络要求** 需要稳定的网络连接（Retell SDK 使用 WebRTC）
4. **开发模式** 启动脚本使用 `--reload`，修改代码会自动重启

---

## 🆘 需要帮助？

遇到问题？请查看：
- 🐛 **错误日志**: 查看 3 个终端窗口的输出
- 📝 **浏览器控制台**: 按 F12 查看前端错误
- 📧 **联系支持**: 提 Issue 到 [GitHub Repository](https://github.com/yijialiu-aigeekgo/cgm_butler)

---

**祝你使用愉快！🚀**

