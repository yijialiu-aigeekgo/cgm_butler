# 快速参考卡：cgm-avatar-app vs digital_avatar 🎯

## 一眼看懂

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  cgm-avatar-app 🎥                 digital_avatar 💬           │
│  ═══════════════════════════════════════════════════════════   │
│                                                                  │
│  高端视频数字人                    实用文本聊天                  │
│  React + Tavus CVI                 Flask + GPT-4o              │
│  http://localhost:5173/            http://localhost:5000/chat  │
│                                                                  │
│  ✅ 实时视频                       ✅ 文本消息                   │
│  ✅ 语音识别/合成                  ✅ 函数调用                   │
│  ✅ 非常专业                       ✅ 对话历史                   │
│  ❌ 无函数调用                     ❌ 无视频                     │
│  ❌ 无对话历史                     ❌ 无语音                     │
│                                                                  │
│  场景: 演示/投资/品牌              场景: 日常使用/开发          │
│  成本: Tavus 额度                  成本: GPT token              │
│  用户体验: 💎 豪华                 用户体验: ⚡ 高效            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 快速对比表

| 特性 | cgm-avatar-app | digital_avatar |
|------|---|---|
| 🎬 **界面** | 🎥 视频 | 💬 文本 |
| 🛠️ **技术** | React | Python |
| 🤖 **AI** | Tavus | GPT-4o |
| 📊 **数据方式** | 预加载 Context | 动态函数调用 |
| 🎤 **音频** | ✅ | ❌ |
| 📝 **聊天历史** | ❌ | ✅ |
| 🔧 **功能调用** | ❌ | ✅ |
| 💰 **成本** | Tavus 额度 | GPT token |
| ⚡ **实用性** | 演示用 | 日常用 |

---

## 启动方式

### cgm-avatar-app (视频)
```bash
start_video_avatar.bat
# 或
cd dashboard && python app.py &
cd cgm-avatar-app && npm run dev

# 访问: http://localhost:5173/
```

### digital_avatar (文本)
```bash
start_chat.bat
# 或
cd dashboard && python app.py

# 访问: http://localhost:5000/chat
```

### 同时运行
```bash
# 终端 1
cd dashboard && python app.py

# 终端 2
cd cgm-avatar-app && npm run dev

# 终端 3 (可选)
# 访问 http://localhost:5000/chat
```

---

## 核心文件

### cgm-avatar-app
- 📍 `cgm-avatar-app/src/App.tsx` - 主逻辑
- 📍 `cgm-avatar-app/package.json` - React 依赖
- 📍 `cgm-avatar-app/.env` - Tavus API Key

### digital_avatar
- 📍 `digital_avatar/gpt_chat.py` - GPT 管理
- 📍 `digital_avatar/chat.html` - 前端界面
- 📍 `digital_avatar/api.py` - Flask 路由
- 📍 `digital_avatar/config.py` - OpenAI Key

---

## 数据流对比

### cgm-avatar-app 📊
```
启动 → 获取数据 (7 个 API)
    ↓
构建 Context (~2300 字)
    ↓
发送给 Tavus
    ↓
Tavus 返回视频 URL
    ↓
🎥 对话开始
```

### digital_avatar 📊
```
用户输入问题
    ↓
发送给 GPT-4o
    ↓
GPT 选择函数调用
    ↓
调用 CGM 函数 (实时查询)
    ↓
GPT 组织回复
    ↓
💬 显示消息
```

---

## 何时使用哪个?

### 使用 cgm-avatar-app 🎬
- [ ] 需要演示给投资者
- [ ] 需要视频/语音交互
- [ ] 想要豪华用户体验
- [ ] 用于品牌宣传
- [ ] 医学会议演讲

### 使用 digital_avatar 💻
- [ ] 日常 CGM 管理
- [ ] 医疗查询/咨询
- [ ] 需要对话历史
- [ ] 成本敏感
- [ ] 需要动态数据查询
- [ ] 开发/测试

---

## 常见问题

**Q: 两个都需要 Flask 后端吗?**
A: 是的，两个都需要 `dashboard/app.py` 提供数据 API

**Q: 可以同时运行吗?**
A: 完全可以！在不同终端启动

**Q: 数据库是共享的吗?**
A: 是的，都访问同一个 `database/cgm_butler.db`

**Q: 哪个成本更低?**
A: digital_avatar (GPT token) 通常比 Tavus 便宜

**Q: 能在生产环境用吗?**
A: 两个都可以，但需要相应的服务账户和成本预算

---

## 功能对标

| 功能 | cgm-avatar-app | digital_avatar |
|------|---|---|
| 查询血糖 | ✅ | ✅ |
| 获取统计 | ✅ | ✅ |
| 查看模式 | ✅ | ✅ |
| 健康建议 | ✅ | ✅ |
| 多用户 | ✅ | ✅ |
| 个性化 | ✅ | ✅ |
| **视频** | ✅ | ❌ |
| **语音** | ✅ | ❌ |
| **对话历史** | ❌ | ✅ |
| **函数调用可见** | ❌ | ✅ |

---

## 技术架构简图

```
数据库 (SQLite)
    ↑
    │ 数据 API
    │
Flask (dashboard/app.py)
    ├─→ cgm-avatar-app (React)
    │   └─→ Tavus API
    │       └─→ 🎥 Video Avatar
    │
    └─→ digital_avatar (Python)
        ├─→ gpt_chat.py (GPT-4o)
        ├─→ chat.html (前端)
        └─→ 💬 Chat Interface
```

---

## 成本参考

### cgm-avatar-app
- Tavus 按对话额度计费
- 一般 ~ $0.1-1 per conversation
- 取决于对话长度和 Tavus 套餐

### digital_avatar
- GPT-4o 按 token 计费
- 一般 ~ $0.01-0.1 per conversation
- 取决于对话长度和模型

---

## 环境配置

### cgm-avatar-app (.env)
```
VITE_TAVUS_API_KEY=your_key
VITE_REPLICA_ID=your_replica
VITE_PERSONA_ID=your_persona
VITE_BACKEND_URL=http://localhost:5000
```

### digital_avatar (config.py)
```python
TAVUS_API_KEY = "..."
TAVUS_PERSONA_ID = "..."
OPENAI_API_KEY = "sk-..."
```

---

## 故障排除

### cgm-avatar-app 不显示视频?
- [ ] 检查 Tavus API Key 是否有效
- [ ] 检查账户是否有对话额度 (402 Payment Required = 无额度)
- [ ] 确认 Flask 后端在运行

### digital_avatar 不回应?
- [ ] 检查 OpenAI API Key 是否有效
- [ ] 检查 Flask 后端在运行
- [ ] 查看 Console 中的错误信息

---

**总结**: 
- 🎥 **cgm-avatar-app** = 豪华体验
- 💬 **digital_avatar** = 实用高效
- 🚀 **都很优秀，选择你需要的!**

