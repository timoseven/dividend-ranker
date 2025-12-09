# 股息率排名 (Dividend Ranker)

一个使用Baostock API获取股票数据，计算并展示股息率排名的Python项目。

## 功能特性

- **数据获取**：使用Baostock API获取2020-2025年股票分红和收盘价数据
- **股息率计算**：自动计算每年的股息率、累计分红和平均股息率
- **方差分析**：计算最近3年股息率的方差，评估股息率稳定性
- **HTML可视化**：生成美观的HTML报告，包含可排序的表格
- **筛选功能**：筛选出股息率大于3%的股票

## 生成文件

- `stocks.id`：股息率大于3%的股票列表
- `output/all_dividend_yield_2025.csv`：2025年所有股票股息率数据
- `output/2020_2025_dividend_data.csv`：2020-2025年股票完整数据
- `output/dividend_ranker.html`：基于2025年数据的股息率排名HTML
- `output/dividend_rankings_2020_2025.html`：2020-2025年完整数据HTML报告

## HTML报告功能

- **可排序表格**：点击表头可按任意列排序
- **固定列设计**：股票代码和名称列固定，方便浏览
- **颜色标识**：绿色显示股息率，红色显示收盘价
- **响应式设计**：支持各种设备
- **使用说明**：清晰的使用指南
- **页脚信息**：包含作者和GitHub链接

## 安装依赖

```bash
pip install baostock
```

## 使用方法

### 1. 获取股票数据

```bash
# 获取2025年所有股票股息率
python3 dividend_yield_collector.py

# 获取2020-2025年完整数据
python3 get_2020_2025_data.py
```

### 2. 生成HTML报告

```bash
# 生成2020-2025年完整数据报告
python3 generate_complete_html.py
```

### 3. 筛选高股息率股票

```bash
python3 extract_high_dividend_stocks.py
```

## 项目结构

```
stock/
├── dividend_yield_collector.py   # 获取2025年股息率
├── get_2020_2025_data.py         # 获取2020-2025年完整数据
├── generate_complete_html.py     # 生成HTML报告
├── extract_high_dividend_stocks.py # 筛选高股息率股票
├── check_pufa_dividend.py        # 检查浦发银行股息率
├── debug_pufa_dividend.py        # 调试浦发银行分红数据
├── extract_stock_codes.py        # 从图片提取股票代码
├── stock.jpg                     # 股票代码图片
├── stocks.id                     # 高股息率股票列表
├── output/                       # 输出目录
│   ├── all_dividend_yield_2025.csv          # 2025年股息率数据
│   ├── 2020_2025_dividend_data.csv          # 2020-2025年完整数据
│   ├── dividend_ranker.html                 # 2025年股息率排名
│   └── dividend_rankings_2020_2025.html     # 2020-2025年完整报告
└── README.md                     # 项目说明文档
```

## 技术栈

- **Python 3**：项目开发语言
- **Baostock API**：金融数据来源
- **HTML/CSS/JavaScript**：HTML报告生成
- **CSV**：数据存储格式

## 注意事项

1. Baostock API有调用频率限制，建议不要频繁运行数据获取脚本
2. 数据获取可能需要较长时间，尤其是获取多年数据时
3. HTML报告建议使用现代浏览器打开，以获得最佳体验
4. 股息率计算基于年报数据，可能与实际情况略有差异

## 更新日志

- **2025-12-09**：修复股息率计算错误，添加README文档
- **2025-12-08**：添加2020-2025年数据支持，优化HTML报告样式
- **2025-12-07**：初始版本，支持2025年股息率计算和HTML报告生成

## 作者

Timo & TRAE

## GitHub

[https://github.com/timoseven/dividend-ranker](https://github.com/timoseven/dividend-ranker)
