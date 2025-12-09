#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从CSV文件中提取股息率大于3%的股票id和名字
"""

import os
import csv

def extract_high_dividend_stocks():
    """提取股息率大于3%的股票"""
    input_file = "output/all_dividend_yield_2025.csv"
    output_file = "stocks.id"
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"输入文件不存在: {input_file}")
        return False
    
    high_dividend_stocks = []
    
    # 读取CSV文件
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # 获取股息率
                dividend_yield = float(row["股息率(%)"])
                # 筛选股息率大于3%的股票
                if dividend_yield > 3:
                    high_dividend_stocks.append({
                        "股票代码": row["股票代码"],
                        "股票名称": row["股票名称"]
                    })
            except (ValueError, KeyError) as e:
                continue
    
    print(f"共找到{len(high_dividend_stocks)}只股息率大于3%的股票")
    
    # 写入到stocks.id文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for stock in high_dividend_stocks:
            # 只写入股票代码和名称，用空格分隔
            f.write(f"{stock['股票代码']} {stock['股票名称']}\n")
    
    print(f"已将{len(high_dividend_stocks)}只股票写入到: {output_file}")
    return True

if __name__ == "__main__":
    extract_high_dividend_stocks()
