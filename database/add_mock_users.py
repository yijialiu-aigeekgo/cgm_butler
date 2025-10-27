# add_mock_users.py
# -*- coding: utf-8 -*-
"""
添加 10 个模拟用户和他们的 CGM 数据
"""
import sqlite3
from datetime import datetime, timedelta
import random
import sys
import io

# 设置 Windows 控制台输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = 'database/cgm_butler.db'

# 模拟数据生成函数
def generate_mock_cgm_data(user_id, start_date, end_date, interval_minutes=5):
    data = []
    current_time = start_date
    while current_time <= end_date:
        glucose_value = random.randint(80, 180)
        status = 'Normal' if 70 <= glucose_value <= 140 else 'Alert'
        data.append((user_id, current_time, glucose_value, status))
        current_time += timedelta(minutes=interval_minutes)
    return data


def add_mock_cgm_data():
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 获取所有用户
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()

    # 设置时间范围（过去24小时）
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=24)

    for user in users:
        user_id = user[0]
        mock_data = generate_mock_cgm_data(user_id, start_date, end_date)

        # 插入模拟数据（去掉status列）
        cursor.executemany('INSERT INTO cgm_readings (user_id, timestamp, glucose_value) VALUES (?, ?, ?)', 
                           [(d[0], d[1], d[2]) for d in mock_data])
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_mock_cgm_data()
    print("✅ 模拟CGM数据已添加到所有用户。")

