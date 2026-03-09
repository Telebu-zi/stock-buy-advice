# A 股票最近 5 日收盘价查询 Skill

这是一个 CatPaw AI 助手的 Skill，用于查询指定 A 股股票的最近 5 日收盘价数据。

## 功能特性

✨ **核心功能**
- 🔍 支持按股票代码或名称查询
- 📊 提供最近 5 个交易日的收盘价
- 📈 自动计算涨跌幅百分比
- 📋 统计最高价、最低价、平均价、价格跨度

## 快速开始

### 安装

```bash
# 克隆项目
git clone <repo-url>

# 进入项目目录
cd a-stock-price-query

# 安装依赖（如有）
pip install -r requirements.txt
```

### 使用

#### 方式 1：命令行运行

```bash
python fetch_stock_price.py
```

#### 方式 2：作为 Python 模块导入

```python
from fetch_stock_price import StockPriceQuery

# 创建查询器
query = StockPriceQuery()

# 按代码查询
result = query.query("000001")

# 按名称查询
result = query.query("平安银行")

# 格式化输出
print(query.format_output(result))
```

## 使用示例

### 示例 1：查询平安银行

**输入：**
```
查询平安银行最近5日的收盘价
```

**输出：**
```
==================================================
【股票信息】
代码：000001
名称：平安银行
货币：人民币

【最近 5 日收盘价】
2026-03-09：¥15.88 ↑ 0.12 (+0.76%)
2026-03-06：¥15.76 ↓ 0.08 (-0.51%)
2026-03-05：¥15.84 ↑ 0.06 (+0.38%)
2026-03-04：¥15.78 ↓ 0.04 (-0.25%)
2026-03-03：¥15.82

【统计信息】
最高价：¥15.88
最低价：¥15.50
平均价：¥15.72
价格跨度：¥0.38
==================================================
```

### 示例 2：按代码查询

```python
result = query.query("600000")  # 浦发银行
```

### 示例 3：JSON 格式获取

```python
result = query.query("000858")  # 五粮液
print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 数据说明

| 字段 | 说明 | 示例 |
|-----|------|------|
| stock_code | 股票代码 | "000001" |
| stock_name | 股票名称 | "平安银行" |
| close_price | 收盘价 | 15.88 |
| change | 价格变化（元） | 0.12 |
| change_percent | 变化百分比 | 0.76 |
| highest_price | 5日最高价 | 15.88 |
| lowest_price | 5日最低价 | 15.50 |
| average_price | 5日平均价 | 15.72 |
| price_range | 5日价格跨度 | 0.38 |

## 支持的股票

目前支持以下股票查询（可扩展）：

- `000001` / `平安银行`
- `000858` / `五粮液`
- `600000` / `浦发银行`

## API 参数

### query(stock_code_or_name: str) -> Dict

查询股票最近 5 日收盘价

**参数：**
- `stock_code_or_name` (str)：股票代码或名称

**返回值：**
```json
{
  "success": true,
  "stock_code": "000001",
  "stock_name": "平安银行",
  "currency": "CNY",
  "data": [...],
  "statistics": {...},
  "query_time": "2026-03-09T10:30:00"
}
```

**错误返回：**
```json
{
  "success": false,
  "error": "找不到股票：999999",
  "message": "请输入有效的股票代码或名称"
}
```

## 文件结构

```
a-stock-price-query/
├── SKILL.md                    # Skill 定义文档
├── README.md                   # 本文件
├── fetch_stock_price.py        # 主程序脚本
├── requirements.txt            # 依赖列表
└── examples/                   # 使用示例目录
    └── example_usage.py        # 使用示例
```

## 扩展功能

### 添加新股票

修改 `fetch_stock_price.py` 中的 `stock_data` 字典：

```python
self.stock_data = {
    "新代码": {
        "name": "新股票名称",
        "prices": [
            {"date": "2026-03-09", "close": 价格},
            # ...
        ]
    }
}
```

### 连接真实数据源

替换 `query()` 方法中的数据获取部分，使用真实 API：

```python
# 调用股票数据 API
response = requests.get(f"https://api.example.com/stock/{stock_code}")
prices = response.json()
```

## 技术栈

- **语言**：Python 3.7+
- **依赖**：无外部依赖（可选 requests 用于 API 调用）

## 常见问题

**Q: 如何查询更多交易日的数据？**
A: 修改脚本中 `query()` 方法返回的数据列表长度。

**Q: 如何添加自己的股票？**
A: 在 `stock_data` 字典中添加新的股票信息。

**Q: 支持国际股票吗？**
A: 目前仅支持 A 股，可通过扩展来支持。

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。

## 版本历史

- **v1.0** (2026-03-09) - 初版发布
  - ✅ 支持按代码查询
  - ✅ 支持按名称查询
  - ✅ 自动计算涨跌幅
  - ✅ 提供统计信息

