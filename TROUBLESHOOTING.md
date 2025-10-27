# 🔧 CGM Butler 故障排除指南

## 🔴 常见错误和解决方案

### 1. "Tavus API key is required" 错误

**错误信息**:
```
ValueError: Tavus API key is required. Set TAVUS_API_KEY environment variable or pass api_key parameter.
```

**原因**: Tavus API Key 未设置（这是可选的，系统会自动降级）

**解决方案**:
```bash
# 这是正常的警告 - 系统会继续运行
# 文本聊天 (GPT-4o) 将完全正常工作
# 视频头像功能将不可用

# 如果你想启用视频头像，设置 API Key:
# Windows PowerShell
$env:TAVUS_API_KEY = "your-api-key"
$env:TAVUS_PERSONA_ID = "your-persona-id"

# 然后重新启动服务
```

**状态**: ✅ 不是问题，系统设计可以不用 API Key 运行

---

### 2. "Failed to fetch /api/users" 错误

**症状**: 浏览器控制台显示 404 或连接错误

**原因**: Flask 服务器未运行或端口被占用

**解决方案**:
```bash
# 确保服务器正在运行
cd dashboard
python app.py

# 应该看到:
# WARNING in app.run...
# Running on http://127.0.0.1:5000
```

**验证**:
```bash
# 在另一个终端测试
curl http://localhost:5000/api/users
```

---

### 3. "No glucose readings found" 错误

**症状**: 聊天时显示没有数据

**原因**: 数据库未初始化或用户选择错误

**解决方案**:
```bash
# 初始化数据库
python database/setup_database.py

# 应该看到:
# ✅ 数据库已创建
# ✅ 添加了 11 个测试用户
# ✅ 添加了 CGM 读数数据
# ✅ 添加了 CGM 模式行动数据
```

---

### 4. 端口已被占用 (Port 5000 in use)

**错误信息**:
```
OSError: [Errno 48] Address already in use
```

**原因**: 端口 5000 已被其他应用程序使用

**解决方案**:

**Windows**:
```bash
# 查找占用端口的进程
netstat -ano | findstr :5000

# 杀死进程 (例如 PID 是 1234)
taskkill /PID 1234 /F

# 或改用另一个端口
cd dashboard
python -c "import app; app.app.run(port=5001)"
```

**Linux/macOS**:
```bash
# 查找进程
lsof -i :5000

# 杀死进程
kill -9 <PID>
```

---

### 5. Python 模块导入错误

**错误**: `ModuleNotFoundError: No module named 'flask'`

**原因**: 依赖未安装

**解决方案**:
```bash
# 在项目根目录运行
pip install -r requirements.txt

# 验证安装
python -c "import flask; print(flask.__version__)"
```

---

### 6. npm 依赖错误 (用于视频头像)

**错误**: `Cannot find module '@tavus/cvi-ui'`

**原因**: Node 依赖未安装

**解决方案**:
```bash
cd cgm-avatar-app
npm install
npm run dev
```

---

### 7. 数据库文件损坏

**症状**: 各种 SQL 错误，无法查询数据

**原因**: `cgm_butler.db` 文件损坏

**解决方案**:
```bash
# 删除旧数据库
rm cgm_butler.db

# 重新初始化
python database/setup_database.py
```

---

### 8. CORS 错误 (跨域请求被阻止)

**错误**:
```
Access to XMLHttpRequest at 'http://localhost:5000/api/users' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**原因**: 浏览器安全限制

**解决方案**: 已自动配置，无需操作。如果仍然出现：
```python
# 在 dashboard/app.py 中检查
from flask_cors import CORS
CORS(app)  # 应该已经添加
```

---

### 9. OpenAI API 错误

**错误**: `AuthenticationError` 或 `RateLimitError`

**原因**: 
- API Key 无效
- 已超额用尽配额
- 网络问题

**解决方案**:
```bash
# 验证 API Key
echo %OPENAI_API_KEY%  # Windows

# 检查 OpenAI 账户
# https://platform.openai.com/account/usage/overview

# 使用新的 API Key
set OPENAI_API_KEY=sk-new-key
```

---

### 10. React 开发服务器无法启动

**错误**: `Port 5173 already in use`

**原因**: Vite 开发服务器端口被占用

**解决方案**:
```bash
cd cgm-avatar-app

# 使用不同的端口
npm run dev -- --port 5174
```

---

## 📋 系统检查清单

在遇到问题前，先检查以下内容：

### ✅ 前置条件检查
```bash
# Python 版本
python --version  # 应该是 3.7+

# pip 版本
pip --version

# Node.js 版本 (用于视频)
node --version  # 应该是 14+

# npm 版本
npm --version
```

### ✅ 依赖检查
```bash
# Python 依赖
pip list | grep flask
pip list | grep openai

# Node 依赖 (如果用视频)
cd cgm-avatar-app
npm list
```

### ✅ 数据库检查
```bash
# 检查数据库文件
ls -la cgm_butler.db  # Linux/macOS
dir cgm_butler.db  # Windows

# 检查数据库完整性
python database/cgm_database.py
```

### ✅ 网络检查
```bash
# 测试 API 服务器
curl http://localhost:5000/api/users

# 测试 OpenAI 连接 (需要 API Key)
python -c "from openai import OpenAI; print('✅ OpenAI OK')"
```

---

## 🐛 调试模式

### 启用详细日志
```bash
# Flask 详细模式
cd dashboard
FLASK_ENV=development FLASK_DEBUG=1 python app.py
```

### 检查浏览器控制台
1. 打开浏览器 (Chrome/Firefox/Edge)
2. 按 F12 打开开发者工具
3. 选择 "Console" 标签
4. 查看任何 JavaScript 错误

### 检查网络请求
1. 打开开发者工具
2. 选择 "Network" 标签
3. 刷新页面
4. 查看 API 请求
   - 状态码 200 = 成功
   - 状态码 404 = 未找到
   - 状态码 500 = 服务器错误

### 收集日志信息
```bash
# 保存 Flask 输出到文件
cd dashboard
python app.py > flask.log 2>&1

# 查看日志
tail -f flask.log  # Linux/macOS
type flask.log  # Windows
```

---

## 🆘 获取帮助

### 问题排查步骤
1. **检查日志** - 查看错误消息
2. **尝试重启** - 关闭所有服务，重新启动
3. **检查依赖** - 确保所有库都已安装
4. **重新初始化** - 重新运行 `setup_database.py`
5. **清除缓存** - 删除 `__pycache__` 目录

### 报告问题
提交 GitHub Issue 时请包括：
- 错误信息的完整堆栈跟踪
- 你的 Python 版本
- 你的操作系统
- 重现问题的步骤
- 已尝试的解决方案

### 常用命令参考
```bash
# 清除 Python 缓存
find . -type d -name __pycache__ -exec rm -r {} +  # Linux/macOS
for /d /r . %d in (__pycache__) do @if exist "%d" rm /s /q "%d"  # Windows

# 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 检查端口占用
netstat -tulpn | grep 5000  # Linux
netstat -ano | findstr :5000  # Windows

# 清除数据库
rm cgm_butler.db database/cgm_butler.db
python database/setup_database.py
```

---

## ✨ 优化建议

### 性能优化
- 使用 `python -m venv` 创建虚拟环境
- 定期清理 `__pycache__` 目录
- 使用 SQLite 查询优化 (已配置索引)

### 开发体验
- 使用 IDE 的集成终端
- 启用 IDE 的 Python Linter
- 使用 Git 进行版本控制

### 部署前检查
- 移除 API Keys (改用环境变量)
- 设置适当的数据库权限
- 配置 HTTPS
- 添加身份认证

---

**版本**: v2.0.0  
**最后更新**: 2025-10-27  
**状态**: ✅ 可直接使用
