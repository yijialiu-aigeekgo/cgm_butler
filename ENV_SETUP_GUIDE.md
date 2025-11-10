# 🔧 环境变量配置指南

本指南帮助你正确配置 CGM Butler 语音对话功能所需的环境变量。

---

## 📁 配置文件位置

语音对话功能需要在 **`minerva/.env`** 中配置环境变量。

```
cgm-butler/
└── minerva/
    └── .env          ← 在这里创建配置文件
```

---

## 🚀 快速配置（复制粘贴）

### 步骤 1: 创建 .env 文件

在 `minerva/` 目录下创建一个名为 `.env` 的文件（注意：文件名以点开头）

**Windows PowerShell:**
```powershell
cd minerva
New-Item -Path ".env" -ItemType File
```

**或手动创建**:
1. 打开 `minerva` 文件夹
2. 右键 → 新建 → 文本文档
3. 重命名为 `.env`（删除 .txt 扩展名）

---

### 步骤 2: 填入配置内容

复制以下内容到 `minerva/.env` 文件中：

```bash
# ============================================
# 🔴 必需配置 - 请替换为你的真实 API Keys
# ============================================

# Retell API Configuration
RETELL_API_KEY=your_retell_api_key_here
INTAKE_AGENT_ID=agent_c7d1cb2c279ec45bce38c95067
INTAKE_LLM_ID=llm_e54c307ce74090cdfd06f682523b

# OpenAI API Configuration  
OPENAI_API_KEY=your_openai_api_key_here

# ============================================
# ✅ 默认配置 - 通常无需修改
# ============================================

# CGM Butler Backend URL
CGM_BACKEND_URL=http://localhost:5000

# Database Configuration
MYSQL_DATABASE_URL=sqlite+aiosqlite:///./minerva_dev.db
SOP_MYSQL_DATABASE_URL=sqlite+aiosqlite:///./sop_dev.db

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

### 步骤 3: 替换 API Keys

**🔴 必须替换的内容：**

#### 1. Retell API Key
将 `your_retell_api_key_here` 替换为你的真实 Retell API Key。

**如何获取：**
1. 访问 [Retell Dashboard](https://dashboard.retellai.com/)
2. 登录你的账号
3. 进入 **Settings** → **API Keys**
4. 复制 API Key（格式：`key_xxxxxxxxxxxxx`）

**示例：**
```bash
RETELL_API_KEY=key_e3b74c0de01a1ba9c20228131da1  # 你的真实 key
```

#### 2. OpenAI API Key
将 `your_openai_api_key_here` 替换为你的真实 OpenAI API Key。

**如何获取：**
1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 登录你的账号
3. 点击 **"Create new secret key"**
4. 复制生成的 key（格式：`sk-proj-...`）

**示例：**
```bash
OPENAI_API_KEY=sk-proj-abcdefghijklmnopqrstuvwxyz123456789  # 你的真实 key
```

---

## ✅ 配置完成检查

配置完成后，你的 `minerva/.env` 文件应该类似于：

```bash
# Retell API Configuration
RETELL_API_KEY=key_e3b74c0de01a1ba9c20228131da1
INTAKE_AGENT_ID=agent_c7d1cb2c279ec45bce38c95067
INTAKE_LLM_ID=llm_e54c307ce74090cdfd06f682523b

# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-XYZ123456789abcdefghijklmnopqrstuvwxyz

# CGM Butler Backend URL
CGM_BACKEND_URL=http://localhost:5000

# Database Configuration
MYSQL_DATABASE_URL=sqlite+aiosqlite:///./minerva_dev.db
SOP_MYSQL_DATABASE_URL=sqlite+aiosqlite:///./sop_dev.db

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 🧪 验证配置

运行以下命令检查配置是否正确：

```powershell
cd minerva
Get-Content .env | Select-String "RETELL_API_KEY"
Get-Content .env | Select-String "OPENAI_API_KEY"
```

**期望输出：**
```
RETELL_API_KEY=key_xxxxxxxxxxxxx
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

如果看到上述输出（而不是 `your_xxx_here`），说明配置成功！

---

## 🔒 安全提示

### ⚠️ 重要：保护你的 API Keys

1. **永远不要** 将 `.env` 文件提交到 Git 仓库
2. **永远不要** 在公开场合分享 API Keys
3. **永远不要** 将 API Keys 硬编码到代码中
4. `.env` 文件已自动被 `.gitignore` 忽略

### 🔐 API Key 泄露怎么办？

如果不小心泄露了 API Key：

**Retell:**
1. 登录 [Retell Dashboard](https://dashboard.retellai.com/)
2. 进入 Settings → API Keys
3. **撤销 (Revoke)** 旧的 key
4. 生成新的 key

**OpenAI:**
1. 登录 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 找到泄露的 key
3. 点击 **"Revoke"** 按钮
4. 生成新的 key

---

## 🐛 常见问题

### ❌ 问题 1: "Environment variable not set"

**原因**: `.env` 文件不存在或格式错误

**解决方案**:
1. 确认 `.env` 文件在 `minerva/` 目录下
2. 确认文件名是 `.env` 而不是 `.env.txt`
3. 确认文件内容没有多余的空格或引号

### ❌ 问题 2: "Invalid API Key"

**原因**: API Key 格式错误或已过期

**解决方案**:
1. 重新从官方平台复制 API Key
2. 确认 key 前后没有多余的空格
3. 确认 key 没有被撤销

### ❌ 问题 3: Windows 无法创建 .env 文件

**原因**: Windows 资源管理器不允许创建以点开头的文件名

**解决方案**:
```powershell
# 使用 PowerShell 创建
cd minerva
New-Item -Path ".env" -ItemType File

# 或使用命令行
echo. > .env
```

---

## 📚 相关文档

- [快速开始指南](./QUICK_START_VOICE_CHAT.md)
- [完整 README](./README.md)
- [测试指南](./TEST_GUIDE.md)

---

## ✅ 下一步

配置完成后，继续：

1. 📖 阅读 [QUICK_START_VOICE_CHAT.md](./QUICK_START_VOICE_CHAT.md)
2. 🚀 运行 `.\start_services.ps1` 启动服务
3. 🎤 访问 http://localhost:5173 开始语音对话

---

**祝你配置顺利！🎉**

