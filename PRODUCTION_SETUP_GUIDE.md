# CGM Butler Voice Chat - 生产环境设置指南

## ✅ 前置条件检查

### 1. Retell Python SDK 已安装
```bash
cd "D:\cgm butler\minerva"
pip list | grep retell
# 应该看到：retell-sdk
```

如果没有安装：
```bash
pip install retell-sdk
```

### 2. 环境变量配置

#### Minerva 后端 (`.env`)
在 `D:\cgm butler\minerva\.env` 中添加：

```env
# Retell API Configuration
RETELL_API_KEY=your_retell_api_key_here
INTAKE_AGENT_ID=agent_c7d1cb2c279ec45bce38c95067
INTAKE_LLM_ID=llm_e54c307ce74090cdfd06f682523b

# CGM Butler Backend URL
CGM_BACKEND_URL=http://localhost:5000

# OpenAI (用于生成 summary 和 goal analysis)
OPENAI_API_KEY=your_openai_api_key_here
```

**获取 Retell API Key：**
1. 登录 https://retellai.com/dashboard
2. 进入 Settings → API Keys
3. 复制 API Key

#### 前端 (`.env.local`)
在 `D:\cgm butler\cgm-avatar-app\.env.local` 中：

```env
VITE_MINERVA_BACKEND_URL=http://localhost:8000
VITE_RETELL_AGENT_ID=agent_c7d1cb2c279ec45bce38c95067
VITE_RETELL_LLM_ID=llm_e54c307ce74090cdfd06f682523b
VITE_BACKEND_URL=http://localhost:5000
VITE_DEFAULT_USER_ID=user_001
```

---

## 🚀 启动服务

### 方式 1: 使用 PowerShell 脚本（推荐）

**一键启动所有服务：**
```powershell
cd "D:\cgm butler"
.\start_services.ps1
```

这会自动启动：
1. CGM Butler Dashboard (Flask) - http://localhost:5000
2. Minerva Backend (FastAPI) - http://localhost:8000
3. Frontend (Vite) - http://localhost:5173

### 方式 2: 手动启动

#### 1. 启动 CGM Butler Dashboard
```powershell
cd "D:\cgm butler\dashboard"
$env:Path += ";C:\Program Files\nodejs"
python app.py
```

#### 2. 启动 Minerva Backend
```powershell
cd "D:\cgm butler\minerva"
$env:Path += ";C:\Program Files\nodejs"
python -m uvicorn main:app --reload --port 8000
```

#### 3. 启动前端
```powershell
cd "D:\cgm butler\cgm-avatar-app"
$env:Path += ";C:\Program Files\nodejs"
npm run dev
```

---

## 🧪 测试流程

### 1. 测试后端 API

**测试 Retell Web Call 创建：**
```powershell
curl -X POST http://localhost:8000/intake/create-web-call `
  -H "Content-Type: application/json" `
  -d '{"user_id": "user_001"}'
```

**预期响应：**
```json
{
  "access_token": "rtl_xxx...",
  "call_id": "call_xxx...",
  "agent_id": "agent_c7d1cb2c279ec45bce38c95067",
  "user_name": "Julia Chen",
  "message": "Web call created successfully"
}
```

如果失败，检查：
- ✅ `RETELL_API_KEY` 是否正确
- ✅ `INTAKE_AGENT_ID` 是否存在于 Retell Dashboard
- ✅ Minerva 后端日志中的错误信息

### 2. 测试前端集成

**打开浏览器：**
```
http://localhost:5173
```

**测试步骤：**
1. 点击 "Voice Chat" 按钮
2. 观察浏览器控制台：
   ```
   🔑 Requesting access token...
   ✅ Web call created: {access_token: "...", call_id: "..."}
   📞 Starting Retell call...
   ✅ Call started successfully
   ```
3. 应该能听到 Olivia 的语音："Hello! I'm Olivia, your health coach..."
4. 说话测试麦克风是否工作
5. 点击 "End Call"
6. 切换到 "Goals Achievement" tab 查看结果

---

## 🐛 常见问题排查

### 问题 1: "Failed to create web call"

**可能原因：**
- Minerva 后端未启动
- CORS 错误
- Retell API Key 错误

**解决方法：**
```powershell
# 检查 Minerva 是否运行
curl http://localhost:8000/docs

# 查看 Minerva 日志
# (在运行 Minerva 的窗口查看错误)
```

### 问题 2: "Retell SDK 未加载"

**可能原因：**
- CDN 被墙或网络问题

**解决方法：**
1. 检查浏览器控制台的网络错误
2. 如果 CDN 无法访问，代码会自动降级使用 Mock 模式

### 问题 3: CORS 错误

**错误信息：**
```
Access to XMLHttpRequest at 'http://localhost:8000/intake/create-web-call' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**解决方法：**
检查 `minerva/main.py` 是否有 CORS 配置：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 问题 4: "No audio input detected"

**解决方法：**
1. 检查浏览器权限：允许麦克风访问
2. 在浏览器地址栏左侧点击🔒图标
3. 确保 "Microphone" 设置为 "Allow"

---

## 📊 监控和日志

### Minerva 后端日志

重要的日志信息：
```
==== Creating CGM Butler web call for user_id: user_001
==== LLM dynamic variables: ['user_name', 'user_age', 'user_health_goal', ...]
==== Using agent_id: agent_c7d1cb2c279ec45bce38c95067
==== ✅ Web call created successfully: call_xxx...
```

### 前端控制台日志

正常流程：
```
🔑 Requesting access token...
✅ Web call created: {access_token: "rtl_xxx", call_id: "call_xxx"}
📞 Starting Retell call...
✅ Retell client initialized
📞 Call started
✅ Call started successfully
```

---

## 🔄 开发模式 vs 生产模式

### 开发模式 (Mock)
- 自动检测：`import.meta.env.DEV === true`
- 不调用后端 API
- 使用 Mock Retell Client 和 Mock 数据
- 适用于：UI 开发、样式调整

### 生产模式 (Production)
- 运行：`npm run build && npm run preview`
- 调用真实的 Retell API
- 需要后端服务运行
- 适用于：功能测试、真实通话

**切换到生产模式测试：**
```powershell
cd "D:\cgm butler\cgm-avatar-app"
npm run build
npm run preview
```

然后访问：http://localhost:4173

---

## ✅ 完整测试清单

- [ ] CGM Butler Dashboard 运行 (http://localhost:5000)
- [ ] Minerva Backend 运行 (http://localhost:8000)
- [ ] 前端运行 (http://localhost:5173)
- [ ] 环境变量已配置 (`.env` 和 `.env.local`)
- [ ] 后端 API 测试成功 (curl 测试)
- [ ] 前端可以创建 web call
- [ ] 可以听到 Olivia 的语音
- [ ] 麦克风工作正常
- [ ] Transcript 实时显示
- [ ] Call Results 页面显示正确
- [ ] Goals Achievement 显示 3 个目标卡片

---

## 📞 技术支持

如果遇到问题：

1. **检查日志**：
   - Minerva 后端日志（运行窗口）
   - 浏览器控制台（F12）
   - CGM Butler Dashboard 日志

2. **验证环境变量**：
   ```powershell
   # Minerva
   cd "D:\cgm butler\minerva"
   Get-Content .env
   
   # 前端
   cd "D:\cgm butler\cgm-avatar-app"
   Get-Content .env.local
   ```

3. **重启所有服务**：
   - 停止所有窗口 (Ctrl+C)
   - 重新运行 `start_services.ps1`

4. **清除缓存**：
   - 浏览器：Ctrl+Shift+R 强制刷新
   - 前端：删除 `node_modules/.vite` 文件夹

---

**准备好后，运行 `start_services.ps1` 开始测试！** 🚀

