#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股票最近 5 日收盘价查询 - 使用示例
"""

import json
import os
import sys

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fetch_stock_price import StockPriceQuery


def example_1_query_by_code():
    """示例 1：按股票代码查询"""
    print("=" * 60)
    print("【示例 1】按股票代码查询 - 000001 (平安银行)")
    print("=" * 60)

    query = StockPriceQuery()
    result = query.query("000001")
    print(query.format_output(result))
    print()


def example_2_query_by_name():
    """示例 2：按股票名称查询"""
    print("=" * 60)
    print("【示例 2】按股票名称查询 - 五粮液")
    print("=" * 60)

    query = StockPriceQuery()
    result = query.query("五粮液")
    print(query.format_output(result))
    print()


def example_3_json_output():
    """示例 3：JSON 格式输出"""
    print("=" * 60)
    print("【示例 3】JSON 格式输出 - 浦发银行")
    print("=" * 60)

    query = StockPriceQuery()
    result = query.query("600000")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()


def example_4_error_handling():
    """示例 4：错误处理"""
    print("=" * 60)
    print("【示例 4】错误处理 - 查询不存在的股票")
    print("=" * 60)

    query = StockPriceQuery()
    result = query.query("999999")
    print(query.format_output(result))
    print()


def example_5_batch_query():
    """示例 5：批量查询"""
    print("=" * 60)
    print("【示例 5】批量查询多只股票")
    print("=" * 60)

    query = StockPriceQuery()
    stocks = ["000001", "五粮液", "浦发银行"]

    for stock in stocks:
        result = query.query(stock)
        if result["success"]:
            print(f"\n✅ {result['stock_name']} ({result['stock_code']})")
            stats = result["statistics"]
            print(f"   最高: ¥{stats['highest_price']:.2f} | "
                  f"最低: ¥{stats['lowest_price']:.2f} | "
                  f"平均: ¥{stats['average_price']:.2f}")
        else:
            print(f"\n❌ {stock}: {result['error']}")

    print()


def example_6_data_analysis():
    """示例 6：数据分析"""
    print("=" * 60)
    print("【示例 6】数据分析 - 计算价格波动情况")
    print("=" * 60)

    query = StockPriceQuery()
    result = query.query("000001")

    if result["success"]:
        data = result["data"]
        stats = result["statistics"]

        print(f"股票：{result['stock_name']} ({result['stock_code']})")
        print(f"\n价格波动分析：")

        # 分析涨跌情况
        up_count = sum(1 for item in data if "change" in item and item["change"] > 0)
        down_count = sum(1 for item in data if "change" in item and item["change"] < 0)
        flat_count = sum(1 for item in data if "change" in item and item["change"] == 0)

        print(f"  上涨天数：{up_count} 天")
        print(f"  下跌天数：{down_count} 天")
        print(f"  持平天数：{flat_count} 天")

        # 波动幅度
        volatility = (stats["price_range"] / stats["average_price"]) * 100
        print(f"\n波动指标：")
        print(f"  价格跨度：¥{stats['price_range']:.2f}")
        print(f"  波动率：{volatility:.2f}%")

        # 趋势判断
        first_price = data[-1]["close_price"]  # 最后一天（最早）
        last_price = data[0]["close_price"]    # 第一天（最新）
        trend = "上升" if last_price > first_price else "下降"
        trend_pct = abs((last_price - first_price) / first_price * 100)

        print(f"\n趋势判断：")
        print(f"  总体趋势：{trend}")
        print(f"  变化幅度：{trend_pct:.2f}%")

    print()


def main():
    """运行所有示例"""
    print("\n")
    print("*" * 60)
    print("    A 股票最近 5 日收盘价查询 - 使用示例")
    print("*" * 60)
    print()

    # 运行所有示例
    example_1_query_by_code()
    example_2_query_by_name()
    example_3_json_output()
    example_4_error_handling()
    example_5_batch_query()
    example_6_data_analysis()

    print("=" * 60)
    print("✅ 所有示例执行完毕！")
    print("=" * 60)


if __name__ == "__main__":
    main()

