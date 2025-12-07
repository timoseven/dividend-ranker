# 沪深股市股息率排名生成器

一个用于生成沪深两市每年最高股息率前100名股票的Python工具。

## 功能特点

- 自动抓取沪深两市所有股票数据
- 计算2020年至2025年每年的股息率排名
- 股票价格以统计当年第一个交易日的收盘价为准
- 生成美观的HTML页面，支持年份切换查看
- 数据来源：东方财富网、网易财经

## 技术栈

- Python 3.8+
- requests - 网络请求
- pandas - 数据处理
- beautifulsoup4 - HTML解析

## 安装使用

### 1. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行程序

```bash
python dividend_ranker.py
```

### 4. 查看结果

程序运行完成后，会生成以下文件：

- `dividend_rankings.html` - 可视化的HTML页面，包含每年的股息率排名
- `data/` 目录 - 包含每年的CSV格式数据文件

## 项目结构

```
.
├── dividend_ranker.py    # 主程序文件
├── requirements.txt      # 依赖包列表
├── README.md            # 项目说明文档
└── data/                # 数据存储目录
    ├── 2020_dividend_rankings.csv
    ├── 2021_dividend_rankings.csv
    ├── 2022_dividend_rankings.csv
    ├── 2023_dividend_rankings.csv
    ├── 2024_dividend_rankings.csv
    └── 2025_dividend_rankings.csv
```

## 数据说明

- **股票代码**：沪深两市股票代码
- **股票名称**：股票的中文名称
- **当年第一个交易日**：统计年度的第一个交易日日期
- **收盘价**：当年第一个交易日的收盘价
- **现金分红**：当年每股现金分红金额
- **股息率**：（现金分红 / 当年第一个交易日收盘价）× 100%

## 注意事项

1. 程序首次运行时需要抓取大量数据，可能需要较长时间
2. 建议在网络稳定的环境下运行
3. 部分股票可能因数据缺失无法计算股息率，会被自动跳过
4. 数据仅供参考，不构成投资建议

## 许可证

MIT