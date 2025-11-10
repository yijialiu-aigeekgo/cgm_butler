# 🧪 Voice Chat 功能测试指南

## 📋 测试前准备清单

### ✅ 第一步：安装前端依赖

```bash
cd cgm-avatar-app
npm install
```

**预期结果**：应该看到依赖安装成功，包括：
- `@retell-ai/web-client`
- `axios`
- `react-router-dom`
- `@types/react-router-dom`

---

### ✅ 第二步：配置环境变量

#### 2.1 前端环境变量

在 `cgm-avatar-app` 目录下创建 `.env.local` 文件：

```bash
# 在项目根目录执行
cd cgm-avatar-app
echo "VITE_MINERVA_BACKEND_URL=http://localhost:8000" > .env.local
echo "VITE_RETELL_AGENT_ID=agent_c7d1cb2c279ec45bce38c95067" >> .env.local
echo "VITE_RETELL_LLM_ID=llm_e54c307ce74090cdfd06f682523b" >> .env.local
echo "VITE_BACKEND_URL=http://localhost:5000" >> .env.local
echo "VITE_DEFAULT_USER_ID=user_001" >> .env.local
```

或者手动创建 `cgm-avatar-app/.env.local`：
```
VITE_MINERVA_BACKEND_URL=http://localhost:8000
VITE_RETELL_AGENT_ID=agent_c7d1cb2c279ec45bce38c95067
VITE_RETELL_LLM_ID=llm_e54c307ce74090cdfd06f682523b
VITE_BACKEND_URL=http://localhost:5000
VITE_DEFAULT_USER_ID=user_001
```

#### 2.2 后端环境变量

检查 `minerva/.env` 文件，确保包含以下内容：

```bash
CGM_BACKEND_URL=http://localhost:5000
INTAKE_AGENT_ID=agent_c7d1cb2c279ec45bce38c95067
INTAKE_LLM_ID=llm_e54c307ce74090cdfd06f682523b

# 以下是原有的环境变量，保持不变
RETELL_API_KEY=your_retell_api_key
OPENAI_API_KEY=your_openai_api_key
```

**注意**：如果 `minerva/.env` 不存在，从 `minerva/.env.example` 复制一份并修改。

---

### ✅ 第三步：启动所有服务（需要 3 个终端）

#### Terminal 1: CGM Butler Dashboard (Flask)
```bash
cd dashboard
python app.py
```

**预期输出**：
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

**验证**：打开浏览器访问 `http://localhost:5000/api/user/user_001`，应该看到用户信息 JSON。

---

#### Terminal 2: Minerva 后端 (FastAPI)
```bash
cd minerva
uvicorn main:app --reload --port 8000
```

**预期输出**：
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**验证**：打开浏览器访问 `http://localhost:8000/docs`，应该看到 FastAPI Swagger 文档。

---

#### Terminal 3: 前端 (Vite + React)
```bash
cd cgm-avatar-app
npm run dev
```

**预期输出**：
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## 🧪 开始测试

### 测试 1: 访问首页

1. 打开浏览器访问 `http://localhost:5173`
2. **预期看到**：
   - 模拟手机界面（MobileFrame）
   - "Olivia" 标题
   - 机器人图标 🤖
   - "Talk with Olivia" 区域
   - 两个按钮："Voice Chat" 和 "Video Chat"

**如果页面显示错误**，打开浏览器开发者工具（F12）查看 Console 错误。

---

### 测试 2: 进入 Voice Chat 页面

1. 点击 **"Voice Chat"** 按钮
2. **预期看到**：
   - 页面跳转到语音对话界面
   - 顶部显示状态栏："准备开始"
   - 中间区域显示 "等待对话开始..."
   - 底部有 **"开始通话"** 按钮（紫色）

---

### 测试 3: 开始语音通话 ⭐ 核心测试

1. 点击 **"开始通话"** 按钮
2. **预期流程**：
   
   **步骤 1**: 连接中
   - 按钮文字变为 "连接中..."
   - 状态指示器变为黄色
   - 状态文字显示 "连接中..."

   **步骤 2**: 通话建立
   - 浏览器可能会请求**麦克风权限** → **点击"允许"**
   - 状态指示器变为绿色
   - 状态文字显示 "通话中"
   - 底部按钮变为：**"🎤 静音"** 和 **"结束通话"**

   **步骤 3**: 对话进行
   - 说话后，实时 transcript 应该在中间区域显示
   - Olivia（AI）的回复显示为紫色气泡
   - 您的话显示为蓝色气泡

---

### 测试 4: 静音功能

1. 通话过程中，点击 **"🎤 静音"** 按钮
2. **预期**：
   - 按钮背景变为黄色
   - 文字变为 "🔇 取消静音"
3. 再次点击恢复

---

### 测试 5: 结束通话

1. 点击 **"结束通话"** 按钮（红色）
2. **预期流程**：
   
   **步骤 1**: 通话结束
   - 状态变为 "通话结束"
   - 1.5 秒后自动跳转到结果页面

   **步骤 2**: 加载分析结果
   - 显示 "正在生成分析结果..." 加载动画
   - 后台调用 Minerva API 生成 Summary 和 Goals Analysis

   **步骤 3**: 显示结果
   - 顶部显示 "通话结果" 标题
   - Tab 切换："摘要" 和 "目标达成"

---

### 测试 6: 查看 Summary (摘要) Tab

在结果页面，查看 **"摘要"** Tab：

**预期内容**：
- 🍽️ 饮食：早餐、午餐、晚餐、零食
- 🏃 运动
- 😴 睡眠
- 🥤 饮品
- 🚭 生活方式：吸烟、饮酒
- 🧠 心理健康
- 📝 补充信息

**注意**：如果通话时间太短（<30秒），可能显示 "通话数据不足"。

---

### 测试 7: 查看 Goals Achievement Tab

点击 **"目标达成"** Tab：

**预期内容**：
- 🎯 您的健康目标
- 📊 达成度（进度条 + 百分比）
- ✅ 做得好的方面（列表）
- 📈 可以改进的方面（列表）
- 💡 建议（列表）
- 📝 总结

---

### 测试 8: 返回首页

1. 点击左上角 **"← 返回"** 按钮
2. **预期**：返回到 Olivia 首页，可以重新开始通话

---

## 🔍 常见问题排查

### 问题 1: 前端无法启动

**错误**：`npm: 无法识别`

**解决**：
1. 检查 Node.js 是否安装：`node --version`
2. 如果未安装，下载安装 Node.js（推荐 v18+）
3. 重新运行 `npm install`

---

### 问题 2: 点击"开始通话"后无反应

**可能原因**：
1. Minerva 后端未启动
2. 环境变量配置错误
3. Agent ID 不正确

**排查步骤**：
```bash
# 1. 检查 Minerva 后端是否运行
curl http://localhost:8000/docs

# 2. 检查创建 Web Call API
curl -X POST http://localhost:8000/intake/create-web-call \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001"}'
```

**查看浏览器 Console**：
- 打开 F12 开发者工具
- 切换到 Console tab
- 查看是否有红色错误信息

---

### 问题 3: 通话后没有生成 Summary

**可能原因**：
1. 通话时间太短（<30秒）
2. OpenAI API Key 未配置
3. 后端处理失败

**排查步骤**：
```bash
# 查看 Minerva 后端日志（Terminal 2）
# 应该看到类似：
# ==== Generating call summary...
# ==== ✅ Generated call summary successfully
```

如果看到错误，检查 `minerva/.env` 中的 `OPENAI_API_KEY`。

---

### 问题 4: 麦克风权限被拒绝

**错误**：通话无法建立，Console 显示 "Permission denied"

**解决**：
1. 点击浏览器地址栏左侧的 🔒 或 🛈 图标
2. 找到"麦克风"权限
3. 选择"允许"
4. 刷新页面重试

---

### 问题 5: Retell 连接失败

**错误**：Console 显示 "Failed to create web call"

**可能原因**：
1. Retell API Key 未配置
2. Agent ID 或 LLM ID 错误
3. Retell 账户问题

**检查**：
```bash
# 查看 minerva/.env
cat minerva/.env | grep RETELL_API_KEY
```

---

## 📊 完整测试检查清单

- [ ] ✅ 安装前端依赖成功
- [ ] ✅ 创建前端 .env.local 文件
- [ ] ✅ 配置后端 .env 文件
- [ ] ✅ CGM Butler Dashboard 启动成功（端口 5000）
- [ ] ✅ Minerva 后端启动成功（端口 8000）
- [ ] ✅ 前端启动成功（端口 5173）
- [ ] ✅ 访问首页看到 Olivia 界面
- [ ] ✅ 点击 Voice Chat 进入语音界面
- [ ] ✅ 点击"开始通话"成功连接
- [ ] ✅ 麦克风权限允许
- [ ] ✅ 对话过程中 Transcript 实时显示
- [ ] ✅ 静音/取消静音功能正常
- [ ] ✅ 结束通话后自动跳转到结果页
- [ ] ✅ Summary Tab 显示对话摘要
- [ ] ✅ Goals Achievement Tab 显示目标分析
- [ ] ✅ 返回按钮正常工作

---

## 🎯 测试成功标准

**最低标准**（必须全部通过）：
1. ✅ 能够成功启动通话
2. ✅ 实时 Transcript 正常显示
3. ✅ 能够正常结束通话
4. ✅ 结果页面至少显示一个 Tab 的内容

**完整标准**（理想状态）：
1. ✅ 通话流畅，无明显延迟
2. ✅ Transcript 准确完整
3. ✅ Summary 包含对话的主要内容
4. ✅ Goals Analysis 有实质性分析
5. ✅ UI 美观，无明显 bug

---

## 📞 需要帮助？

如果遇到无法解决的问题，请提供：
1. **错误截图**（浏览器 Console + 页面）
2. **后端日志**（Terminal 1 和 Terminal 2 的输出）
3. **环境变量配置**（隐藏敏感信息）

祝测试顺利！🎉

