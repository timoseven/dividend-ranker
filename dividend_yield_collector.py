#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Baostock API获取2025年所有沪深股市股票的股息率
股息率大于3%的股票保存为CSV文件
"""

import os
import csv
import time
import random

class DividendYieldCollector:
    def __init__(self):
        self.baostock = None
        self.stock_list = []
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def init_baostock(self):
        """初始化Baostock API"""
        import baostock as bs
        self.baostock = bs
        
        login_result = bs.login()
        if login_result.error_code != '0':
            print(f"Baostock登录失败: {login_result.error_msg}")
            return False
        print("Baostock登录成功")
        return True
    
    def get_stock_list(self):
        """获取所有沪深股市股票列表"""
        print("正在获取股票列表...")
        
        rs = self.baostock.query_stock_basic()
        if rs.error_code != '0':
            print(f"获取股票列表失败: {rs.error_msg}")
            return False
        
        stock_list = []
        while rs.next():
            row = rs.get_row_data()
            code = row[0]  # 股票代码，如sh.600000
            name = row[1]  # 股票名称
            stock_type = row[4]  # 类型：1为股票，2为指数，3为ETF等
            status = row[5]  # 上市状态：1为上市，0为退市
            
            # 只保留沪深股市的上市股票（类型为1，状态为1）
            if code.startswith(('sh.', 'sz.')) and stock_type == '1' and status == '1':
                stock_list.append((code, name))
        
        self.stock_list = stock_list
        print(f"共获取到{len(stock_list)}只上市股票")
        return True
    
    def get_2025_dividends(self, code):
        """获取股票2025年的累计分红金额"""
        total_dividend = 0.0
        
        # 使用Baostock的分红数据查询接口
        rs = self.baostock.query_dividend_data(
            code=code,
            year=2025,
            yearType="report"
        )
        
        if rs.error_code != '0':
            # print(f"获取{code}分红数据失败: {rs.error_msg}")
            return total_dividend
        
        while rs.next():
            row = rs.get_row_data()
            # row[9]是10派x元的x值
            if len(row) >= 10:
                dividend = row[9]
                if dividend and dividend != '' and dividend != '0':
                    try:
                        # dividCashPsBeforeTax字段直接是每股税前分红，不需要再除以10
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
            return None
        
        if rs.next():
            row = rs.get_row_data()
            return row[0] if row[0] and row[0] != '' else None
        return None
    
    def calculate_dividend_yield(self):
        """计算所有股票的股息率，保存所有股票数据"""
        results = []
        
        for i, (code, name) in enumerate(self.stock_list):
            print(f"正在处理第{i+1}/{len(self.stock_list)}只股票: {code} {name}")
            
            try:
                # 获取2025年累计分红
                total_dividend = self.get_2025_dividends(code)
                
                # 获取2025年11月28日收盘价
                close_price = self.get_2025_close_price(code)
                
                if close_price and float(close_price) > 0:
                    # 计算股息率：(累计分红 / 收盘价) * 100%
                    dividend_yield = (total_dividend / float(close_price)) * 100
                    
                    # 添加日志
                    print(f"  2025年累计分红: {total_dividend:.4f}, 2025-11-28收盘价: {close_price}, 股息率: {dividend_yield:.2f}%")
                    
                    # 保存所有股票，不设过滤条件
                    results.append({
                        "股票代码": code,
                        "股票名称": name,
                        "2025年累计分红": round(total_dividend, 4),
                        "2025-11-28收盘价": float(close_price),
                        "股息率(%)": round(dividend_yield, 2)
                    })
                else:
                    print(f"  收盘价数据缺失或为0: {close_price}")
                    # 即使收盘价缺失，也保存股票信息，股息率设为0
                    results.append({
                        "股票代码": code,
                        "股票名称": name,
                        "2025年累计分红": round(total_dividend, 4),
                        "2025-11-28收盘价": 0.0,
                        "股息率(%)": 0.0
                    })
                
                # 每处理100只股票，保存一次中间结果
                if (i + 1) % 100 == 0:
                    self.save_to_csv(results, f"all_dividend_yield_2025_temp.csv")
                    print(f"  已保存中间结果，共{len(results)}条数据")
                
                # 随机休眠，避免API调用过于频繁
                time.sleep(random.uniform(0.3, 1.0))
                
            except Exception as e:
                print(f"处理{code}时出错: {e}")
                continue
        
        return results
    
    def save_to_csv(self, data, output_path="all_dividend_yield_2025.csv"):
        """将结果保存为CSV文件"""
        csv_path = os.path.join(self.output_dir, output_path)
        
        if not data:
            print("没有股票数据")
            return False
        
        # 获取字段名
        fieldnames = list(data[0].keys())
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        
        print(f"已将{len(data)}只股票的股息率数据保存到{csv_path}")
        return True
    
    def close_baostock(self):
        """关闭Baostock API"""
        if self.baostock:
            self.baostock.logout()
            print("Baostock已退出")
    
    def run(self):
        """运行数据收集流程"""
        try:
            if not self.init_baostock():
                return
            
            if not self.get_stock_list():
                return
            
            results = self.calculate_dividend_yield()
            self.save_to_csv(results)
            
        finally:
            self.close_baostock()

if __name__ == "__main__":
    collector = DividendYieldCollector()
    collector.run()
