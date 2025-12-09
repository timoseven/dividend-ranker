#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Baostock API获取收盘价
"""

import baostock as bs

def test_close_price():
    """测试获取收盘价"""
    # 登录Baostock
    login_result = bs.login()
    print(f"登录结果: {login_result.error_code}, {login_result.error_msg}")
    
    if login_result.error_code != '0':
        return
    
    # 测试获取收盘价
    code = "sh.600000"  # 浦发银行
    year = 2020
    
    print(f"\n=== 测试获取{code} {year}年收盘价 ===")
    
    # 使用不复权数据
    rs = bs.query_history_k_data_plus(
        code=code,
        fields="date,close",
        start_date=f"{year}-01-01",
        end_date=f"{year}-12-31",
        frequency="d",
        adjustflag="3"  # 3表示不复权
    )
    
    print(f"查询结果: {rs.error_code}, {rs.error_msg}")
    
    if rs.error_code == '0':
        close_prices = []
        while rs.next():
            row = rs.get_row_data()
            close_prices.append(row)
        
        print(f"共获取到{len(close_prices)}条记录")
        
        # 显示前5条和最后5条
        if close_prices:
            print("\n前5条记录:")
            for row in close_prices[:5]:
                print(f"  {row}")
            
            print("\n最后5条记录:")
            for row in close_prices[-5:]:
                print(f"  {row}")
            
            # 显示最后一个交易日的收盘价
            last_close = close_prices[-1]
            print(f"\n最后一个交易日: {last_close[0]}, 收盘价: {last_close[1]}")
    
    # 登出
    bs.logout()

if __name__ == "__main__":
    test_close_price()