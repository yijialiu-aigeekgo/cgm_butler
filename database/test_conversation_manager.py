# test_conversation_manager.py
# -*- coding: utf-8 -*-
"""测试 ConversationManager 是否可以正常保存和查询对话"""
import os
from conversation_manager import ConversationManager
from datetime import datetime

def test_conversation_manager():
    """测试对话管理器"""
    
    # 获取数据库路径
    db_path = os.path.join(os.path.dirname(__file__), 'cgm_butler.db')
    
    print("=" * 60)
    print("开始测试 ConversationManager...")
    print("=" * 60)
    
    # 初始化管理器
    manager = ConversationManager(db_path)
    print("\n✅ 初始化管理器成功")
    
    # 测试保存 GPT 对话
    print("\n[测试1] 保存 GPT 对话...")
    transcript = [
        {
            "role": "user",
            "content": "我的血糖是多少?",
            "timestamp": datetime.now().isoformat()
        },
        {
            "role": "assistant",
            "content": "你的当前血糖是 114 mg/dL，状态正常。",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    conv_id = manager.save_gpt_conversation(
        user_id='user_001',
        transcript=transcript,
        conversational_context='用户询问当前血糖',
        started_at=datetime.now().isoformat(),
        status='ended'
    )
    print(f"✅ GPT 对话已保存: {conv_id}")
    
    # 测试获取对话
    print("\n[测试2] 查询对话...")
    conversation = manager.get_conversation(conv_id)
    if conversation:
        print(f"✅ 对话查询成功")
        print(f"   - 用户ID: {conversation['user_id']}")
        print(f"   - 类型: {conversation['conversation_type']}")
        print(f"   - 对话轮数: {len(conversation['transcript'])}")
        print(f"   - 状态: {conversation['status']}")
    else:
        print(f"❌ 对话查询失败")
        return
    
    # 测试保存分析
    print("\n[测试3] 保存对话分析...")
    analysis_id = manager.save_analysis(
        conversation_id=conv_id,
        summary='用户询问了当前血糖水平',
        key_topics=['blood_sugar', 'current_status'],
        user_intents=['seeking_information'],
        user_sentiment='neutral',
        engagement_score=85.0
    )
    print(f"✅ 分析已保存: {analysis_id}")
    
    # 测试获取分析
    print("\n[测试4] 查询分析...")
    analysis = manager.get_analysis(conv_id)
    if analysis:
        print(f"✅ 分析查询成功")
        print(f"   - 摘要: {analysis['summary']}")
        print(f"   - 情感: {analysis['user_sentiment']}")
        print(f"   - 参与度: {analysis['engagement_score']}")
    else:
        print(f"❌ 分析查询失败")
        return
    
    # 测试获取用户所有对话
    print("\n[测试5] 查询用户所有对话...")
    user_convs = manager.get_user_conversations('user_001', limit=10)
    print(f"✅ 找到 {len(user_convs)} 条对话")
    
    # 测试统计
    print("\n[测试6] 获取统计信息...")
    stats = manager.get_conversation_stats('user_001')
    print(f"✅ 统计信息:")
    print(f"   - 总对话数: {stats['total_conversations']}")
    print(f"   - 对话类型分布: {stats['by_type']}")
    print(f"   - 需要跟进: {stats['follow_up_needed']}")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！ConversationManager 可以正常工作！")
    print("=" * 60)

if __name__ == '__main__':
    test_conversation_manager()

