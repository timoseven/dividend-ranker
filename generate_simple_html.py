#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成简单的股息率排名HTML文件，基于2025年数据
"""

import os
import csv

def generate_simple_html():
    """生成HTML文件"""
    stocks_id_file = "stocks.id"
    csv_file = "output/all_dividend_yield_2025.csv"
    output_html = "output/dividend_ranker.html"
    
    # 读取stocks.id中的股票列表
    selected_stocks = {}  # 股票代码 -> 股票名称
    with open(stocks_id_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                stock_code, stock_name = line.split(maxsplit=1)
                selected_stocks[stock_code] = stock_name
    
    print(f"共读取到{len(selected_stocks)}只股票")
    
    # 读取CSV文件，筛选出selected_stocks中的股票
    stock_data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stock_code = row["股票代码"]
            if stock_code in selected_stocks:
                stock_data.append({
                    "股票代码": stock_code,
                    "股票名称": selected_stocks[stock_code],
                    "2025年累计分红": float(row["2025年累计分红"]),
                    "2025-11-28收盘价": float(row["2025-11-28收盘价"]),
                    "股息率(%)": float(row["股息率(%)"])
                })
    
    print(f"共匹配到{len(stock_data)}只股票的数据")
    
    # 按股息率降序排序
    stock_data.sort(key=lambda x: x["股息率(%)"], reverse=True)
    
    # 生成HTML头部
    html_header = """<!DOCTYPE html>
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
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
            cursor: pointer;
        }
        th:hover {
            background-color: #e9e9e9;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .sort-indicator {
            margin-left: 5px;
            font-size: 12px;
        }
        .stock-code {
            font-weight: bold;
        }
        .high-yield {
            color: red;
        }
        .medium-yield {
            color: orange;
        }
        .low-yield {
            color: green;
        }
        .stats {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f0f8ff;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>2025年股息率排名</h1>
        <div class="stats">
            <p>共包含 <strong>{total_stocks}</strong> 只股票，按股息率降序排列</p>
            <p>数据来源：Baostock API，更新时间：2025年11月28日</p>
        </div>
        <table id="dividendTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">排名 <span class="sort-indicator">▼</span></th>
                    <th onclick="sortTable(1)">股票代码 <span class="sort-indicator"></span></th>
                    <th onclick="sortTable(2)">股票名称 <span class="sort-indicator"></span></th>
                    <th onclick="sortTable(3)">2025年累计分红 <span class="sort-indicator"></span></th>
                    <th onclick="sortTable(4)">2025-11-28收盘价 <span class="sort-indicator"></span></th>
                    <th onclick="sortTable(5)">股息率(%) <span class="sort-indicator"></span></th>
                </tr>
            </thead>
            <tbody>
"""
    
    # 生成HTML尾部
    html_footer = """
            </tbody>
        </table>
    </div>
    
    <script>
        function sortTable(n) {
            const table = document.getElementById("dividendTable");
            const tbody = table.getElementsByTagName("tbody")[0];
            const rows = Array.from(tbody.getElementsByTagName("tr"));
            const headers = table.getElementsByTagName("th");
            
            // Reset sort indicators
            for (let header of headers) {
                header.querySelector(".sort-indicator").textContent = "";
            }
            
            // Determine sort direction
            const currentIndicator = headers[n].querySelector(".sort-indicator");
            const isAscending = currentIndicator.textContent !== "▼";
            
            // Set sort indicator
            currentIndicator.textContent = isAscending ? "▼" : "▲";
            
            // Sort rows
            rows.sort((a, b) => {
                const aVal = a.cells[n].textContent;
                const bVal = b.cells[n].textContent;
                
                // Handle numeric values
                if (!isNaN(parseFloat(aVal)) && isFinite(aVal)) {
                    return isAscending 
                        ? parseFloat(aVal) - parseFloat(bVal)
                        : parseFloat(bVal) - parseFloat(aVal);
                } else {
                    // Handle text values
                    return isAscending 
                        ? aVal.localeCompare(bVal, "zh-CN")
                        : bVal.localeCompare(aVal, "zh-CN");
                }
            });
            
            // Update row indices for rank column
            rows.forEach((row, index) => {
                row.cells[0].textContent = index + 1;
            });
            
            // Append sorted rows back to tbody
            rows.forEach(row => tbody.appendChild(row));
        }
    </script>
</body>
</html>"""
    
    # 生成表格内容
    table_content = ""
    for i, stock in enumerate(stock_data, 1):
        # 根据股息率设置颜色
        if stock["股息率(%)"] > 5:
            yield_class = "high-yield"
        elif stock["股息率(%)"] > 3:
            yield_class = "medium-yield"
        else:
            yield_class = "low-yield"
        
        table_content += f"""
                <tr>
                    <td>{i}</td>
                    <td class="stock-code">{stock['股票代码']}</td>
                    <td>{stock['股票名称']}</td>
                    <td>{stock['2025年累计分红']:.4f}</td>
                    <td>{stock['2025-11-28收盘价']:.2f}</td>
                    <td class="{yield_class}">{stock['股息率(%)']:.2f}%</td>
                </tr>
"""
    
    # 组合HTML内容并替换占位符
    total_stocks = len(stock_data)
    html_content = html_header.replace("{total_stocks}", str(total_stocks)) + table_content + html_footer
    
    # 写入HTML文件
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML文件已生成: {output_html}")
    return True

if __name__ == "__main__":
    generate_simple_html()
