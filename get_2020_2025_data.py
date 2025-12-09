#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据stocks.id获取2020年到2025年的数据并生成CSV文件
"""

import os
import time
import random
import csv
import baostock as bs

class YearlyDataCollector:
    def __init__(self):
        self.baostock = None
        self.stocks_id_file = "stocks.id"
        self.output_csv = "output/2020_2025_dividend_data.csv"
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
        """从stocks.id文件中获取股票列表"""
        stock_list = []
        with open(self.stocks_id_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    stock_code, stock_name = line.split(maxsplit=1)
                    stock_list.append((stock_code, stock_name))
        print(f"共读取到{len(stock_list)}只股票")
        return stock_list
    
    def get_yearly_dividend(self, code, year):
        """获取单只股票单年度的分红金额"""
        total_dividend = 0.0
        
        rs = self.baostock.query_dividend_data(
            code=code,
            year=year,
            yearType="report"
        )
        
        if rs.error_code != '0':
            # print(f"  获取{code} {year}年分红数据失败: {rs.error_msg}")
            return total_dividend
        
        while rs.next():
            row = rs.get_row_data()
            if len(row) >= 10:
                dividend = row[9]
                if dividend and dividend != '' and dividend != '0':
                    try:
                        per_share_dividend = float(dividend)
                        total_dividend += per_share_dividend
                    except (ValueError, TypeError):
                        continue
        
        return total_dividend
    
    def get_yearly_close_price(self, code, year):
        """获取单只股票单年度最后一个交易日的收盘价"""
        # 构建查询日期范围
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        rs = self.baostock.query_history_k_data_plus(
            code=code,
            fields="date,close",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"  # 3表示不复权
        )
        
        if rs.error_code != '0':
            # print(f"  获取{code} {year}年收盘价数据失败: {rs.error_msg}")
            return None
        
        close_price = None
        while rs.next():
            row = rs.get_row_data()
            close_price = float(row[1])
        
        return close_price
    
    def get_yearly_profit(self, code, year):
        """获取单只股票单年度的净利润数据"""
        # 使用baostock的query_profit_data方法获取利润表数据
        try:
            # 查询利润表数据（使用年报，第四季度）
            rs = self.baostock.query_profit_data(
                code=code,
                year=year,
                quarter=4
            )
            
            if rs.error_code == '0':
                while rs.next():
                    row = rs.get_row_data()
                    fields = rs.fields
                    
                    # 查找netProfit字段的索引
                    if 'netProfit' in fields:
                        net_profit_index = fields.index('netProfit')
                        if net_profit_index < len(row):
                            net_profit_val = row[net_profit_index]
                            if net_profit_val and net_profit_val != '' and net_profit_val != '0':
                                try:
                                    # netProfit字段值的单位是元，需要转换为亿元
                                    # 1亿元 = 100,000,000元
                                    profit = float(net_profit_val) / 100000000
                                    return round(profit, 4)
                                except (ValueError, TypeError):
                                    continue
            
            # 如果年报数据获取失败，尝试获取第三季度数据
            rs = self.baostock.query_profit_data(
                code=code,
                year=year,
                quarter=3
            )
            
            if rs.error_code == '0':
                while rs.next():
                    row = rs.get_row_data()
                    fields = rs.fields
                    
                    if 'netProfit' in fields:
                        net_profit_index = fields.index('netProfit')
                        if net_profit_index < len(row):
                            net_profit_val = row[net_profit_index]
                            if net_profit_val and net_profit_val != '' and net_profit_val != '0':
                                try:
                                    # netProfit字段值的单位是元，转换为亿元
                                    profit = float(net_profit_val) / 100000000
                                    return round(profit, 4)
                                except (ValueError, TypeError):
                                    continue
        except Exception as e:
            # 打印详细错误信息以便调试
            # print(f"  获取{code} {year}年利润数据异常: {e}")
            pass
        
        # 如果所有方法都失败，返回默认值0
        return 0.0
    
    def collect_yearly_data(self):
        """收集2020-2025年的数据"""
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
                # 获取分红
                dividend = self.get_yearly_dividend(code, year)
                yearly_data[f"{year}年分红"] = round(dividend, 4)
                
                # 获取收盘价
                close_price = self.get_yearly_close_price(code, year)
                yearly_data[f"{year}年收盘价"] = close_price if close_price is not None else 0.0
                
                # 计算股息率
                if close_price and close_price > 0:
                    dividend_yield = (dividend / close_price) * 100
                    yearly_data[f"{year}年股息率(%)"] = round(dividend_yield, 2)
                else:
                    yearly_data[f"{year}年股息率(%)"] = 0.0
                
                # 获取利润
                profit = self.get_yearly_profit(code, year)
                yearly_data[f"{year}年利润(亿元)"] = round(profit, 4)
            
            # 计算2020-2025年累计分红和平均股息率
            total_dividend = sum(yearly_data[f"{year}年分红"] for year in self.years)
            valid_yields = [yearly_data[f"{year}年股息率(%)"] for year in self.years if yearly_data[f"{year}年股息率(%)"] > 0]
            avg_yield = sum(valid_yields) / len(valid_yields) if valid_yields else 0.0
            
            # 计算2020-2025年平均利润
            total_profit = sum(yearly_data[f"{year}年利润(亿元)"] for year in self.years)
            avg_profit = total_profit / len(self.years)
            
            yearly_data["2020-2025年累计分红"] = round(total_dividend, 4)
            yearly_data["2020-2025年平均股息率(%)"] = round(avg_yield, 2)
            yearly_data["2020-2025年平均利润(亿元)"] = round(avg_profit, 4)
            
            all_data.append(yearly_data)
            
            # 随机休眠，避免API调用过于频繁
            time.sleep(random.uniform(0.3, 1.0))
        
        return all_data
    
    def save_to_csv(self, data):
        """保存数据到CSV文件"""
        if not data:
            print("没有数据可保存")
            return False
        
        # 构建字段名
        fields = ["股票代码", "股票名称"]
        for year in self.years:
            fields.extend([f"{year}年分红", f"{year}年收盘价", f"{year}年股息率(%)", f"{year}年利润(亿元)"])
        fields.extend(["2020-2025年累计分红", "2020-2025年平均股息率(%)", "2020-2025年平均利润(亿元)"])
        
        # 保存到CSV
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        
        print(f"已将{len(data)}只股票的2020-2025年数据保存到: {self.output_csv}")
        return True
    
    def run(self):
        """运行数据收集流程"""
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
    collector = YearlyDataCollector()
    collector.run()
