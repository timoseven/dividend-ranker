#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股息率排名生成器
从2020年到2025年，每年最高股息率前100名股票
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import re
from bs4 import BeautifulSoup

class DividendYieldRanker:
    def __init__(self):
        self.base_url = "http://quotes.money.163.com"
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def get_trading_days(self, year):
        """获取指定年份的第一个交易日"""
        # 使用新浪财经API获取交易日历
        url = f"https://money.finance.sina.com.cn/corp/go.php/vIR_Calendar/getAjaxData.php?year={year}"
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = response.json()
            trading_days = [date for date, status in data.items() if status == '0']
            if trading_days:
                # 返回第一个交易日，格式为YYYY-MM-DD
                first_trading_day = sorted(trading_days)[0]
                return first_trading_day
            else:
                # 如果没有数据，返回1月1日
                return f"{year}-01-01"
        except Exception as e:
            print(f"获取{year}年交易日历失败: {e}")
            return f"{year}-01-01"
    
    def get_stock_list(self):
        """获取沪深两市所有股票列表"""
        stock_list = []
        # 上海A股
        sh_url = f"{self.base_url}/service/stock_list.html?type=SH"
        # 深圳A股
        sz_url = f"{self.base_url}/service/stock_list.html?type=SZ"
        
        for url in [sh_url, sz_url]:
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                response.encoding = 'gb2312'
                html = response.text
                
                # 使用正则表达式提取股票代码和名称
                pattern = r'<li><a href="http://quotes\.money\.163\.com/(\d+)\.html" target="_blank">(.*?)</a></li>'
                matches = re.findall(pattern, html)
                
                for code, name in matches:
                    stock_list.append((code, name))
            except Exception as e:
                print(f"获取股票列表失败: {e}")
        
        return stock_list
    
    def get_stock_price(self, code, date):
        """获取指定日期的股票收盘价"""
        # 使用东方财富网API获取历史数据
        url = f"https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.{code}&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=1&end={date.replace('-', '')}&lmt=1"
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = response.json()
            if data['data'] and data['data']['klines']:
                kline = data['data']['klines'][0].split(',')
                # 收盘价是第5个字段
                close_price = float(kline[4])
                return close_price
            else:
                return None
        except Exception as e:
            print(f"获取股票{code}在{date}的价格失败: {e}")
            return None
    
    def get_dividend_data(self, code, year):
        """获取指定股票在指定年份的分红数据"""
        # 使用东方财富网分红扩股数据
        url = f"https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/ShareholderResearchAjax?code=sh{code}&type=5&year={year}"
        if code.startswith('0') or code.startswith('3'):
            url = f"https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/ShareholderResearchAjax?code=sz{code}&type=5&year={year}"
        
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = response.json()
            
            if data and data['Result'] and data['Result']['分红送配']:
                dividend_data = data['Result']['分红送配']
                # 计算总现金分红
                total_dividend = 0.0
                for item in dividend_data:
                    if '派息' in item['方案']:
                        # 提取派息金额
                        pattern = r'派([0-9.]+)元'
                        match = re.search(pattern, item['方案'])
                        if match:
                            total_dividend += float(match.group(1))
                
                return total_dividend
            else:
                return 0.0
        except Exception as e:
            print(f"获取股票{code}在{year}的分红数据失败: {e}")
            return 0.0
    
    def calculate_dividend_yield(self, code, name, year):
        """计算指定股票在指定年份的股息率"""
        # 获取当年第一个交易日
        first_trading_day = self.get_trading_days(year)
        
        # 获取该交易日的收盘价
        price = self.get_stock_price(code, first_trading_day)
        if price is None:
            return None
        
        # 获取当年分红金额
        dividend = self.get_dividend_data(code, year)
        
        # 计算股息率
        if price > 0:
            dividend_yield = (dividend / price) * 100
            return {
                'code': code,
                'name': name,
                'year': year,
                'price': round(price, 2),
                'dividend': round(dividend, 2),
                'dividend_yield': round(dividend_yield, 2),
                'first_trading_day': first_trading_day
            }
        else:
            return None
    
    def generate_rankings(self, start_year=2020, end_year=2025):
        """生成指定年份范围的股息率排名"""
        # 获取股票列表
        print("正在获取股票列表...")
        stock_list = self.get_stock_list()
        print(f"共获取到{len(stock_list)}只股票")
        
        all_rankings = {}
        
        for year in range(start_year, end_year + 1):
            print(f"\n正在处理{year}年数据...")
            year_data = []
            
            for i, (code, name) in enumerate(stock_list):
                if i % 100 == 0:
                    print(f"已处理{year}年第{i}/{len(stock_list)}只股票")
                
                # 计算股息率
                result = self.calculate_dividend_yield(code, name, year)
                if result:
                    year_data.append(result)
            
            # 按股息率降序排序
            year_data.sort(key=lambda x: x['dividend_yield'], reverse=True)
            
            # 取前100名
            all_rankings[year] = year_data[:100]
            
            # 保存当年数据
            df = pd.DataFrame(year_data[:100])
            df.to_csv(f"{self.data_dir}/{year}_dividend_rankings.csv", index=False, encoding='utf-8-sig')
            print(f"{year}年数据已保存到{self.data_dir}/{year}_dividend_rankings.csv")
        
        return all_rankings
    
    def generate_html(self, rankings):
        """生成HTML页面"""
        years = sorted(rankings.keys())
        
        # 使用普通字符串模板，避免f-string大括号冲突
        html_template = '''
        <!DOCTYPE html>
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
                    统计范围：2020年 - 2025年 | 数据来源：东方财富网、网易财经 | 股票价格：统计当年第一个交易日收盘价
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-value">{year_count}</div>
                        <div class="stat-label">统计年份</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">100</div>
                        <div class="stat-label">每年上榜股票数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{start_year}-{end_year}</div>
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
        </html>
        '''
        
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
        
        # 替换模板中的变量
        html = html_template.format(
            year_count=len(years),
            start_year=years[0],
            end_year=years[-1],
            year_tabs=year_tabs,
            year_contents=year_contents
        )
        
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
