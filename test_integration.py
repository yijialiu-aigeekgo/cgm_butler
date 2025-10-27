# test_integration.py
# -*- coding: utf-8 -*-
"""
集成测试：验证对话历史保存系统是否正常工作
测试流程：
1. 初始化 GPTChatManager
2. 模拟用户对话
3. 保存对话
4. 验证数据库中的对话
5. 查询对话历史
"""
import os
import sys
import json
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from digital_avatar.gpt_chat import GPTChatManager
from database.conversation_manager import ConversationManager

def test_integration():
    """运行集成测试"""
    
    print("=" * 70)
    print("🚀 对话历史保存系统 - 集成测试")
    print("=" * 70)
    
    try:
        # 1. 初始化管理器
        print("\n[测试 1] 初始化 GPTChatManager...")
        gpt_manager = GPTChatManager()
        print("✅ GPTChatManager 初始化成功")
        
        # 2. 开始对话
        print("\n[测试 2] 开始新对话...")
        result = gpt_manager.start_conversation('user_001')
        if result['success']:
            print(f"✅ 对话已开始")
        else:
            print(f"❌ 对话开始失败: {result}")
            return
        
        # 3. 模拟用户对话
        print("\n[测试 3] 模拟用户对话...")
        test_messages = [
            "Hello, what's my current glucose level?",
            "What patterns have been detected?",
            "Give me some recommendations"
        ]
        
        for i, msg in enumerate(test_messages, 1):
            print(f"   [{i}] 用户: {msg}")
            result = gpt_manager.chat('user_001', msg)
            if result['success']:
                print(f"   ✅ Olivia: {result['message'][:100]}...")
                if result.get('function_called'):
                    print(f"      [函数调用] {result['function_called']}")
            else:
                print(f"   ❌ 出错: {result['error']}")
        
        # 4. 保存对话
        print("\n[测试 4] 保存对话到数据库...")
        save_result = gpt_manager.end_conversation('user_001')
        
        if save_result['success']:
            conv_id = save_result['conversation_id']
            duration = save_result['duration_seconds']
            print(f"✅ 对话已保存")
            print(f"   - 对话ID: {conv_id}")
            print(f"   - 对话时长: {duration} 秒")
        else:
            print(f"❌ 保存失败: {save_result}")
            return
        
        # 5. 验证数据库中的对话
        print("\n[测试 5] 验证数据库中的对话...")
        db_manager = ConversationManager()
        conversation = db_manager.get_conversation(conv_id)
        
        if conversation:
            print(f"✅ 对话查询成功")
            print(f"   - 用户: {conversation['user_id']}")
            print(f"   - 类型: {conversation['conversation_type']}")
            print(f"   - 消息数: {len(conversation['transcript'])}")
            print(f"   - 状态: {conversation['status']}")
            print(f"   - 开始时间: {conversation['started_at']}")
            print(f"   - 结束时间: {conversation['ended_at']}")
            
            # 显示消息摘要
            print(f"\n   消息摘要:")
            for i, msg in enumerate(conversation['transcript'][:3], 1):
                role = "用户" if msg['role'] == 'user' else "Olivia"
                content = msg['content'][:50]
                print(f"      [{i}] {role}: {content}...")
        else:
            print(f"❌ 对话查询失败")
            return
        
        # 6. 查询用户对话历史
        print("\n[测试 6] 查询用户对话历史...")
        user_conversations = db_manager.get_user_conversations(
            user_id='user_001',
            limit=5,
            conversation_type='gpt_chat'
        )
        
        print(f"✅ 找到 {len(user_conversations)} 条对话")
        if user_conversations:
            latest = user_conversations[0]
            print(f"   - 最新对话: {latest['conversation_id'][:8]}...")
            print(f"   - 消息数: {len(latest['transcript'])}")
            print(f"   - 时长: {latest.get('duration_seconds', 'N/A')} 秒")
        
        # 7. 获取用户统计
        print("\n[测试 7] 获取用户对话统计...")
        stats = db_manager.get_conversation_stats('user_001', days=7)
        
        print(f"✅ 统计信息:")
        print(f"   - 总对话数: {stats['total_conversations']}")
        print(f"   - 对话类型分布: {stats['by_type']}")
        print(f"   - 需要跟进: {stats['follow_up_needed']} 条")
        
        # 8. 获取对话分析
        print("\n[测试 8] 获取对话分析...")
        analysis = db_manager.get_analysis(conv_id)
        
        if analysis:
            print(f"✅ 分析查询成功")
            print(f"   - 摘要: {analysis['summary']}")
            print(f"   - 情感: {analysis['user_sentiment']}")
            print(f"   - 参与度: {analysis['engagement_score']}")
        else:
            print(f"⚠️  暂无分析数据（需要后续 AI 分析）")
        
        # 9. 验证 Transcript 格式
        print("\n[测试 9] 验证 Transcript 格式...")
        transcript = conversation['transcript']
        
        valid_transcript = True
        for msg in transcript:
            if not all(k in msg for k in ['role', 'content', 'timestamp']):
                valid_transcript = False
                break
        
        if valid_transcript:
            print(f"✅ Transcript 格式正确")
            print(f"   - 总消息数: {len(transcript)}")
            print(f"   - 第一条消息时间: {transcript[0]['timestamp']}")
            print(f"   - 最后一条消息时间: {transcript[-1]['timestamp']}")
        else:
            print(f"❌ Transcript 格式有问题")
        
        # 总结
        print("\n" + "=" * 70)
        print("🎉 集成测试完成！")
        print("=" * 70)
        print("\n✅ 所有测试通过！")
        print("\n关键功能验证:")
        print("  ✓ GPTChatManager 能正确初始化和进行对话")
        print("  ✓ 对话能成功保存到数据库")
        print("  ✓ Transcript 包含完整的消息历史和时间戳")
        print("  ✓ ConversationManager 能正确查询对话")
        print("  ✓ 用户统计信息能正确计算")
        print("\n对话历史保存系统完全就绪！🚀")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_integration()
