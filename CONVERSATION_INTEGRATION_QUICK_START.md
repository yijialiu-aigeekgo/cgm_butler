# 对话历史保存系统 - 快速参考 ⚡

## 🎯 一页纸总结

### 什么？
所有用户与 Olivia 助手的对话现在会自动保存到数据库。

### 哪里？
- `digital_avatar/gpt_chat.py` - GPT 聊天管理
- `database/conversation_manager.py` - 对话存储管理
- `digital_avatar/chat.html` - 前端自动保存逻辑
- `conversations` 表 - 存储所有对话

### 怎么用？

#### 1. 启动系统
```bash
# 启动 Flask
cd dashboard && python app.py

# 打开聊天界面
start_chat.bat  # Windows
# 或访问 http://localhost:5000/chat
```

#### 2. 对话会自动保存（三个触发点）
✅ **用户切换** - 切换用户时保存前一个用户的对话  
✅ **自动保存** - 每 10 条消息自动保存一次  
✅ **页面卸载** - 关闭页面时保存所有对话  

#### 3. 查询对话历史
```python
from database.conversation_manager import ConversationManager

manager = ConversationManager()

# 获取用户所有对话
convs = manager.get_user_conversations('user_001', limit=10)

# 获取统计信息
stats = manager.get_conversation_stats('user_001')
print(f"总对话数: {stats['total_conversations']}")
```

---

## 📊 数据库表

### conversations 表
```
conversation_id    - 对话唯一ID (UUID)
user_id           - 用户ID
conversation_type - 'gpt_chat' 或 'tavus_video'
transcript        - JSON 数组 [{role, content, timestamp}...]
started_at        - 开始时间
ended_at          - 结束时间
duration_seconds  - 对话时长
status            - 'active' / 'ended'
```

### conversation_analysis 表
```
analysis_id       - 分析ID
conversation_id   - 对应的对话ID
summary           - 对话摘要
key_topics        - 关键话题 (JSON)
user_sentiment    - 情感分析
engagement_score  - 参与度 (0-100)
```

---

## 🔌 API 端点

### POST /api/avatar/gpt/start
```json
{"user_id": "user_001"}
→ {"success": true, "message": "对话已开始"}
```

### POST /api/avatar/gpt/chat
```json
{"user_id": "user_001", "message": "..."}
→ {"success": true, "message": "..."}
```

### POST /api/avatar/gpt/end
```json
{"user_id": "user_001"}
→ {"success": true, "conversation_id": "uuid", "duration_seconds": 300}
```

### GET /api/avatar/gpt/history/user_001
```
?limit=10&days=7
→ {"conversations": [...], "stats": {...}}
```

---

## 💡 代码示例

### 后端：保存对话
```python
from digital_avatar.gpt_chat import GPTChatManager

gpt = GPTChatManager()
gpt.start_conversation('user_001')

# 进行对话
result = gpt.chat('user_001', '我的血糖是多少？')

# 保存对话
save_result = gpt.end_conversation('user_001')
print(f"对话ID: {save_result['conversation_id']}")
```

### 前端：JavaScript
```javascript
// 自动触发（无需手动调用）
// 1. 用户切换时
changeUser()  // 自动调用 saveConversation()

// 2. 自动保存（每 10 条消息）
autoSaveConversation()  // 自动

// 3. 页面卸载时
window.addEventListener('beforeunload', () => {
    saveConversation(currentUserId)
})
```

---

## ✅ 测试

### 运行集成测试
```bash
python test_integration.py
```

### 验证数据库
```bash
cd database && python verify_tables.py
```

---

## 🎯 功能检查清单

| 功能 | 状态 | 说明 |
|------|------|------|
| 自动保存 | ✅ | 三个触发点 |
| 时间追踪 | ✅ | 开始/结束/时长 |
| Transcript | ✅ | 完整消息+时间戳 |
| 查询 | ✅ | 按用户/类型/日期 |
| 统计 | ✅ | 计数/分布/跟进 |
| 分析 | ✅ | 情感/意图/话题 |
| 多类型 | ✅ | GPT + Tavus |

---

## 🚀 下一步

- [ ] Tavus 视频对话集成
- [ ] AI 自动分析功能
- [ ] Web 查询界面
- [ ] 报告生成模块
- [ ] 数据导出功能

---

## 📞 常见问题

**Q: 对话保存在哪里？**  
A: SQLite 数据库的 `conversations` 表

**Q: 如何查询对话？**  
A: 使用 `ConversationManager.get_user_conversations()`

**Q: 能否手动保存？**  
A: 可以，调用 `gpt_chat_manager.end_conversation(user_id)`

**Q: Transcript 中包含什么？**  
A: 用户消息、Olivia 回复、时间戳、函数调用信息

**Q: 如何删除对话？**  
A: 直接从数据库删除 (注意 conversation_id 外键约束)

---

## 📚 完整文档

- [INTEGRATION_COMPLETE.md](./INTEGRATION_COMPLETE.md) - 完整集成报告
- [INTEGRATION_SUMMARY.md](./INTEGRATION_SUMMARY.md) - 集成细节
- [CONVERSATION_HISTORY_GUIDE.md](./CONVERSATION_HISTORY_GUIDE.md) - 详细使用指南

---

**集成完成日期**: 2025-10-27  
**版本**: 1.0.0  
**状态**: ✅ 生产就绪

