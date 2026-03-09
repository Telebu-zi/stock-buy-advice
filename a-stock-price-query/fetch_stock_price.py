#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股票最近5日收盘价查询脚本

功能：查询指定A股股票的最近5日收盘价数据
"""

import json
from datetime import datetime
from typing import Dict, Optional


class StockPriceQuery:
    """A股票价格查询类"""

    def __init__(self):
        """初始化股票查询器"""
        # 模拟股票数据字典
        self.stock_data = {
            "000001": {
                "name": "平安银行",
                "prices": [
                    {"date": "2026-03-09", "close": 15.88},
                    {"date": "2026-03-06", "close": 15.76},
                    {"date": "2026-03-05", "close": 15.84},
                    {"date": "2026-03-04", "close": 15.78},
                    {"date": "2026-03-03", "close": 15.82},
                ]
            },
            "000858": {
                "name": "五粮液",
                "prices": [
                    {"date": "2026-03-09", "close": 185.50},
                    {"date": "2026-03-06", "close": 183.25},
                    {"date": "2026-03-05", "close": 182.10},
                    {"date": "2026-03-04", "close": 181.50},
                    {"date": "2026-03-03", "close": 180.80},
                ]
            },
            "600000": {
                "name": "浦发银行",
                "prices": [
                    {"date": "2026-03-09", "close": 12.45},
                    {"date": "2026-03-06", "close": 12.38},
                    {"date": "2026-03-05", "close": 12.50},
                    {"date": "2026-03-04", "close": 12.42},
                    {"date": "2026-03-03", "close": 12.40},
                ]
            }
        }

        # 股票名称到代码的映射
        self.name_to_code = {v["name"]: k for k, v in self.stock_data.items()}

    def _resolve_stock_code(self, code_or_name: str) -> Optional[str]:
        """
        根据股票代码或名称查找股票代码

        Args:
            code_or_name: 股票代码或名称

        Returns:
            股票代码，如果不存在返回 None
        """
        # 直接查找代码
        if code_or_name in self.stock_data:
            return code_or_name

        # 按名称查找
        if code_or_name in self.name_to_code:
            return self.name_to_code[code_or_name]

        return None

    def _calculate_change(self, current_price: float, previous_price: float) -> tuple:
        """
        计算价格变化

        Args:
            current_price: 当前价格
            previous_price: 前一个价格

        Returns:
            (价格变化值, 变化百分比)
        """
        change = round(current_price - previous_price, 2)
        change_percent = round((change / previous_price * 100), 2) if previous_price != 0 else 0
        return change, change_percent

    def query(self, stock_code_or_name: str) -> Dict:
        """
        查询股票最近5日收盘价

        Args:
            stock_code_or_name: 股票代码或名称

        Returns:
            包含股票数据的字典
        """
        # 解析股票代码
        stock_code = self._resolve_stock_code(stock_code_or_name)

        if not stock_code:
            return {
                "success": False,
                "error": f"找不到股票：{stock_code_or_name}",
                "message": "请输入有效的股票代码或名称"
            }

        stock_info = self.stock_data[stock_code]
        prices = stock_info["prices"]

        # 构建带涨跌幅的数据
        data = []
        for i, price_info in enumerate(prices):
            record = {
                "date": price_info["date"],
                "close_price": price_info["close"],
            }

            # 计算涨跌幅（相对前一日）
            if i < len(prices) - 1:
                next_price = prices[i + 1]["close"]
                change, change_percent = self._calculate_change(price_info["close"], next_price)
                record["change"] = change
                record["change_percent"] = change_percent

            data.append(record)

        # 计算统计信息
        close_prices = [p["close"] for p in prices]
        statistics = {
            "highest_price": round(max(close_prices), 2),
            "lowest_price": round(min(close_prices), 2),
            "average_price": round(sum(close_prices) / len(close_prices), 2),
            "price_range": round(max(close_prices) - min(close_prices), 2),
        }

        return {
            "success": True,
            "stock_code": stock_code,
            "stock_name": stock_info["name"],
            "currency": "CNY",
            "data": data,
            "statistics": statistics,
            "query_time": datetime.now().isoformat()
        }

    def format_output(self, result: Dict) -> str:
        """
        格式化输出结果为易读的文本格式

        Args:
            result: 查询结果字典

        Returns:
            格式化后的文本
        """
        if not result["success"]:
            return f"❌ {result['error']}\n{result['message']}"

        output = []
        output.append("=" * 50)
        output.append(f"【股票信息】")
        output.append(f"代码：{result['stock_code']}")
        output.append(f"名称：{result['stock_name']}")
        output.append(f"货币：人民币")
        output.append("")

        output.append(f"【最近 5 日收盘价】")
        for item in result["data"]:
            date = item["date"]
            price = item["close_price"]

            if "change" in item:
                change = item["change"]
                change_pct = item["change_percent"]
                direction = "↑" if change >= 0 else "↓"
                output.append(f"{date}：¥{price:.2f} {direction} {abs(change):.2f} ({change_pct:+.2f}%)")
            else:
                output.append(f"{date}：¥{price:.2f}")

        output.append("")
        output.append(f"【统计信息】")
        stats = result["statistics"]
        output.append(f"最高价：¥{stats['highest_price']:.2f}")
        output.append(f"最低价：¥{stats['lowest_price']:.2f}")
        output.append(f"平均价：¥{stats['average_price']:.2f}")
        output.append(f"价格跨度：¥{stats['price_range']:.2f}")
        output.append("=" * 50)

        return "\n".join(output)


def main():
    """主函数 - 演示脚本使用"""
    query = StockPriceQuery()

    # 示例 1：用代码查询
    print("示例 1：查询平安银行（代码）")
    result1 = query.query("000001")
    print(query.format_output(result1))
    print()

    # 示例 2：用名称查询
    print("示例 2：查询五粮液（名称）")
    result2 = query.query("五粮液")
    print(query.format_output(result2))
    print()

    # 示例 3：查询不存在的股票
    print("示例 3：查询不存在的股票")
    result3 = query.query("999999")
    print(query.format_output(result3))

    # 返回 JSON 格式
    print("\n" + "=" * 50)
    print("JSON 格式输出示例：")
    print(json.dumps(result1, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

