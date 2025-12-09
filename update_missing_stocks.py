#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新sz.301528到sz.302132范围内的缺失股票数据
"""

import os
import csv
import time
import random
import baostock as bs

class MissingStockUpdater:
    def __init__(self):
        self.baostock = None
        self.input_csv = "output/all_dividend_yield_2025.csv"
        self.output_csv = "output/all_dividend_yield_2025_updated.csv"
        self.target_range = ("sz.301528", "sz.302132")
        
    def init_baostock(self):
        """初始化Baostock API"""
        login_result = bs.login()
        if login_result.error_code != '0':
            print(f"Baostock登录失败: {login_result.error_msg}")
            return False
        print("Baostock登录成功")
        self.baostock = bs
        return True
    
    def get_target_stocks(self):
        """从CSV文件中获取目标范围内的股票"""
        target_stocks = []
        
        if not os.path.exists(self.input_csv):
            print(f"输入文件不存在: {self.input_csv}")
            return target_stocks
        
        with open(self.input_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row["股票代码"]
                # 检查是否在目标范围内
                if self.target_range[0] <= code <= self.target_range[1]:
                    target_stocks.append({
                        "股票代码": code,
                        "股票名称": row["股票名称"]
                    })
        
        print(f"共找到{len(target_stocks)}只目标股票")
        return target_stocks
    
    def get_2025_dividends(self, code):
        """获取股票2025年的累计分红金额"""
        total_dividend = 0.0
        
        rs = self.baostock.query_dividend_data(
            code=code,
            year=2025,
            yearType="report"
        )
        
        if rs.error_code != '0':
            print(f"  获取{code}分红数据失败: {rs.error_msg}")
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
    
    def get_2025_close_price(self, code):
        """获取股票2025年11月28日的收盘价"""
        rs = self.baostock.query_history_k_data_plus(
            code=code,
            fields="close",
            start_date="2025-11-28",
            end_date="2025-11-28",
            frequency="d",
            adjustflag="3"
        )
        
        if rs.error_code != '0':
            print(f"  获取{code}收盘价失败: {rs.error_msg}")
            return None
        
        if rs.next():
            row = rs.get_row_data()
            return row[0] if row[0] and row[0] != '' else None
        return None
    
    def update_stock_data(self, target_stocks):
        """更新目标股票的数据"""
        updated_data = {}
        
        for i, stock in enumerate(target_stocks):
            code = stock["股票代码"]
            name = stock["股票名称"]
            print(f"正在处理第{i+1}/{len(target_stocks)}只股票: {code} {name}")
            
            try:
                # 获取2025年累计分红
                total_dividend = self.get_2025_dividends(code)
                
                # 获取2025年11月28日收盘价
                close_price = self.get_2025_close_price(code)
                
                if close_price and float(close_price) > 0:
                    # 计算股息率
                    dividend_yield = (total_dividend / float(close_price)) * 100
                    
                    # 保存更新后的数据
                    updated_data[code] = {
                        "股票代码": code,
                        "股票名称": name,
                        "2025年累计分红": round(total_dividend, 4),
                        "2025-11-28收盘价": float(close_price),
                        "股息率(%)": round(dividend_yield, 2)
                    }
                    
                    print(f"  更新成功: 分红={total_dividend:.4f}, 收盘价={close_price}, 股息率={dividend_yield:.2f}%")
                else:
                    # 即使收盘价缺失，也要保存更新状态
                    updated_data[code] = {
                        "股票代码": code,
                        "股票名称": name,
                        "2025年累计分红": round(total_dividend, 4),
                        "2025-11-28收盘价": 0.0,
                        "股息率(%)": 0.0
                    }
                    
                    print(f"  更新成功: 分红={total_dividend:.4f}, 收盘价=0.0")
                
                # 随机休眠，避免API调用过于频繁
                time.sleep(random.uniform(0.3, 1.0))
                
            except Exception as e:
                print(f"  处理{code}时出错: {e}")
                continue
        
        return updated_data
    
    def update_csv_file(self, updated_data):
        """更新CSV文件"""
        if not os.path.exists(self.input_csv):
            print(f"输入文件不存在: {self.input_csv}")
            return False
        
        with open(self.input_csv, 'r', encoding='utf-8') as f_in, \
             open(self.output_csv, 'w', newline='', encoding='utf-8') as f_out:
            reader = csv.DictReader(f_in)
            writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
            writer.writeheader()
            
            # 遍历所有行，更新目标范围内的股票
            for row in reader:
                code = row["股票代码"]
                if code in updated_data:
                    # 使用更新后的数据
                    writer.writerow(updated_data[code])
                    print(f"已更新: {code}")
                else:
                    # 使用原始数据
                    writer.writerow(row)
        
        print(f"\nCSV文件更新完成，保存到: {self.output_csv}")
        
        # 替换原始文件
        os.replace(self.output_csv, self.input_csv)
        print(f"已替换原始文件: {self.input_csv}")
        return True
    
    def run(self):
        """运行更新流程"""
        try:
            if not self.init_baostock():
                return False
            
            # 获取目标股票
            target_stocks = self.get_target_stocks()
            if not target_stocks:
                return False
            
            # 更新股票数据
            updated_data = self.update_stock_data(target_stocks)
            
            # 更新CSV文件
            if updated_data:
                self.update_csv_file(updated_data)
            
            return True
            
        finally:
            # 登出Baostock
            if self.baostock:
                bs.logout()
                print("Baostock已退出")

if __name__ == "__main__":
    updater = MissingStockUpdater()
    updater.run()
