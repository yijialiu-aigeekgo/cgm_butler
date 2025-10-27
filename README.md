# CGM Butler

智能血糖管理助手 - 通过分析 CGM (连续血糖监测) 数据,为用户提供个性化的健康建议和生活方式指导。

## 项目概述

### 目标用户
- 年龄: 25-45岁
- 关心健康,有付费能力和付费意愿的群体

### 核心功能
1. **数据分析**: 分析 CGM 数据,识别血糖模式
2. **智能提醒**: 每天向用户汇报血糖模式,建议改进行动
3. **聊天互动**: 与用户对话,收集饮食和生活方式数据
4. **血糖预测**: 预测食物/运动对血糖的影响
5. **上下文引擎**: 对比用户目标和数据,主动提问以提供个性化建议

### 呈现形式
- **数字人**: 男性用户 → 女管家, 女性用户 → 帅哥管家
- **性格**: 给予情绪价值,鼓励用户,applaud achievement

## 项目结构

```
cgm butler/
├── database/              # 数据库模块
│   ├── cgm_database.py   # 数据库操作工具类
│   ├── setup_database.py # 数据库初始化脚本
│   ├── query_database.py # 查询工具
│   ├── test_database.py  # 测试脚本
│   ├── database_schema.sql # SQL Schema
│   ├── cgm_butler.db     # SQLite 数据库
│   └── README.md         # 数据库模块文档
│
├── dashboard/            # Web Dashboard (实时数据可视化)
│   ├── app.py           # Flask 应用
│   ├── templates/       # HTML 模板
│   └── README.md        # Dashboard 文档
│
├── README.md             # 项目主文档 (本文件)
├── QUICKSTART.md         # 快速开始指南
├── start_dashboard.bat   # Dashboard 启动脚本
├── requirements.txt      # 依赖列表
└── .gitignore           # Git 忽略规则
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
cd database
python setup_database.py
```

### 3. 启动 Web Dashboard (实时查看数据)

```bash
# 方法一: 使用启动脚本
start_dashboard.bat

# 方法二: 命令行启动
cd dashboard
python app.py
```

然后在浏览器中打开: http://localhost:5000

### 4. 使用数据库

```python
from database import CGMDatabase

# 使用上下文管理器
with CGMDatabase('database/cgm_butler.db') as db:
    # 获取用户信息
    user = db.get_user('user_001')
    
    # 获取血糖统计
    stats = db.get_glucose_statistics('user_001')
    
    # 计算 Time In Range
    tir = db.get_time_in_range('user_001', 70, 140)
    
    # 获取建议
    actions = db.get_pattern_actions(min_priority=4)
```

## Web Dashboard (实时数据可视化)

### 🎯 核心特性
- ✨ **实时自动刷新** - 每 5 秒自动更新数据
- 📊 **可视化图表** - Chart.js 绘制血糖趋势
- 📱 **响应式设计** - 支持电脑、平板、手机
- 🎨 **现代化 UI** - 美观的渐变色界面
- ⚡ **RESTful API** - 提供完整的数据接口

### 📊 Dashboard 功能
- 用户信息卡片
- 血糖统计 (含 Time In Range)
- 最新读数 (实时状态)
- 血糖趋势图 (最近 50 条)
- 最近读数表格 (最近 20 条)
- 健康建议列表

详细信息请查看 [`dashboard/README.md`](dashboard/README.md)

## 数据库模块

数据库模块提供完整的 CGM 数据管理功能:

### 核心功能
- ✅ 用户信息管理
- ✅ CGM 数据存储和查询
- ✅ 血糖统计分析
- ✅ Time In Range 计算
- ✅ 餐后血糖飙升检测
- ✅ 每日血糖总结
- ✅ Pattern-Action 建议系统

### 数据库表结构

**users** - 用户信息表
- 用户基本信息、健康目标、CGM 设备信息

**cgm_readings** - CGM 读数表
- 连续血糖监测数据,每 5 分钟一条记录
- 已建立索引优化查询性能

**cgm_pattern_actions** - Pattern-Action 映射表
- 血糖模式和对应的建议行动
- 按类别 (diet/exercise/sleep/other) 和优先级 (1-5) 组织

详细信息请查看 [`database/README.md`](database/README.md)

## 开发路线图

### ✅ 已完成 (Phase 1)
- [x] 数据库设计和实现
- [x] 数据库操作工具类
- [x] 基础数据分析功能
- [x] 完整的测试和文档

### 🚧 进行中 (Phase 2)
- [ ] 生活方式记录功能 (饮食、运动、睡眠、压力)
- [ ] 对话记录系统
- [ ] 基础模式识别算法

### 📋 计划中 (Phase 3)
- [ ] 用户画像系统
- [ ] 血糖预测模型
- [ ] 每日报告生成

### 🎯 未来规划 (Phase 4+)
- [ ] LLM 对话系统集成
- [ ] 数字人前端界面
- [ ] CGM 设备 API 对接
- [ ] 高级分析和机器学习

## 技术栈

### 当前
- **数据库**: SQLite 3
- **编程语言**: Python 3.7+
- **依赖**: 内置库 (sqlite3, datetime, typing)

### 计划
- **后端**: Flask/FastAPI
- **前端**: React/Vue
- **AI**: OpenAI API / 本地 LLM
- **数据分析**: NumPy, Pandas, Scikit-learn
- **可视化**: Matplotlib, Plotly

## 文档

- **[快速开始指南](QUICKSTART.md)** - 5 分钟快速上手
- **[项目结构文档](PROJECT_STRUCTURE.md)** - 详细的项目结构说明
- **[数据库模块文档](database/README.md)** - 数据库使用指南
- **[项目完成总结](项目完成总结.md)** - Phase 1 完成总结

## 血糖范围定义

| 范围 | 血糖值 (mg/dL) | 说明 |
|------|----------------|------|
| 低血糖 | < 70 | 需要立即处理 |
| 正常 | 70-140 | 目标范围 (Time In Range) |
| 偏高 | 141-180 | 需要注意 |
| 高血糖 | > 180 | 需要干预 |

## 示例数据

项目包含 7 天的模拟 CGM 数据:
- **记录数**: 2016 条 (每 5 分钟一条)
- **平均血糖**: 117.0 mg/dL
- **Time In Range**: 76.5%
- **血糖范围**: 80-171 mg/dL

数据模拟了真实的血糖波动:
- 餐后血糖上升 (早/午/晚餐)
- 夜间血糖稳定
- 随机波动

## 贡献指南

欢迎贡献代码、报告问题或提出建议!

### 开发流程
1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 注意事项

1. **数据隐私**: 遵守医疗数据隐私法规 (HIPAA/GDPR)
2. **数据安全**: 生产环境需要添加用户认证和数据加密
3. **数据库选择**: 当前使用 SQLite 适合原型开发,生产环境建议迁移到 MySQL/PostgreSQL
4. **医疗免责**: 本项目仅供参考,不构成医疗建议

## 许可证

待定

## 联系方式

待定

---

**当前版本**: v1.0.0 (Phase 1 完成)  
**最后更新**: 2025-10-26  
**状态**: ✅ 数据库模块已完成,准备开始 Phase 2 开发
