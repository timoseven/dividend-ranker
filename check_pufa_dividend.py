#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查浦发银行的分红数据，验证股息率计算是否正确
"""

import os

class PufaDividendChecker:
    def __init__(self):
        self.baostock = None
    
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
    
    def check_pufa_dividend(self):
        """检查浦发银行的分红数据"""
        code = "sh.600000"
        name = "浦发银行"
        
        print(f"=== 检查{name}({code})的分红数据 ===")
        
        # 查询2025年的分红数据
        rs = self.baostock.query_dividend_data(
            code=code,
            year=2025,
            yearType="report"
        )
        
        if rs.error_code != '0':
            print(f"获取分红数据失败: {rs.error_msg}")
            return
        
        print("\n2025年分红数据:")
        total_dividend = 0.0
        while rs.next():
            row = rs.get_row_data()
            print(f"\n分红记录: {row}")
            print(f"  分红日期: {row[2]}")
            print(f"  登记日期: {row[3]}")
            print(f"  除权除息日期: {row[4]}")
            print(f"  派息日期: {row[5]}")
            print(f"  每股分红: {row[9]}")
            print(f"  分红方案: {row[12]}")
            
            # 计算每股分红
            if len(row) >= 10:
                dividend = row[9]
                if dividend and dividend != '' and dividend != '0':
                    try:
                        # dividCashPsBeforeTax字段直接是每股税前分红，不需要再除以10
                        per_share_dividend = float(dividend)
                        total_dividend += per_share_dividend
                        print(f"  每股分红: {per_share_dividend}元")
                    except (ValueError, TypeError) as e:
                        print(f"  解析分红数据出错: {e}")
        
        print(f"\n2025年累计分红: {total_dividend:.4f}元/股")
        
        # 查询2025-11-28的收盘价
        rs = self.baostock.query_history_k_data_plus(
            code=code,
            fields="code,date,close",
            start_date="2025-11-28",
            end_date="2025-11-28",
            frequency="d",
            adjustflag="3"
        )
        
        if rs.error_code != '0':
            print(f"获取收盘价失败: {rs.error_msg}")
            return
        
        close_price = 0.0
        if rs.next():
            row = rs.get_row_data()
            print(f"\n2025-11-28收盘价数据: {row}")
            close_price = float(row[2])
            print(f"2025-11-28收盘价: {close_price}元")
        
        # 计算股息率
        if close_price > 0:
            dividend_yield = (total_dividend / close_price) * 100
            print(f"\n计算股息率: ({total_dividend} / {close_price}) * 100% = {dividend_yield:.2f}%")
        
        # 检查是否还有其他分红数据
        print("\n=== 检查历史分红数据 ===")
        rs = self.baostock.query_dividend_data(
            code=code,
            year=2024,
            yearType="report"
        )
        
        if rs.error_code == '0':
            print("2024年分红数据:")
            while rs.next():
                row = rs.get_row_data()
                print(f"  分红方案: {row[12]}")
                print(f"  每股分红: {row[9]}")
        
    def run(self):
        """运行检查"""
        if self.init_baostock():
            self.check_pufa_dividend()
            # 登出
            self.baostock.logout()
            print("Baostock已退出")

if __name__ == "__main__":
    checker = PufaDividendChecker()
    checker.run()
