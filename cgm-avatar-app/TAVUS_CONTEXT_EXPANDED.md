# Tavus 数字人 - 完整 Context 信息结构

## 📊 概述

Tavus 数字人 (Olivia) 现在接收**丰富的、多维度的用户数据**，使其能够进行更个性化、更智能的对话。

---

## 📋 传递给数字人的完整数据结构

### 1️⃣ **个人信息** (Personal Information)
```
- 姓名 (Name)
- 用户 ID (User ID)
- 健康目标 (Health Goal) - 例如："Keep stable glucose levels"
- 健康状况 (Conditions) - 例如："Type 2 Diabetes"
- CGM 设备类型 (CGM Device Type) - 例如："Freestyle Libre"
```

### 2️⃣ **当前血糖状态** (Current CGM Status)
```
- 当前血糖值 (Current Glucose) - 例如：114 mg/dL
- 血糖状态 (Status) - Low / Normal / Elevated / High
- 人工诊断信息 - ✅ In range / ⚠️ Below target / ⚡ Slightly elevated
```

### 3️⃣ **24 小时统计** (24-Hour Metrics)
```
- 平均血糖 (Average Glucose) - 例如：118.4 mg/dL
- 最低血糖 (Min Glucose) - 例如：82 mg/dL
- 最高血糖 (Max Glucose) - 例如：156 mg/dL
- 目标范围内时间 (Time In Range 70-140) - 例如：74.7%
- 读数次数 (Reading Count) - 例如：48 次
```

### 4️⃣ **7 天统计** (7-Day Metrics)
```
- 7 天平均血糖 (7-Day Average Glucose)
- 7 天目标范围内时间 (7-Day Time In Range)
```

### 5️⃣ **检测到的血糖模式** (Detected Patterns)
```
每个模式包含：
- 模式名称 (Pattern Name) - 例如：post_meal_spike, dawn_phenomenon
- 严重程度 (Severity) - low / medium / high
- 置信度 (Confidence) - 0-100% (例如：85%)
- 模式描述 (Description) - 对模式的详细解释

示例：
- post_meal_spike (high, 85% confidence): 
  Glucose spikes after meals, particularly after high-carb meals
```

### 6️⃣ **最近的血糖读数** (Recent Glucose Readings - Last 20)
```
每条读数包含：
- 时间戳 (Timestamp)
- 血糖值 (Glucose Value) in mg/dL
- 状态 (Status) - Low / Normal / Elevated / High

示例显示：最多前 10 条最近读数的详细记录
```

### 7️⃣ **健康建议** (Recommended Health Actions)
```
每条建议包含：
- 标题 (Title) - 例如："Reduce refined carbohydrates"
- 详细说明 (Detail) - 具体建议内容
- 类别 (Category) - diet / exercise / sleep / medication
- 优先级 (Priority) - 1-5 级 (高级优先级显示)

示例显示：最多前 5 条高优先级建议
```

### 8️⃣ **对话指示** (Instructions for Olivia)
Olivia 被明确指示：
1. 热情地问候用户并确认他们的当前血糖状态
2. 利用个人信息来定制回应
3. 参考检测到的模式并解释其含义
4. 基于 24 小时和 7 天趋势提供洞察
5. 如果有高优先级建议，主动提出建议
6. 展示对改进和用户做得好的地方的热情
7. 对数据中显示的任何挑战表示支持
8. 提出后续问题以了解用户对血糖管理的感受

---

## 🔄 数据流程

```
Flask API (后端)
    ↓
    ├─ /api/user/{userId}              → 个人信息
    ├─ /api/glucose/{userId}           → 当前血糖
    ├─ /api/stats/{userId}             → 24小时统计
    ├─ /api/stats/{userId}?days=7      → 7天统计
    ├─ /api/recent/{userId}/20         → 最近20条读数
    ├─ /api/patterns/{userId}          → 检测到的模式
    └─ /api/actions                    → 健康建议
    ↓
App.tsx - fetchUserData()
    ↓
buildConversationalContext()  (格式化为 markdown)
    ↓
Tavus API v2/conversations
    ├─ conversational_context (上述所有信息)
    └─ custom_greeting (用户名和欢迎词)
    ↓
Tavus Video Avatar (Olivia)
    ↓
用户对话开始 🎥
```

---

## 📊 Context 示例

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
- post_meal_spike (high, 85% confidence): Glucose spikes after meals, particularly after high-carb meals
- dawn_phenomenon (medium, 72% confidence): Elevated glucose in early morning hours
- post_exercise_drop (low, 58% confidence): Gradual glucose decrease during/after exercise

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 RECENT GLUCOSE READINGS (Last 20):
  2025-10-27T08:30:00Z: 156 mg/dL (Elevated)
  2025-10-27T08:00:00Z: 142 mg/dL (Elevated)
  2025-10-27T07:30:00Z: 128 mg/dL (Normal)
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 RECOMMENDED HEALTH ACTIONS:
- [diet] Reduce refined carbohydrates: Try replacing white rice with brown rice or quinoa. (Priority: 5)
- [exercise] Increase daily activity: Aim for at least 30 minutes of moderate exercise. (Priority: 4)
- [diet] Improve meal timing: Eat meals at consistent times to stabilize glucose. (Priority: 4)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTRUCTIONS FOR OLIVIA:
1. Greet John Doe warmly and acknowledge their current glucose status
2. Use the personal information to tailor your response
...
```

---

## ✨ 数字人能做什么

有了这些丰富的上下文信息，Olivia 现在可以：

✅ **个性化问候**
- "Hi John! I see your glucose is at 114 mg/dL and in target range. Great work!"

✅ **参考具体数据**
- "Your Time In Range is 74.7%, which shows good control. Let's keep pushing for 80%!"
- "I noticed your 7-day average is 120.2 mg/dL, up slightly from yesterday..."

✅ **识别和解释模式**
- "I've detected a post-meal spike pattern with 85% confidence. This means your glucose tends to spike after meals, especially high-carb ones. Let me suggest some strategies..."

✅ **提供针对性建议**
- "Based on your dawn phenomenon pattern, I'd recommend a light evening snack with protein..."

✅ **追踪趋势**
- "Your Time In Range improved 2.1% compared to last week! You're doing amazing!"

✅ **智能对话**
- "I see you had some elevated readings after lunch. How did that meal feel to you?"

---

## 🔧 技术细节

### 文件位置
- **App.tsx**: `cgm-avatar-app/src/App.tsx`
- **核心函数**:
  - `fetchUserData()` - 从 Flask API 获取所有数据
  - `buildConversationalContext()` - 格式化为 markdown context

### API 端点
Flask 后端必须提供以下端点：
- `GET /api/user/<user_id>` - 用户信息
- `GET /api/glucose/<user_id>` - 当前血糖
- `GET /api/stats/<user_id>?days=7` - 统计数据
- `GET /api/recent/<user_id>/20` - 最近读数
- `GET /api/patterns/<user_id>` - 检测模式
- `GET /api/actions` - 健康建议

### 浏览器控制台调试
启动 React 应用后，在浏览器 DevTools Console 中可以看到：
```
📍 Initializing for user: user_001
Creating conversation with context: [完整的格式化 context]
✅ Conversation created successfully
Conversation URL: https://tavus.daily.co/...
```

---

## 🎯 使用建议

1. **监控 Console 输出**: 查看完整的 context 信息了解数字人获得了什么数据
2. **测试不同用户**: 切换用户看 context 如何变化
3. **数据更新**: Flask API 的数据越新鲜，Olivia 的对话就越准确
4. **模式检测**: 确保 pattern_identification 模块定期运行，以获得最新的模式检测

---

## 📝 相关文件

- `cgm-avatar-app/src/App.tsx` - React 应用主文件
- `dashboard/app.py` - Flask API 后端
- `digital_avatar/config.py` - 配置文件
- `database/cgm_database.py` - 数据库接口

