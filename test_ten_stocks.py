#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试前十个股票的净利润数据获取
"""

import os
import time
import random
import csv
import baostock as bs

class TestTenStocks:
    def __init__(self):
        self.baostock = None
        self.stocks_id_file = "stocks.id"
        self.output_csv = "output/test_ten_stocks.csv"
        self.years = [2020, 2021, 2022, 2023, 2024, 2025]
        
    def init_baostock(self):
        """初始化Baostock API"""
        login_result = bs.login()
        if login_result.error_code != '0':
            print(f"Baostock登录失败: {login_result.error_msg}")
            return False
        print("Baostock登录成功")
        self.baostock = bs
        return True
    
    def get_stock_list(self):
        """从stocks.id文件中获取前十个股票"""
        stock_list = []
        with open(self.stocks_id_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= 10:  # 只取前10个
                    break
                line = line.strip()
                if line:
                    stock_code, stock_name = line.split(maxsplit=1)
                    stock_list.append((stock_code, stock_name))
        print(f"共读取到{len(stock_list)}只股票")
        return stock_list
    
    def get_yearly_profit(self, code, year):
        """获取单只股票单年度的净利润数据"""
        # 使用baostock的query_profit_data方法获取利润表数据
        try:
            # 查询利润表数据
            rs = self.baostock.query_profit_data(
                code=code,
                year=year,
                quarter=4
            )
            
            if rs.error_code == '0':
                while rs.next():
                    row = rs.get_row_data()
                    # 打印所有字段，查看包含哪些数据
                    print(f"{code} {year}年利润表数据: {row}")
                    print(f"字段名: {rs.fields}")
                    
                    # 查找netProfit相关字段
                    for i, field in enumerate(rs.fields):
                        if 'netprofit' in field.lower() or '净利润' in field:
                            print(f"找到净利润字段: {field} = {row[i]}")
                            if row[i] and row[i] != '' and row[i] != '0':
                                try:
                                    # 净利润单位是万元，转换为亿元
                                    return float(row[i]) / 10000
                                except (ValueError, TypeError):
                                    continue
        except Exception as e:
            print(f"  获取{code} {year}年利润数据异常: {e}")
        
        return 0.0
    
    def collect_yearly_data(self):
        """收集前10只股票2020-2025年的数据"""
        stock_list = self.get_stock_list()
        if not stock_list:
            return []
        
        all_data = []
        
        for i, (code, name) in enumerate(stock_list):
            print(f"正在处理第{i+1}/{len(stock_list)}只股票: {code} {name}")
            
            # 收集每年的数据
            yearly_data = {
                "股票代码": code,
                "股票名称": name
            }
            
            for year in self.years:
                # 只获取利润数据进行测试
                profit = self.get_yearly_profit(code, year)
                yearly_data[f"{year}年利润(亿元)"] = round(profit, 4)
                
                # 休眠一下，避免API调用过于频繁
                time.sleep(0.5)
            
            all_data.append(yearly_data)
        
        return all_data
    
    def save_to_csv(self, data):
        """保存数据到CSV文件"""
        if not data:
            print("没有数据可保存")
            return False
        
        # 构建字段名
        fields = ["股票代码", "股票名称"]
        for year in self.years:
            fields.append(f"{year}年利润(亿元)")
        
        # 保存到CSV
        os.makedirs("output", exist_ok=True)
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        
        print(f"已将{len(data)}只股票的数据保存到: {self.output_csv}")
        return True
    
    def run(self):
        """运行测试"""
        try:
            if not self.init_baostock():
                return False
            
            # 收集数据
            data = self.collect_yearly_data()
            
            # 保存到CSV
            if data:
                self.save_to_csv(data)
            
            return True
            
        finally:
            # 登出Baostock
            if self.baostock:
                bs.logout()
                print("Baostock已退出")

if __name__ == "__main__":
    tester = TestTenStocks()
    tester.run()