#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：查询浦发银行的分红数据
"""

import time
import baostock as bs

# 登录Baostock
login_result = bs.login()
print(f"登录结果: {login_result.error_code}, {login_result.error_msg}")

# 查询浦发银行(sh.600000)2025年的分红数据
code = "sh.600000"
print(f"\n查询{code}浦发银行2025年分红数据...")

rs = bs.query_dividend_data(
    code=code,
    year=2025,
    yearType="report"
)

print(f"查询结果: {rs.error_code}, {rs.error_msg}")
print("\n分红数据详情:")
print(f"字段: {rs.fields}")

# 打印所有数据行
while rs.next():
    row = rs.get_row_data()
    print(f"行数据: {row}")
    print(f"第9列(分红额): {row[9]}")
    
    # 手动计算每股分红
    if len(row) >= 10:
        dividend = row[9]
        if dividend and dividend != '' and dividend != '0':
            try:
                # 检查计算逻辑
                dividend_value = float(dividend)
                per_share_dividend_10 = dividend_value / 10.0  # 10派x元
                per_share_dividend_100 = dividend_value / 100.0  # 100派x元
                print(f"\n计算测试:")
                print(f"原始分红值: {dividend_value}")
                print(f"如果是10派x元: {per_share_dividend_10}元/股")
                print(f"如果是100派x元: {per_share_dividend_100}元/股")
            except ValueError:
                print(f"无法转换分红值: {dividend}")

# 同时查询历史K线数据，获取2025年11月28日的收盘价
print(f"\n查询{code}2025年11月28日收盘价...")
rs_k = bs.query_history_k_data_plus(
    code=code,
    fields="date,close",
    start_date="2025-11-28",
    end_date="2025-11-28",
    frequency="d",
    adjustflag="3"
)

print(f"K线查询结果: {rs_k.error_code}, {rs_k.error_msg}")
while rs_k.next():
    row = rs_k.get_row_data()
    print(f"收盘价数据: {row}")

# 退出Baostock
bs.logout()
print("\n已退出Baostock")
