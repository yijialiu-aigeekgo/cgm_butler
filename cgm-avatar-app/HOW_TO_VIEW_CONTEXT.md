# 如何查看传给数字人的完整 Context

## 🎯 快速开始

### 步骤 1: 启动所有服务
```bash
# 在项目根目录，启动完整系统
start_video_avatar.bat
```

这会自动启动：
- ✅ Flask API 后端 (http://localhost:5000)
- ✅ React Vite 应用 (http://localhost:5173)

### 步骤 2: 打开浏览器开发者工具
在 `http://localhost:5173/` 页面，按下 **F12** 打开浏览器开发者工具

### 步骤 3: 进入 Console 标签
点击上方的 **Console** 标签

---

## 📊 查看 Context 信息

### 完整的 Conversational Context

1. **打开 Console** (F12)

2. **查找日志信息**，你会看到：

```
📍 Initializing for user: user_001
Creating conversation with context: 
╔════════════════════════════════════════════════════════════════╗
║                    USER PROFILE & HEALTH CONTEXT               ║
╚════════════════════════════════════════════════════════════════╝

👤 PERSONAL INFORMATION:
- Name: John Doe
- User ID: user_001
- Health Goal: Keep stable glucose levels and reduce medication usage
- Conditions: Type 2 Diabetes
- CGM Device: Freestyle Libre

[... 完整的 context 信息 ...]
```

### 包含的信息

Context 包含以下 **8 个主要部分**：

| # | 部分 | 内容 |
|---|------|------|
| 1 | 👤 个人信息 | 名字、ID、健康目标、医疗状况、CGM设备 |
| 2 | 📊 当前状态 | 当前血糖值、状态、诊断 |
| 3 | 📈 24小时统计 | 平均、最小、最大、TIR、读数次数 |
| 4 | 📈 7天统计 | 7天平均、7天TIR |
| 5 | 🔍 检测模式 | 模式名称、严重程度、置信度、描述 |
| 6 | 📋 最近读数 | 最近20条读数（显示最多10条）|
| 7 | 💡 健康建议 | 前5条高优先级建议 |
| 8 | 📌 对话指示 | 指导 Olivia 的8条行为指示 |

---

## 🔍 复制完整 Context

1. **在 Console 中右键点击** Context 输出部分
2. **选择 "Copy"**
3. **粘贴到文本编辑器** 查看完整内容

或者，点击 Console 中的日志信息查看展开的详情。

---

## 📊 示例输出

### 当前状态信息
```
📍 Initializing for user: user_001
```

### Context 格式化示例
```
╔════════════════════════════════════════════════════════════════╗
║                    USER PROFILE & HEALTH CONTEXT               ║
╚════════════════════════════════════════════════════════════════╝

👤 PERSONAL INFORMATION:
- Name: John Doe
- User ID: user_001
- Health Goal: Keep stable glucose levels and reduce medication usage
- Conditions: Type 2 Diabetes
- CGM Device: Freestyle Libre

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 CURRENT CGM STATUS:
- Current Glucose: 114 mg/dL (Normal) 🩺
- Status: ✅ In range

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 GLUCOSE STATISTICS:

24-Hour Metrics:
- Average: 118.4 mg/dL
- Min-Max: 82 - 156 mg/dL
- Time In Range (70-140): 74.7%
- Reading Count: 48

7-Day Metrics:
- Average: 120.2 mg/dL
- Time In Range (70-140): 72.1%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 DETECTED GLUCOSE PATTERNS (Last 24h):
- post_meal_spike (high, 85% confidence): Glucose spikes after meals...
- dawn_phenomenon (medium, 72% confidence): Elevated glucose in early morning...
- post_exercise_drop (low, 58% confidence): Gradual glucose decrease...

[... 更多内容 ...]
```

### 成功消息
```
✅ Conversation created successfully
Conversation URL: https://tavus.daily.co/c82c04a87c867440
```

---

## 🧪 测试不同用户

### 切换用户查看不同的 Context

1. **在 Console 运行**:
```javascript
// 设置不同用户
localStorage.setItem('currentUserId', 'user_002');

// 刷新页面
window.location.reload();
```

2. **观察 Console 输出**，你会看到：
```
📍 Initializing for user: user_002
Creating conversation with context: 
[user_002 的完整 context 信息]
```

---

## ⚠️ 调试技巧

### 如果看不到 Context 信息

1. **确保 Flask 服务运行**:
```bash
# 在另一个终端检查
curl http://localhost:5000/api/users
```

2. **清除浏览器缓存**:
- Ctrl + Shift + Delete
- 选择"所有时间"和"清除"

3. **重新刷新页面**:
- Ctrl + Shift + R (强制刷新)

### 如果看到 API 错误

1. **检查 Console 中的错误消息**
2. **验证 Flask 后端是否运行**
3. **确认数据库中有数据**: `python database/check_database.py`

---

## 📊 Context 包含的数据来源

```
数据来源 → API 端点 → Context 字段
├─ 用户表 → /api/user/{userId} → 个人信息
├─ 最新读数 → /api/glucose/{userId} → 当前血糖
├─ 统计表 → /api/stats/{userId} → 24小时统计
├─ 统计表 → /api/stats/{userId}?days=7 → 7天统计
├─ 读数表 → /api/recent/{userId}/20 → 最近读数
├─ 模式表 → /api/patterns/{userId} → 检测模式
└─ 建议表 → /api/actions → 健康建议
```

---

## 🎯 Context 对数字人的影响

### Olivia 会根据 Context 中的数据：

1. ✅ **个性化问候**
   - "Hi John! I see your glucose is at 114 mg/dL..."

2. ✅ **参考具体数据**
   - "Your Time In Range is 74.7%..."

3. ✅ **解释模式**
   - "I've detected a post-meal spike pattern with 85% confidence..."

4. ✅ **提出建议**
   - "Based on your patterns, I'd recommend..."

---

## 📚 更多信息

- 详细说明: `cgm-avatar-app/TAVUS_CONTEXT_EXPANDED.md`
- 对比文档: `TAVUS_CONTEXT_ENHANCEMENT_SUMMARY.md`
- 源代码: `cgm-avatar-app/src/App.tsx`

---

## 🚀 总结

通过查看 Browser Console，你可以：
✅ 看到传给 Tavus 数字人的完整 context 信息
✅ 验证所有 CGM 数据都被正确获取
✅ 理解数字人的对话背景
✅ 调试任何数据问题

