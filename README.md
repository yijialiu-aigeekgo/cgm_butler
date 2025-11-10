# CGM Butler - 智能血糖管理助手

通过 AI 驱动的对话和实时数据分析,为用户提供个性化的血糖管理支持和健康建议。

## 🎯 项目概述

### 核心功能
- 🩺 **CGM 数据管理** - 存储和分析连续血糖监测数据
- 🤖 **AI 聊天助手** (Olivia) - GPT-4o 驱动的智能对话
- 🎙️ **语音对话** (NEW!) - Retell Web Call 实时语音对话，自动生成摘要和目标分析
- 🎬 **数字人视频** - Tavus AI 创建的视频对话互动
- 📊 **Web 仪表板** - 实时数据可视化和分析
- 🔍 **模式识别** - 自动检测血糖模式(共10种)
- 💾 **对话历史** - 保存所有对话记录用于分析

### 核心模块
```
cgm-butler/
├── database/                  # 数据库模块
│   ├── cgm_database.py       # 数据库操作类
│   ├── cgm_butler.db         # SQLite 数据库
│   ├── conversation_manager.py # 对话历史管理
│   ├── migration_add_conversations.py # 数据库迁移
│   └── setup_database.py     # 初始化脚本
│
├── dashboard/                # Flask Web 仪表板
│   ├── app.py               # Flask 应用
│   └── templates/index.html # 前端界面
│
├── digital_avatar/          # AI 聊天模块
│   ├── gpt_chat.py          # GPT-4o 聊天管理
│   ├── api.py               # REST API 端点
│   ├── chat.html            # 聊天界面
│   ├── cgm_tools.py         # CGM 工具函数
│   ├── config.py            # 配置管理
│   └── tavus_client.py      # Tavus API 客户端
│
├── pattern_identification/  # 模式识别模块
│   ├── identifier.py        # 10 种 CGM 模式识别
│   └── scheduler.py         # 定时任务调度
│
├── cgm-avatar-app/          # React 前端应用
│   ├── src/App.tsx          # React 应用主组件
│   ├── src/pages/VoiceChat/ # 语音对话页面
│   ├── src/hooks/           # React Hooks (Retell SDK)
│   ├── package.json         # 依赖配置
│   └── vite.config.ts       # Vite 配置
│
├── minerva/                 # Retell 后端服务
│   ├── intake_phone_agent/  # 语音对话 Agent
│   ├── main.py              # FastAPI 应用
│   └── .env                 # 后端环境变量
│
├── start_services.ps1       # 🎙️ 启动所有服务（语音对话）
├── start_all_services.ps1   # 完整启动脚本
├── start_chat.bat           # 启动文本聊天
├── start_dashboard.bat      # 启动 Web 仪表板
├── start_video_avatar.bat   # 启动视频头像
├── requirements.txt         # Python 依赖
├── README.md                # 本文档
├── QUICK_START_VOICE_CHAT.md # 🎙️ 语音对话快速开始
└── INTEGRATION_COMPLETE.md  # 功能集成完成报告
```

## 🚀 快速开始

### 1. 环境配置
```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Node.js 依赖 (用于视频头像)
cd cgm-avatar-app
npm install
```

### 2. 初始化数据库
```bash
python database/setup_database.py
```

### 3. 启动服务

#### 方式 A: 🎙️ 语音对话（最新功能，推荐！）
```powershell
# 一键启动所有服务（CGM Butler + Minerva + 前端）
.\start_services.ps1

# 或使用完整脚本
.\start_all_services.ps1

# 访问: http://localhost:5173
# 点击 "Olivia" 标签 → "Voice Chat" 开始语音对话
```

📖 **详细指南**: [QUICK_START_VOICE_CHAT.md](./QUICK_START_VOICE_CHAT.md)

#### 方式 B: 文本聊天
```bash
start_chat.bat
# 或
cd dashboard && python app.py
# 然后访问: http://localhost:5000/chat
```

#### 方式 C: Web 仪表板
```bash
start_dashboard.bat
# 访问: http://localhost:5000
```

#### 方式 D: 视频头像
```bash
start_video_avatar.bat
# 启动: Flask (端口 5000) 和 React (端口 5173)
# 访问: http://localhost:5173
```

## 🔑 配置 API Keys

### 语音对话 (Retell + OpenAI)
在 `minerva/.env` 中配置：
```bash
# Retell API (必需)
RETELL_API_KEY=your_retell_api_key
INTAKE_AGENT_ID=agent_c7d1cb2c279ec45bce38c95067
INTAKE_LLM_ID=llm_e54c307ce74090cdfd06f682523b

# OpenAI API (必需)
OPENAI_API_KEY=your_openai_api_key

# CGM Butler 后端地址
CGM_BACKEND_URL=http://localhost:5000

# 数据库配置
MYSQL_DATABASE_URL=sqlite+aiosqlite:///./minerva_dev.db
SOP_MYSQL_DATABASE_URL=sqlite+aiosqlite:///./sop_dev.db

# CORS 配置
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 视频头像 (Tavus)
在根目录 `.env` 中配置：
```bash
TAVUS_API_KEY=your-tavus-api-key
TAVUS_PERSONA_ID=your-persona-id
OPENAI_API_KEY=your-openai-api-key
```

📝 **提示**: 详细配置指南请参考 [ENV_SETUP_GUIDE.md](./ENV_SETUP_GUIDE.md)

## 📊 功能详情

### Web 仪表板
- 📈 实时血糖数据可视化
- 📊 7 天血糖统计
- 🔍 血糖模式识别显示
- 💡 个性化健康建议
- 👥 多用户支持

### AI 聊天助手 (Olivia)
- 🤖 由 GPT-4o 驱动
- 💬 自然对话交互
- 🔍 自动查询 CGM 数据
- 📝 完整对话历史保存
- 🧠 个性化的健康顾问

### 🎙️ 语音对话 (Retell Web Call) - NEW!
- 🎤 **实时语音对话** - 使用 Retell Web SDK 进行自然语音交互
- 📝 **实时转录** - 对话过程中显示实时文字转录
- 📊 **自动摘要** - 通话结束后自动生成结构化摘要（饮食、运动、睡眠等）
- 🎯 **目标分析** - AI 分析用户行为与健康目标的匹配度
- ⚡ **零延迟** - 后台预生成分析，用户体验流畅
- 📱 **移动优先 UI** - 适配手机端的现代化界面设计

### 数字人视频 (Tavus)
- 🎬 AI 生成的视频对话
- 🎤 支持语音交互
- 💡 上下文感知回应
- 📹 专业视频质量

## 📝 对话历史

所有对话都自动保存到数据库:
```python
from database.conversation_manager import ConversationManager

manager = ConversationManager()
conversations = manager.get_user_conversations('user_001')
for conv in conversations:
    print(f"对话 ID: {conv['conversation_id']}")
    print(f"消息数: {len(conv['transcript'])}")
    print(f"时长: {conv['duration_seconds']}s")
```

## 🔍 CGM 模式识别 (10 种)

系统能识别以下血糖模式:

1. **Post-Meal Spike** - 餐后血糖飙升
2. **Dawn Phenomenon** - 黎明现象
3. **Nocturnal Hypoglycemia** - 夜间低血糖
4. **Afternoon Dip** - 下午血糖下降
5. **High Variability** - 高血糖波动
6. **Sustained Hyperglycemia** - 持续高血糖
7. **Frequent Hypoglycemia** - 频繁低血糖
8. **Post-Exercise Drop** - 运动后血糖下降
9. **Stress Hyperglycemia** - 压力引起的高血糖
10. **Roller Coaster** - 血糖大幅波动

每 4 小时自动检测一次,结果显示在仪表板上。

## 📚 文档

### 🎙️ 语音对话相关
- **[🚀 语音对话快速开始](QUICK_START_VOICE_CHAT.md)** - 5 分钟快速上手指南
- **[🔧 环境变量配置](ENV_SETUP_GUIDE.md)** - API Keys 配置详解
- **[📖 完整集成指南](RETELL_WEB_CALL_INTEGRATION_GUIDE.md)** - 技术实现细节
- **[🧪 测试指南](TEST_GUIDE.md)** - 功能测试说明

### 其他文档
- **[对话历史指南](CONVERSATION_HISTORY_GUIDE.md)** - 对话保存和分析
- **[集成完成报告](INTEGRATION_COMPLETE.md)** - 所有功能集成细节
- **[迁移方案](VOICE_CHAT_MIGRATION_PLAN.md)** - 语音功能迁移设计
- **[迁移进度](MIGRATION_PROGRESS.md)** - 实施进度追踪

## 🛠 技术栈

### 后端
- **Python 3.7+** - 核心编程语言
- **SQLite 3** - 数据库
- **Flask** - Web 框架
- **OpenAI GPT-4o** - AI 聊天
- **Tavus API** - 数字人视频

### 前端
- **HTML/CSS/JavaScript** - 仪表板
- **React + TypeScript** - 视频应用
- **Vite** - 构建工具
- **Chart.js** - 数据可视化

## 🔒 安全性

⚠️ **重要提示**:

1. **API Keys** - 永远不要硬编码敏感信息,使用环境变量
2. **数据隐私** - 遵守 HIPAA/GDPR 等医疗数据法规
3. **生产部署** - 添加用户认证和 HTTPS
4. **医疗免责** - 本项目仅供参考,不构成医疗建议

## 📞 联系方式

GitHub: [yijialiu-aigeekgo/cgm_butler](https://github.com/yijialiu-aigeekgo/cgm_butler)

## 📄 许可证

待定

---

**版本**: v2.0.0  
**最后更新**: 2025-10-27  
**状态**: ✅ 所有核心模块完成,可用于生产
