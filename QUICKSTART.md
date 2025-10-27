# 🚀 CGM Butler 快速开始指南

本指南帮助你快速启动和使用 CGM Butler 系统。

## 📋 前置条件

- Python 3.7+
- Node.js 14+ (用于视频头像)
- pip 包管理器
- npm 包管理器

## ⚙️ 安装步骤

### 1️⃣ 克隆仓库
```bash
git clone https://github.com/yijialiu-aigeekgo/cgm_butler.git
cd cgm_butler
```

### 2️⃣ 安装 Python 依赖
```bash
pip install -r requirements.txt
```

### 3️⃣ 安装 Node.js 依赖 (可选，仅用于视频头像)
```bash
cd cgm-avatar-app
npm install
cd ..
```

### 4️⃣ 初始化数据库
```bash
python database/setup_database.py
```

你应该看到类似的输出：
```
✅ 数据库已创建
✅ 添加了 11 个测试用户
✅ 添加了 CGM 读数数据
✅ 添加了 CGM 模式行动数据
```

## 🎯 三种使用方式

### 方式 A: 文本聊天 (⭐ 推荐)
**最简单，无需额外配置。**

```bash
cd dashboard
python app.py
```

然后打开浏览器访问：
- 📊 **仪表板**: http://localhost:5000
- 💬 **聊天**: http://localhost:5000/chat

### 方式 B: Web 仪表板
**查看血糖数据和分析。**

```bash
cd dashboard
python app.py
```

打开 http://localhost:5000 查看：
- 📈 实时血糖数据
- 📊 血糖统计信息
- 🔍 检测到的血糖模式
- 💡 个性化健康建议

### 方式 C: 视频头像 (需要 API Key)
**需要配置 Tavus 和 OpenAI API Keys。**

首先设置环境变量：
```bash
# Windows PowerShell
$env:TAVUS_API_KEY = "your-tavus-api-key"
$env:TAVUS_PERSONA_ID = "your-persona-id"
$env:OPENAI_API_KEY = "your-openai-api-key"

# 或 Windows CMD
set TAVUS_API_KEY=your-tavus-api-key
set TAVUS_PERSONA_ID=your-persona-id
set OPENAI_API_KEY=your-openai-api-key
```

然后启动两个服务：
```bash
# 终端 1: Flask 后端
cd dashboard
python app.py

# 终端 2: React 前端
cd cgm-avatar-app
npm run dev
```

打开 http://localhost:5173 使用视频头像。

## 🔑 API Key 配置

### 选项 1: 环境变量 (推荐)
```bash
# Linux/macOS
export OPENAI_API_KEY="sk-..."
export TAVUS_API_KEY="api_key_..."
export TAVUS_PERSONA_ID="p_id_..."

# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."
$env:TAVUS_API_KEY="api_key_..."
$env:TAVUS_PERSONA_ID="p_id_..."
```

### 选项 2: .env 文件
在项目根目录创建 `.env` 文件：
```
OPENAI_API_KEY=sk-...
TAVUS_API_KEY=api_key_...
TAVUS_PERSONA_ID=p_id_...
```

### 选项 3: 系统环境变量
通过系统设置永久设置环境变量。

## 🧪 验证安装

### 检查数据库
```bash
python database/cgm_database.py
```

### 测试 API
```bash
# 获取用户列表
curl http://localhost:5000/api/users

# 获取特定用户的数据
curl http://localhost:5000/api/user/user_001

# 获取血糖统计
curl http://localhost:5000/api/stats/user_001
```

### 测试聊天
打开 http://localhost:5000/chat 并：
1. 从下拉菜单选择用户
2. 输入问题，例如：
   - "What's my current glucose level?"
   - "Analyze my glucose patterns"
   - "What actions should I take?"

## 📊 测试数据

系统预装了测试数据：
- **11 个用户** - 名字、邮箱、健康条件等
- **CGM 读数** - 7 天的模拟血糖数据 (2000+ 条记录)
- **健康建议** - 50+ 条根据血糖模式的建议

用户列表：
- `user_001` - John Chen (糖尿病患者)
- `user_002` - Alice Smith (正常)
- `user_003` - Bob Wilson (代谢综合征)
- ... 以及更多

## 🎨 UI 特点

### 仪表板
- 🔄 每 5 秒自动刷新
- 📱 响应式设计 (支持手机/平板/PC)
- 🎨 蓝白现代风格
- 👥 多用户支持

### 聊天
- 🤖 GPT-4o 驱动
- 💬 自然对话
- 🔍 自动查询血糖数据
- 📝 完整对话历史

### 视频头像 (需要 API Key)
- 🎬 AI 生成的视频
- 🎤 语音交互
- 💡 上下文感知回应

## ❌ 常见问题

### Q: "Tavus API key is required"
**A:** 这个警告是正常的。系统会自动降级到 GPT 文本聊天。如果你想用视频头像，请:
1. 获取 Tavus API Key
2. 设置环境变量: `set TAVUS_API_KEY=your-key`
3. 重新启动服务

### Q: "Failed to fetch /api/users"
**A:** 确保 Flask 服务器正在运行:
```bash
cd dashboard
python app.py
```

### Q: 聊天说 "No glucose readings found"
**A:** 检查数据库是否初始化:
```bash
python database/setup_database.py
```

### Q: 视频头像不工作
**A:** 检查 API 密钥:
```bash
# 验证环境变量
echo %TAVUS_API_KEY%  # Windows
echo $env:TAVUS_API_KEY  # PowerShell
```

### Q: 如何添加更多用户？
**A:** 编辑 `database/setup_database.py` 中的用户列表并重新运行:
```bash
python database/setup_database.py
```

## 📚 更多资源

- 📖 [完整文档](README.md)
- 💬 [对话历史指南](CONVERSATION_HISTORY_GUIDE.md)
- 🔧 [集成完成报告](INTEGRATION_COMPLETE.md)
- 🐛 [GitHub Issues](https://github.com/yijialiu-aigeekgo/cgm_butler/issues)

## 🚀 下一步

1. **探索仪表板** - 查看血糖数据和分析
2. **尝试聊天** - 与 Olivia 交互
3. **获取 API Keys** - 解锁视频头像功能
4. **自定义** - 添加你的用户和数据

## 📞 需要帮助？

- 查看 [README.md](README.md) 了解系统架构
- 检查日志输出查找错误信息
- 在 GitHub 提出 Issue

---

**版本**: v2.0.0  
**最后更新**: 2025-10-27  
**状态**: ✅ 可直接使用
