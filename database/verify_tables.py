# verify_tables.py
# -*- coding: utf-8 -*-
"""验证数据库表是否正确创建"""
import sqlite3
import os
import sys
import io

# 设置 Windows 控制台输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = os.path.join(os.path.dirname(__file__), 'cgm_butler.db')

print("=" * 60)
print("验证数据库表...")
print("=" * 60)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 获取所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("\n✅ 数据库中的所有表:")
for table in tables:
    print(f"  - {table[0]}")

# 验证 conversations 表
print("\n[验证 conversations 表]")
cursor.execute("PRAGMA table_info(conversations)")
columns = cursor.fetchall()
print(f"✅ conversations 表有 {len(columns)} 列:")
for col in columns[:5]:  # 显示前5列
    print(f"  - {col[1]}: {col[2]}")
print(f"  ... 还有 {len(columns) - 5} 列")

# 验证 conversation_analysis 表
print("\n[验证 conversation_analysis 表]")
cursor.execute("PRAGMA table_info(conversation_analysis)")
columns = cursor.fetchall()
print(f"✅ conversation_analysis 表有 {len(columns)} 列:")
for col in columns:
    print(f"  - {col[1]}: {col[2]}")

# 获取索引
print("\n[验证索引]")
cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
indexes = cursor.fetchall()
print(f"✅ 数据库中有 {len(indexes)} 个索引:")
for idx in indexes:
    print(f"  - {idx[0]}")

# 获取外键关系
print("\n[验证外键关系]")
cursor.execute("PRAGMA foreign_key_list(conversations)")
fks = cursor.fetchall()
print(f"✅ conversations 表有 {len(fks)} 个外键:")
for fk in fks:
    print(f"  - {fk}")

conn.close()

print("\n" + "=" * 60)
print("✅ 数据库结构验证完成！")
print("=" * 60)
