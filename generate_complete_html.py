#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成2020-2025年股息率排名HTML文件，符合参考格式
"""

import os
import csv

def generate_complete_html():
    """生成完整的HTML文件"""
    csv_file = "output/2020_2025_dividend_data.csv"
    output_html = "output/dividend_rankings_2020_2025.html"
    
    # 导入math模块用于计算方差
    import math
    
    def calculate_variance(values):
        """计算样本方差"""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance
    
    # 读取CSV文件
    stock_data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 转换数值类型
            try:
                # 获取最近6年的股息率
                recent_years = [
                    float(row["2020年股息率(%)"]),
                    float(row["2021年股息率(%)"]),
                    float(row["2022年股息率(%)"]),
                    float(row["2023年股息率(%)"]),
                    float(row["2024年股息率(%)"]),
                    float(row["2025年股息率(%)"])
                ]
                
                # 计算最近6年的方差
                variance = calculate_variance(recent_years)
                
                stock_data.append({
                    "股票代码": row["股票代码"],
                    "股票名称": row["股票名称"],
                    "2020-2025年累计分红": float(row["2020-2025年累计分红"]),
                    "2020-2025年平均股息率(%)": float(row["2020-2025年平均股息率(%)"]),
                    "最近6年股息率方差": variance,
                    # 按2025年到2020年的顺序
                    "2025年分红": float(row["2025年分红"]),
                    "2025年收盘价": float(row["2025年收盘价"]),
                    "2025年股息率(%)": float(row["2025年股息率(%)"]),
                    "2024年分红": float(row["2024年分红"]),
                    "2024年收盘价": float(row["2024年收盘价"]),
                    "2024年股息率(%)": float(row["2024年股息率(%)"]),
                    "2023年分红": float(row["2023年分红"]),
                    "2023年收盘价": float(row["2023年收盘价"]),
                    "2023年股息率(%)": float(row["2023年股息率(%)"]),
                    "2022年分红": float(row["2022年分红"]),
                    "2022年收盘价": float(row["2022年收盘价"]),
                    "2022年股息率(%)": float(row["2022年股息率(%)"]),
                    "2021年分红": float(row["2021年分红"]),
                    "2021年收盘价": float(row["2021年收盘价"]),
                    "2021年股息率(%)": float(row["2021年股息率(%)"]),
                    "2020年分红": float(row["2020年分红"]),
                    "2020年收盘价": float(row["2020年收盘价"]),
                    "2020年股息率(%)": float(row["2020年股息率(%)"])
                })
            except (ValueError, KeyError) as e:
                continue
    
    print(f"共读取到{len(stock_data)}只股票的数据")
    
    # 按2020-2025年平均股息率降序排序
    stock_data.sort(key=lambda x: x["2020-2025年平均股息率(%)"], reverse=True)
    
    # 生成HTML内容
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股票股息率排名 (2020-2025)</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: #f5f7fa;
            color: #333;
            line-height: 1.4; /* 减小行间距，使内容更紧凑 */
        }
        
        .container {
            max-width: 1600px; /* 增加容器宽度 */
            margin: 0 auto;
            padding: 20px;
            width: 100%; /* 允许容器占满可用宽度 */
            min-width: 1000px; /* 设置最小宽度 */
        }
        
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
            font-size: 2.2rem; /* 减小标题大小 */
        }
        
        .section {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
            padding: 20px;
        }
        
        h2 {
            color: #34495e;
            margin-bottom: 20px;
            font-size: 1.6rem; /* 减小二级标题大小 */
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        
        .stock-table {
            width: 100%;
            border-collapse: collapse;
            overflow-x: auto;
            display: block;
            max-height: 700px; /* 增加表格高度 */
            overflow-y: auto;
        }
        
        .comparison-table {
            table-layout: auto; /* 改为auto布局，允许列宽自动调整 */
        }
        
        .comparison-table th {
            min-width: 80px; /* 调整最小宽度 */
            white-space: normal; /* 允许标题换行 */
            text-align: center; /* 居中显示 */
            vertical-align: middle; /* 垂直居中 */
        }
        
        .stock-table th,
        .stock-table td {
            padding: 8px 12px; /* 调整内边距，增加水平空间 */
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
            font-size: 13px; /* 减小文字大小 */
        }
        
        .stock-table th {
            background: #3498db;
            color: white;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 10;
            cursor: pointer;
            user-select: none;
        }
        
        .stock-table th:hover {
            background: #2980b9;
        }
        
        .stock-table tr:hover {
            background: #f8f9fa;
        }
        
        .stock-table tr:nth-child(even) {
            background: #f5f7fa;
        }
        
        .stock-info {
            font-weight: 600;
            color: #2c3e50;
            white-space: nowrap;
        }
        
        .dividend-yield {
            color: #27ae60;
            font-weight: 600;
            text-align: center;
        }
        
        .price {
            color: #e74c3c;
            font-weight: 600;
            text-align: center;
        }
        
        .header-info {
            text-align: center;
            margin-bottom: 20px;
            color: #666;
            font-size: 1.1rem;
            background-color: #e3f2fd; /* 浅蓝色背景 */
            padding: 10px;
            border-radius: 5px;
        }
        
        .comparison-table th {
            min-width: 120px;
        }
        
        /* 固定列样式 */
        .stock-table th:nth-child(1),
        .stock-table td:nth-child(1),
        .stock-table th:nth-child(2),
        .stock-table td:nth-child(2),
        .stock-table th:nth-child(3),
        .stock-table td:nth-child(3) {
            position: sticky;
            left: 0;
            background: white;
            z-index: 1;
        }
        
        .stock-table th:nth-child(1),
        .stock-table th:nth-child(2),
        .stock-table th:nth-child(3) {
            z-index: 11;
            background: #3498db;
        }
        
        .stock-table td:nth-child(2) {
            left: 50px;
        }
        
        .stock-table td:nth-child(3) {
            left: 170px;
        }
        
        /* 调整各列宽度 */
        .stock-table th:nth-child(1),
        .stock-table td:nth-child(1) {
            width: 50px;
            min-width: 50px;
            text-align: center;
        }
        
        .stock-table th:nth-child(2),
        .stock-table td:nth-child(2) {
            width: 120px;
            min-width: 120px;
        }
        
        .stock-table th:nth-child(3),
        .stock-table td:nth-child(3) {
            width: 100px;
            min-width: 100px;
        }
        
        .stock-table th:nth-child(4),
        .stock-table td:nth-child(4) {
            width: 100px;
            min-width: 100px;
            text-align: center;
        }
        
        .stock-table th:nth-child(5),
        .stock-table td:nth-child(5) {
            width: 100px;
            min-width: 100px;
            text-align: center;
        }
        
        /* 年份相关列的宽度 */
        .stock-table th:nth-child(n+6):nth-child(-n+23),
        .stock-table td:nth-child(n+6):nth-child(-n+23) {
            width: 80px;
            min-width: 80px;
            text-align: right;
        }
        
        /* 累计分红列宽度 */
        .stock-table th:nth-child(24),
        .stock-table td:nth-child(24) {
            width: 120px;
            min-width: 120px;
            text-align: right;
        }
        
        /* 排序指示器样式 */
        .sort-indicator {
            font-size: 0.8rem;
            margin-left: 5px;
            transition: transform 0.2s;
        }
        
        /* 页脚样式 */
        .footer {
            margin-top: 30px;
            padding: 20px;
            background-color: #f5f7fa;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            font-size: 14px;
            color: #666;
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .footer a {
            color: #3498db;
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        /* 调整表格宽度和行间距 */
        .stock-table {
            width: 100%;
            border-collapse: collapse;
            overflow-x: auto;
            display: block;
            max-height: 700px;
            overflow-y: auto;
        }
        
        /* 调整行间距 */
        .stock-table tr {
            line-height: 1.3; /* 减小行高，使行间距更紧凑 */
        }
        
        /* 筛选条件样式 */
        .filter-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            align-items: center;
            padding: 10px 0;
        }
        
        .filter-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .filter-item label {
            font-weight: 600;
            color: #34495e;
        }
        
        .filter-item input {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            width: 120px;
        }
        
        .filter-actions {
            display: flex;
            gap: 10px;
        }
        
        .filter-actions button {
            padding: 8px 16px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
        }
        
        .filter-actions button:hover {
            background-color: #2980b9;
        }
        
        .filter-actions button:active {
            background-color: #21618c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>股票股息率排名 (2020-2025)</h1>
        <div class="header-info">
            <p>共包含 <strong>{total_stocks}</strong> 只股票，数据来源：Baostock API</p>
            <p>按2020-2025年平均股息率降序排列，点击表头可排序</p>
        </div>
        
        <div class="section" style="background-color: #e3f2fd; border-radius: 5px;">
            <h2>使用说明</h2>
            <ul>
                <li>点击表头可按对应列进行排序，再次点击可切换排序方向</li>
                <li>表格支持横向滚动，方便查看完整数据</li>
                <li>股票代码和名称列固定，方便浏览时参考</li>
                <li>股息率以百分比形式显示，颜色标识为绿色</li>
                <li>收盘价以红色显示，方便区分不同数据类型</li>
            </ul>
        </div>
        
        <div class="section" style="background-color: #e3f2fd; border-radius: 5px;">
            <h2>筛选条件</h2>
            <div class="filter-container">
                <div class="filter-item">
                    <label for="avgYieldFilter">2020-2025年平均股息率 > </label>
                    <input type="number" id="avgYieldFilter" placeholder="例如: 5" step="0.1">
                </div>
                <div class="filter-item">
                    <label for="varianceFilter">最近6年股息率方差 < </label>
                    <input type="number" id="varianceFilter" placeholder="例如: 1.5" step="0.1">
                </div>
                <div class="filter-actions">
                    <button onclick="applyFilters()">应用筛选</button>
                    <button onclick="resetFilters()">重置</button>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>2020-2025年股息率对比</h2>
            <table class="stock-table comparison-table">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">排名 <span class="sort-indicator">▼</span></th>
                        <th onclick="sortTable(1)">股票名称 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(2)">股票代码 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(3)">2020-2025年平均股息率(%) <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(4)">最近6年股息率方差 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(5)">2025年分红 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(6)">2025年收盘价 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(7)">2025年股息率(%) <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(8)">2024年分红 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(9)">2024年收盘价 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(10)">2024年股息率(%) <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(11)">2023年分红 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(12)">2023年收盘价 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(13)">2023年股息率(%) <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(14)">2022年分红 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(15)">2022年收盘价 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(16)">2022年股息率(%) <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(17)">2021年分红 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(18)">2021年收盘价 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(19)">2021年股息率(%) <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(20)">2020年分红 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(21)">2020年收盘价 <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(22)">2020年股息率(%) <span class="sort-indicator"></span></th>
                        <th onclick="sortTable(23)">2020-2025年累计分红 <span class="sort-indicator"></span></th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # 添加股票数据行
    for i, stock in enumerate(stock_data, 1):
        html_content += f"""
                    <tr>
                        <td>{i}</td>
                        <td class="stock-info">{stock['股票名称']}</td>
                        <td class="stock-info">{stock['股票代码']}</td>
                        <td class="dividend-yield"><strong>{stock['2020-2025年平均股息率(%)']:.2f}%</strong></td>
                        <td>{stock['最近6年股息率方差']:.4f}</td>
                        <td>{stock['2025年分红']:.4f}</td>
                        <td class="price">{stock['2025年收盘价']:.2f}</td>
                        <td class="dividend-yield">{stock['2025年股息率(%)']:.2f}%</td>
                        <td>{stock['2024年分红']:.4f}</td>
                        <td class="price">{stock['2024年收盘价']:.2f}</td>
                        <td class="dividend-yield">{stock['2024年股息率(%)']:.2f}%</td>
                        <td>{stock['2023年分红']:.4f}</td>
                        <td class="price">{stock['2023年收盘价']:.2f}</td>
                        <td class="dividend-yield">{stock['2023年股息率(%)']:.2f}%</td>
                        <td>{stock['2022年分红']:.4f}</td>
                        <td class="price">{stock['2022年收盘价']:.2f}</td>
                        <td class="dividend-yield">{stock['2022年股息率(%)']:.2f}%</td>
                        <td>{stock['2021年分红']:.4f}</td>
                        <td class="price">{stock['2021年收盘价']:.2f}</td>
                        <td class="dividend-yield">{stock['2021年股息率(%)']:.2f}%</td>
                        <td>{stock['2020年分红']:.4f}</td>
                        <td class="price">{stock['2020年收盘价']:.2f}</td>
                        <td class="dividend-yield">{stock['2020年股息率(%)']:.2f}%</td>
                        <td>{stock['2020-2025年累计分红']:.4f}</td>
                    </tr>
"""
    
    # 生成HTML尾部，包含排序脚本
    html_content += """
                </tbody>
            </table>
        </div>
        
        <!-- 页脚信息 -->
        <footer class="footer">
            <div class="footer-content">
                <p>Author：Timo & TRAE</p>
                <p>GitHub：<a href="https://github.com/timoseven/dividend-ranker" target="_blank">https://github.com/timoseven/dividend-ranker</a></p>
            </div>
        </footer>
    </div>
    
    <script>
        let sortColumn = 3;
        let sortDirection = true; // true for ascending, false for descending
        
        function sortTable(n) {
            const table = document.querySelector('.stock-table');
            const tbody = table.getElementsByTagName('tbody')[0];
            const rows = Array.from(tbody.getElementsByTagName('tr'));
            const headers = table.getElementsByTagName('th');
            
            // Reset sort indicators
            for (let header of headers) {
                header.querySelector('.sort-indicator').textContent = '';
            }
            
            // Determine sort direction
            if (sortColumn === n) {
                sortDirection = !sortDirection;
            } else {
                sortDirection = true;
                sortColumn = n;
            }
            
            // Set sort indicator
            const indicator = headers[n].querySelector('.sort-indicator');
            indicator.textContent = sortDirection ? '▼' : '▲';
            
            // Sort rows
            rows.sort((a, b) => {
                const aVal = a.cells[n].textContent;
                const bVal = b.cells[n].textContent;
                
                // Handle numeric values (remove % sign if present)
                const aNum = parseFloat(aVal.replace('%', ''));
                const bNum = parseFloat(bVal.replace('%', ''));
                
                if (!isNaN(aNum) && !isNaN(bNum) && isFinite(aNum) && isFinite(bNum)) {
                    return sortDirection 
                        ? aNum - bNum
                        : bNum - aNum;
                } else {
                    // Handle text values
                    return sortDirection 
                        ? aVal.localeCompare(bVal, 'zh-CN')
                        : bVal.localeCompare(aVal, 'zh-CN');
                }
            });
            
            // Update row indices for rank column
            rows.forEach((row, index) => {
                row.cells[0].textContent = index + 1;
            });
            
            // Append sorted rows back to tbody
            rows.forEach(row => tbody.appendChild(row));
        }
        
        // 应用筛选条件
        function applyFilters() {
            const table = document.querySelector('.stock-table');
            const tbody = table.getElementsByTagName('tbody')[0];
            const rows = Array.from(tbody.getElementsByTagName('tr'));
            
            // 获取筛选条件
            const avgYieldFilter = parseFloat(document.getElementById('avgYieldFilter').value);
            const varianceFilter = parseFloat(document.getElementById('varianceFilter').value);
            
            let visibleCount = 0;
            
            // 遍历所有行
            rows.forEach(row => {
                const avgYieldCell = row.cells[3];
                const varianceCell = row.cells[4];
                
                // 获取数值
                const avgYield = parseFloat(avgYieldCell.textContent.replace('%', ''));
                const variance = parseFloat(varianceCell.textContent);
                
                // 检查是否符合筛选条件
                const meetsAvgYield = isNaN(avgYieldFilter) || avgYield > avgYieldFilter;
                const meetsVariance = isNaN(varianceFilter) || variance < varianceFilter;
                
                if (meetsAvgYield && meetsVariance) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            // 更新排名列
            updateRanks();
            
            // 显示筛选结果数量
            const headerInfo = document.querySelector('.header-info');
            const existingCount = headerInfo.querySelector('.filter-count');
            if (existingCount) {
                existingCount.textContent = `，筛选后显示${visibleCount}只股票`;
            } else {
                const countSpan = document.createElement('span');
                countSpan.className = 'filter-count';
                countSpan.textContent = `，筛选后显示${visibleCount}只股票`;
                headerInfo.lastElementChild.appendChild(countSpan);
            }
        }
        
        // 重置筛选条件
        function resetFilters() {
            // 清除输入
            document.getElementById('avgYieldFilter').value = '';
            document.getElementById('varianceFilter').value = '';
            
            // 显示所有行
            const table = document.querySelector('.stock-table');
            const tbody = table.getElementsByTagName('tbody')[0];
            const rows = Array.from(tbody.getElementsByTagName('tr'));
            
            rows.forEach(row => {
                row.style.display = '';
            });
            
            // 更新排名列
            updateRanks();
            
            // 清除筛选结果数量
            const headerInfo = document.querySelector('.header-info');
            const existingCount = headerInfo.querySelector('.filter-count');
            if (existingCount) {
                existingCount.remove();
            }
        }
        
        // 更新排名列
        function updateRanks() {
            const table = document.querySelector('.stock-table');
            const tbody = table.getElementsByTagName('tbody')[0];
            const rows = Array.from(tbody.getElementsByTagName('tr'));
            
            let rank = 1;
            rows.forEach(row => {
                if (row.style.display !== 'none') {
                    row.cells[0].textContent = rank++;
                }
            });
        }
        
        // Initial sort
        sortTable(3);
    </script>
</body>
</html>"""
    
    # 写入HTML文件
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content.replace("{total_stocks}", str(len(stock_data))))
    
    print(f"HTML文件已生成: {output_html}")
    return True

if __name__ == "__main__":
    generate_complete_html()
