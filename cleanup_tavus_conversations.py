#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理所有 Tavus 对话
Clean up all Tavus conversations
"""

import requests
import json
import sys
import io
import time

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_KEY = "2baf6b72f7dc4c728132e63193c1dac7"
BASE_URL = "https://tavusapi.com/v2"

print("\n" + "="*70)
print("🧹 Tavus 对话清理工具")
print("Tavus Conversation Cleanup Tool")
print("="*70 + "\n")

def get_all_conversations():
    """获取所有对话"""
    print("📋 正在获取所有对话列表...")
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(f"{BASE_URL}/conversations", headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict):
                if 'data' in result:
                    conversations = result['data']
                elif 'conversations' in result:
                    conversations = result['conversations']
                else:
                    conversations = []
            elif isinstance(result, list):
                conversations = result
            else:
                conversations = []
            print(f"✅ 获取成功！找到 {len(conversations)} 个对话")
            return conversations
        else:
            print(f"❌ 获取失败，状态码: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return []
    except Exception as e:
        print(f"❌ 错误: {e}")
        return []

def delete_conversation(conversation_id):
    """删除单个对话"""
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.delete(f"{BASE_URL}/conversations/{conversation_id}", headers=headers, timeout=10)
        if response.status_code in [200, 204, 304]:
            print(f"   ✅ 对话 {conversation_id} 已删除")
            return True
        else:
            print(f"   ⚠️ 删除失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False

def cleanup_all():
    """清理所有对话"""
    conversations = get_all_conversations()
    if not conversations:
        print("\n✅ 没有需要清理的对话！")
        return
    
    print(f"\n🗑️  正在删除 {len(conversations)} 个对话...")
    deleted_count = 0
    for conv in conversations:
        if isinstance(conv, dict):
            conv_id = conv.get('conversation_id', 'unknown')
            status = conv.get('status', 'unknown')
        else:
            conv_id = str(conv)
            status = 'unknown'
        print(f"删除对话 {conv_id} (状态: {status})...")
        if delete_conversation(conv_id):
            deleted_count += 1
        time.sleep(0.5)
    
    print(f"\n✅ 清理完成！已删除 {deleted_count}/{len(conversations)} 个对话")
    print("="*70)
    
    # 验证清理结果
    print("\n🔍 验证清理结果...")
    remaining = get_all_conversations()
    if len(remaining) == 0:
        print("✅ 所有对话已清理，现在可以创建新对话了！")
    else:
        print(f"⚠️ 还有 {len(remaining)} 个对话未清理")

if __name__ == "__main__":
    cleanup_all()

