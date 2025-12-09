#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成股息率排名HTML文件
"""

import os
import csv

def generate_dividend_html():
    """生成HTML文件"""
    # 读取stocks.id文件，获取股票列表
    stocks_id_file = "stocks.id"
    csv_file = "output/all_dividend_yield_2025.csv"
    output_html = "output/dividend_ranker.html"
    
    # 读取stocks.id文件
    selected_stocks = set()
    with open(stocks_id_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                # 提取股票代码
                stock_code = line.split()[0]
                selected_stocks.add(stock_code)
    
    print(f"共读取到{len(selected_stocks)}只股票ID")
    
    # 读取CSV文件，获取股票详细数据
    stock_data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stock_code = row["股票代码"]
            if stock_code in selected_stocks:
                stock_data.append({
                    "股票代码": row["股票代码"],
                    "股票名称": row["股票名称"],
                    "2025年累计分红": float(row["2025年累计分红"]),
                    "2025-11-28收盘价": float(row["2025-11-28收盘价"]),
                    "股息率(%)": float(row["股息率(%)"])
                })
    
    print(f"共获取到{len(stock_data)}只股票的详细数据")
    
    # 按股息率降序排序
    stock_data.sort(key=lambda x: x["股息率(%)"], reverse=True)
    
    # 生成HTML内容
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股息率排名 - 2025年</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0