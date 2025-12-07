# 沪深股市股息率排名生成器

一个用于生成沪深两市股息率排名的Python工具，展示2020年至2025年的股息率数据。

## 功能特点

- 自动从Baostock API抓取沪深两市股票数据
- 计算2020年至2025年每年的股息率排名
- 显示2020-2025年间至少有一年股息率大于3%的所有股票
- 支持横向比较各年份股息率
- 股票价格以统计当年1月1日的收盘价为准
- 计算并显示累计股息率
- 显示最新收盘价
- 计算并显示最近3年（2023-2025）的股息率方差
- 生成美观的HTML页面，支持：
  - 表格排序（点击表头）
  - 粘性列（股票代码和名称固定）
  - 冻结表头
  - 数据说明

## 技术栈

- Python 3.8+
- baostock - 金融数据API
- requests - 网络请求

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
python real_data_dividend_ranker.py
```

### 4. 查看结果

程序运行完成后，会生成以下文件：

- `dividend_rankings.html` - 可视化的HTML页面，包含股息率横向比较和排名
- `data/` 目录 - 包含每年的CSV格式数据文件和累计排名文件

## 项目结构

```
.
├── real_data_dividend_ranker.py    # 主程序文件
├── requirements.txt                # 依赖包列表
├── README.md                      # 项目说明文档
├── dividend_rankings.html          # 生成的HTML页面
└── data/                          # 数据存储目录
    ├── 2020_dividend_rankings.csv
    ├── 2021_dividend_rankings.csv
    ├── 2022_dividend_rankings.csv
    ├── 2023_dividend_rankings.csv
    ├── 2024_dividend_rankings.csv
    ├── 2025_dividend_rankings.csv
    └── cumulative_dividend_rankings.csv
```

## 数据说明

- **股票代码**：沪深两市股票代码
- **股票名称**：股票的中文名称
- **最新收盘价**：股票最近一个交易日的收盘价
- **累计股息率**：2020年至2025年的股息率总和
- **股息率方差**：2023年至2025年股息率的方差
- **年度股息率**：当年累计分红金额 / 当年1月1日收盘价 × 100%
- **年度首价**：当年1月1日的收盘价

## 注意事项

1. 程序运行时需要从Baostock API获取数据，可能需要较长时间
2. 建议在网络稳定的环境下运行
3. 部分股票可能因数据缺失无法计算股息率，会被自动跳过
4. 数据仅供参考，不构成投资建议
5. 程序会自动处理股票一年中多次分红的情况，计算累计分红金额

## 许可证

MIT