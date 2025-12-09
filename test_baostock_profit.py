#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Baostock API 的利润数据获取
"""

import baostock as bs

def test_baostock_profit():
    """测试获取利润数据"""
    # 登录 Baostock
    login_result = bs.login()
    print(f"登录结果: {login_result.error_code}, {login_result.error_msg}")
    
    if login_result.error_code != '0':
        return
    
    # 测试查询利润数据 - 尝试不同的参数格式
    print("\n=== 测试查询利润数据 ===")
    code = "sh.600000"  # 浦发银行
    year = 2020
    
    # 尝试查询资产负债表数据
    print("\n=== 测试查询资产负债表数据 ===")
    rs = bs.query_balance_data(
        code=code,
        year=year,
        quarter=4
    )
    
    print(f"查询结果: {rs.error_code}, {rs.error_msg}")
    
    if rs.error_code == '0':
        # 获取字段信息
        print(f"\n字段名: {rs.fields}")
        
        # 遍历结果
        print("\n资产负债表数据:")
        while rs.next():
            row = rs.get_row_data()
            print(f"  {row}")
    
    # 尝试查询现金流量表数据
    print("\n=== 测试查询现金流量表数据 ===")
    rs = bs.query_cash_flow_data(
        code=code,
        year=year,
        quarter=4
    )
    
    print(f"查询结果: {rs.error_code}, {rs.error_msg}")
    
    if rs.error_code == '0':
        # 获取字段信息
        print(f"\n字段名: {rs.fields}")
        
        # 遍历结果
        print("\n现金流量表数据:")
        while rs.next():
            row = rs.get_row_data()
            print(f"  {row}")
    
    # 尝试查询成长能力数据
    print("\n=== 测试查询成长能力数据 ===")
    rs = bs.query_growth_data(
        code=code,
        year=year,
        quarter=4
    )
    
    print(f"查询结果: {rs.error_code}, {rs.error_msg}")
    
    if rs.error_code == '0':
        # 获取字段信息
        print(f"\n字段名: {rs.fields}")
        
        # 遍历结果
        print("\n成长能力数据:")
        while rs.next():
            row = rs.get_row_data()
            print(f"  {row}")
    
    # 登出
    bs.logout()

if __name__ == "__main__":
    test_baostock_profit()