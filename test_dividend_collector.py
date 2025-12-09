#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证CSV保存功能
"""

import os
import csv

def test_csv_save():
    """测试CSV保存功能"""
    print("测试CSV保存功能...")
    
    # 测试数据
    test_data = [
        {
            "股票代码": "sh.600000",
            "股票名称": "浦发银行",
            "2025年累计分红": 0.41,
            "2025-11-28收盘价": 11.48,
            "股息率(%)": 3.57
        },
        {
            "股票代码": "sh.600036",
            "股票名称": "招商银行",
            "2025年累计分红": 1.75,
            "2025-11-28收盘价": 34.56,
            "股息率(%)": 5.06
        }
    ]
    
    # 检查output目录
    output_dir = "output"
    if not os.path.exists(output_dir):
        print(f"创建output目录: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    else:
        print(f"output目录已存在: {output_dir}")
    
    # 保存测试数据
    csv_path = os.path.join(output_dir, "test_dividend.csv")
    print(f"保存测试数据到: {csv_path}")
    
    fieldnames = list(test_data[0].keys())
    
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in test_data:
                writer.writerow(row)
        print(f"测试数据保存成功，共{len(test_data)}条记录")
        
        # 验证文件存在
        if os.path.exists(csv_path):
            print(f"文件已生成: {csv_path}")
            print(f"文件大小: {os.path.getsize(csv_path)} bytes")
            # 读取并显示内容
            with open(csv_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print("文件内容:")
            print(content)
        else:
            print("文件未生成！")
    except Exception as e:
        print(f"保存文件时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_csv_save()
