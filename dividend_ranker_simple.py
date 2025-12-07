#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股息率排名生成器（简化版 - 使用模拟数据）
从2020年到2025年，每年最高股息率前100名股票
"""

import random
import os
from datetime import datetime

class DividendYieldRanker:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def generate_mock_data(self, year):
        """生成指定年份的模拟数据"""
        # 生成100只模拟股票数据
        mock_data = []
        for i in range(100):
            # 生成股票代码
            if random.random() < 0.5:
                # 上海股票
                code = f"600{i:03d}"
            else:
                # 深圳股票
                code = f"000{i:03d}"
            
            # 模拟股票名称
            name = f"模拟股票{i+1}"
            
            # 模拟价格（1-200元）
            price = round(random.uniform(1, 200), 2)
            
            # 模拟股息率（0-10%）
            dividend_yield = round(random.uniform(3, 10), 2)
            
            # 计算分红金额
            dividend = round(price * (dividend_yield / 100), 2)
            
            # 模拟当年第一个交易日
            first_trading_day = f"{year}-01-02" if year != 2025 else f"{year}-01-02"
            
            mock_data.append({
                'code': code,
                'name': name,
                'year': year,
                'price': price,
                'dividend': dividend,
                'dividend_yield': dividend_yield,
                'first_trading_day': first_trading_day
            })
        
        # 按股息率降序排序
        mock_data.sort(key=lambda x: x['dividend_yield'], reverse=True)
        
        return mock_data
    
    def generate_rankings(self, start_year=2020, end_year=2025):
        """生成指定年份范围的股息率排名"""
        all_rankings = {}
        
        for year in range(start_year, end_year + 1):
            print(f"正在生成{year}年模拟数据...")
            
            # 生成模拟数据
            year_data = self.generate_mock_data(year)
            all_rankings[year] = year_data
            
            # 保存当年数据
            with open(f"{self.data_dir}/{year}_dividend_rankings.csv", "w", encoding="utf-8-sig") as f:
                # 写入表头
                f.write("code,name,year,price,dividend,dividend_yield,first_trading_day\n")
                # 写入数据
                for item in year_data:
                    f.write(f"{item['code']},{item['name']},{item['year']},{item['price']},{item['dividend']},{item['dividend_yield']},{item['first_trading_day']}\n")
            
            print(f"{year}年数据已保存到{self.data_dir}/{year}_dividend_rankings.csv")
        
        return all_rankings
    
    def generate_html(self, rankings):
        """生成HTML页面"""
        years = sorted(rankings.keys())
        
        # 生成年份标签
        year_tabs = ''
        for year in years:
            active_class = 'active' if year == years[0] else ''
            year_tabs += f'''                    <button class="year-tab {active_class}" 
                            onclick="showYearContent({year})">
                        {year}年
                    </button>\n'''
        
        # 生成年份内容
        year_contents = ''
        for year in years:
            year_data = rankings[year]
            active_class = 'active' if year == years[0] else ''
            
            year_content = f'''                    <div id="year-{year}" class="year-content {active_class}">
                        <table class="stock-table">
                            <thead>
                                <tr>
                                    <th>排名</th>
                                    <th>股票代码</th>
                                    <th>股票名称</th>
                                    <th>当年第一个交易日</th>
                                    <th>收盘价 (元)</th>
                                    <th>现金分红 (元/股)</th>
                                    <th>股息率 (%)</th>
                                </tr>
                            </thead>
                            <tbody>\n'''
            
            for i, stock in enumerate(year_data):
                year_content += f'''                                <tr>
                                    <td>{i+1}</td>
                                    <td class="stock-info">{stock['code']}</td>
                                    <td>{stock['name']}</td>
                                    <td>{stock['first_trading_day']}</td>
                                    <td class="price">{stock['price']}</td>
                                    <td>{stock['dividend']}</td>
                                    <td class="dividend-yield">{stock['dividend_yield']}</td>
                                </tr>\n'''
            
            year_content += '''                            </tbody>
                        </table>
                    </div>\n'''
            year_contents += year_content
        
        # 直接构建HTML字符串，避免使用format方法
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>沪深股市股息率排名 (2020-2025)</title>
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
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
            font-size: 2.5rem;
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
            font-size: 1.8rem;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        
        .year-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            overflow-x: auto;
            padding-bottom: 10px;
        }
        
        .year-tab {
            padding: 10px 20px;
            background: #ecf0f1;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            white-space: nowrap;
        }
        
        .year-tab:hover {
            background: #3498db;
            color: white;
        }
        
        .year-tab.active {
            background: #3498db;
            color: white;
            box-shadow: 0 2px 5px rgba(52, 152, 219, 0.3);
        }
        
        .stock-table {
            width: 100%;
            border-collapse: collapse;
            overflow-x: auto;
            display: block;
        }
        
        .stock-table th,
        .stock-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .stock-table th {
            background: #3498db;
            color: white;
            font-weight: 600;
            position: sticky;
            top: 0;
        }
        
        .stock-table tr:hover {
            background: #f8f9fa;
        }
        
        .stock-table tr:nth-child(even) {
            background: #f5f7fa;
        }
        
        .stock-table tr:nth-child(even):hover {
            background: #e9ecef;
        }
        
        .stock-info {
            font-weight: 600;
            color: #2c3e50;
        }
        
        .dividend-yield {
            color: #27ae60;
            font-weight: 600;
        }
        
        .price {
            color: #e74c3c;
        }
        
        .year-content {
            display: none;
        }
        
        .year-content.active {
            display: block;
        }
        
        .header-info {
            text-align: center;
            margin-bottom: 20px;
            color: #666;
            font-size: 1.1rem;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            flex: 1;
            min-width: 200px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }
            
            h2 {
                font-size: 1.5rem;
            }
            
            .stock-table {
                font-size: 0.9rem;
            }
            
            .stock-table th,
            .stock-table td {
                padding: 8px;
            }
            
            .year-tab {
                padding: 8px 15px;
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>沪深股市股息率排名</h1>
        <div class="header-info">
            统计范围：2020年 - 2025年 | 数据类型：模拟数据 | 股票价格：统计当年第一个交易日收盘价
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{len(years)}</div>
                <div class="stat-label">统计年份</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">100</div>
                <div class="stat-label">每年上榜股票数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{years[0]}-{years[-1]}</div>
                <div class="stat-label">统计区间</div>
            </div>
        </div>
        
        <div class="section">
            <h2>每年最高股息率前100名股票</h2>
            <div class="year-tabs">
{year_tabs}
            </div>
            
{year_contents}
        </div>
    </div>
    
    <script>
        function showYearContent(year) {
            // Hide all year contents
            document.querySelectorAll('.year-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.year-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected year content
            document.getElementById(`year-${year}`).classList.add('active');
            
            // Add active class to selected tab
            event.target.classList.add('active');
        }
    </script>
</body>
</html>'''
        
        # 保存HTML文件
        with open("dividend_rankings.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"\nHTML页面已生成: dividend_rankings.html")
        return html

def main():
    """主函数"""
    ranker = DividendYieldRanker()
    
    # 生成2020-2025年的股息率排名
    rankings = ranker.generate_rankings()
    
    # 生成HTML页面
    ranker.generate_html(rankings)
    
    print("\n任务完成！")

if __name__ == "__main__":
    main()
