# A 股票最近 5 日收盘价查询 Skill - 安装和部署指南

## 快速开始

### 1. 项目克隆（如果还没有）

```bash
cd /Users/telebup/github-project
git clone <repository-url>
cd a-stock-price-query
```

### 2. 安装依赖

目前该 Skill 无外部依赖，纯 Python 实现：

```bash
# 可选：安装开发依赖
pip install -r requirements.txt
```

### 3. 快速测试

```bash
# 运行主程序演示
python3 fetch_stock_price.py

# 或运行完整示例
python3 examples/example_usage.py
```

## 目录结构说明

```
a-stock-price-query/
│
├── SKILL.md                     # Skill 定义文档（CatPaw 识别）
├── README.md                    # 项目说明文档
├── INSTALLATION.md              # 本文件 - 安装指南
│
├── fetch_stock_price.py         # 核心功能模块
│   ├── StockPriceQuery          # 主要类
│   ├── query()                  # 查询方法
│   ├── format_output()          # 格式化输出
│   └── main()                   # 命令行入口
│
├── requirements.txt             # Python 依赖
│
└── examples/
    └── example_usage.py         # 使用示例和演示
        ├── example_1_query_by_code()
        ├── example_2_query_by_name()
        ├── example_3_json_output()
        ├── example_4_error_handling()
        ├── example_5_batch_query()
        └── example_6_data_analysis()
```

## 文件说明

### SKILL.md
- **用途**：CatPaw 识别和加载该项目为 Skill 的标记文件
- **内容**：Skill 的功能描述、使用场景、参数定义、输出格式等
- **格式**：Markdown

### fetch_stock_price.py
- **用途**：核心功能实现
- **主要类**：`StockPriceQuery`
- **主要方法**：
  - `query(stock_code_or_name)` - 查询股票数据
  - `format_output(result)` - 格式化输出
  - `_resolve_stock_code()` - 代码/名称解析
  - `_calculate_change()` - 计算涨跌幅

### examples/example_usage.py
- **用途**：展示各种使用方法
- **包含示例**：
  1. 按代码查询
  2. 按名称查询
  3. JSON 格式输出
  4. 错误处理
  5. 批量查询
  6. 数据分析

## 使用方式

### 方式 1：命令行直接运行

```bash
cd /Users/telebup/github-project/a-stock-price-query
python3 fetch_stock_price.py
```

**输出**：显示 3 个示例查询和统计信息

### 方式 2：Python 模块导入

```python
from fetch_stock_price import StockPriceQuery
import json

# 创建查询器实例
query = StockPriceQuery()

# 查询示例
result = query.query("000001")

# 格式化输出
print(query.format_output(result))

# 或 JSON 输出
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### 方式 3：在 CatPaw 中使用

当 Skill 被正确加载后，用户可以在 CatPaw 中直接使用：

```
用户: 查询平安银行最近5日的收盘价

CatPaw: 触发 a-stock-price-query Skill
        │
        ├── 解析用户意图：查询股票
        ├── 调用 query("平安银行")
        └── 返回格式化结果
```

### 方式 4：运行完整示例

```bash
python3 examples/example_usage.py
```

**包含**：6 种不同的使用场景演示

## 扩展功能

### 添加新股票

编辑 `fetch_stock_price.py`，修改 `StockPriceQuery.__init__()` 中的 `stock_data`：

```python
self.stock_data = {
    "000001": {
        "name": "平安银行",
        "prices": [...]
    },
    "NEW_CODE": {  # 添加新股票
        "name": "新股票名称",
        "prices": [
            {"date": "2026-03-09", "close": 100.00},
            {"date": "2026-03-06", "close": 99.50},
            # ...
        ]
    }
}
```

### 连接真实数据源

替换数据获取部分：

```python
def _fetch_from_api(self, stock_code):
    """从真实 API 获取数据"""
    import requests

    url = f"https://api.example.com/stock/{stock_code}/5d"
    response = requests.get(url)
    return response.json()
```

### 支持更多交易日

修改查询逻辑以支持 10 日、30 日等：

```python
def query(self, stock_code_or_name, days=5):
    """
    查询股票收盘价

    Args:
        stock_code_or_name: 股票代码或名称
        days: 交易日数（默认 5）
    """
    # 实现逻辑...
```

## 数据说明

### 当前支持的股票

| 代码 | 名称 | 类别 |
|-----|------|------|
| 000001 | 平安银行 | 金融 |
| 000858 | 五粮液 | 消费 |
| 600000 | 浦发银行 | 金融 |

### 数据格式

#### 查询结果成功时：
```json
{
  "success": true,
  "stock_code": "000001",
  "stock_name": "平安银行",
  "currency": "CNY",
  "data": [
    {
      "date": "2026-03-09",
      "close_price": 15.88,
      "change": 0.12,
      "change_percent": 0.76
    }
  ],
  "statistics": {
    "highest_price": 15.88,
    "lowest_price": 15.76,
    "average_price": 15.82,
    "price_range": 0.12
  },
  "query_time": "2026-03-09T11:18:11.510715"
}
```

#### 查询结果失败时：
```json
{
  "success": false,
  "error": "找不到股票：999999",
  "message": "请输入有效的股票代码或名称"
}
```

## 性能指标

- **查询速度**：< 100ms（本地数据）
- **内存占用**：< 10MB
- **支持并发**：无限制（Python GIL 限制）

## 测试

### 单元测试（可选实现）

```bash
# 如果有 pytest
pytest tests/
```

### 手动测试

```bash
# 测试所有查询方法
python3 examples/example_usage.py

# 测试错误处理
python3 -c "
from fetch_stock_price import StockPriceQuery
q = StockPriceQuery()
print(q.format_output(q.query('invalid_code')))
"
```

## 常见问题

**Q: 如何更新股票数据？**
A: 目前使用硬编码数据。生产环境应连接真实 API。

**Q: 支持实时数据吗？**
A: 当前示例使用静态数据。可扩展为实时数据接口。

**Q: 如何添加更多股票？**
A: 编辑 `stock_data` 字典，或连接数据库。

**Q: 可以查询超过 5 日的数据吗？**
A: 可以修改 `query()` 方法支持参数化天数。

## 故障排除

### 问题 1：模块导入失败

```bash
# 确保在正确的目录
cd /Users/telebup/github-project/a-stock-price-query

# 运行
python3 fetch_stock_price.py
```

### 问题 2：无输出

确保 Python 版本 >= 3.6：

```bash
python3 --version
```

### 问题 3：CatPaw 不识别 Skill

检查 SKILL.md 是否存在且格式正确。

## 开发建议

1. **添加单元测试** - 使用 pytest
2. **添加日志** - 使用 logging 模块
3. **优化性能** - 缓存常用查询
4. **扩展功能** - 支持技术指标、比较等
5. **文档完善** - 添加更多示例和 API 文档

## 许可证

MIT License

## 支持

遇到问题？
- 查看 SKILL.md - 功能说明
- 查看 README.md - 使用指南
- 查看 examples/ - 使用示例
- 修改 fetch_stock_price.py - 本地测试

---

**创建日期**: 2026-03-09
**最后更新**: 2026-03-09
**版本**: 1.0.0

