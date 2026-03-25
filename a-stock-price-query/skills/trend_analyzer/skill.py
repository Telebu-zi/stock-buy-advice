#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票趋势分析 Skill
功能：分析股票价格趋势，提供趋势判断和投资建议
"""

from datetime import datetime
from typing import Dict, List, Optional


class StockTrendAnalyzer:
    """股票趋势分析 Skill"""

    def __init__(self):
        """初始化趋势分析器"""
        # 示例股票数据（在实际应用中应该从数据库或API获取）
        self.stock_trend_data = {
            "000001": {
                "name": "平安银行",
                "sector": "金融",
                "trend": "上升",
                "momentum": "中等",
                "support_level": 15.50,
                "resistance_level": 16.20,
                "risk_level": "低",
                "recommendation": "持有",
                "analysis_date": "2026-03-09"
            },
            "000858": {
                "name": "五粮液",
                "sector": "消费",
                "trend": "震荡",
                "momentum": "弱",
                "support_level": 180.00,
                "resistance_level": 190.00,
                "risk_level": "中",
                "recommendation": "观望",
                "analysis_date": "2026-03-09"
            },
            "600000": {
                "name": "浦发银行",
                "sector": "金融",
                "trend": "下降",
                "momentum": "弱",
                "support_level": 12.00,
                "resistance_level": 12.60,
                "risk_level": "中",
                "recommendation": "谨慎",
                "analysis_date": "2026-03-09"
            }
        }

        # 技术指标权重
        self.indicator_weights = {
            "trend": 0.3,
            "momentum": 0.25,
            "support_resistance": 0.2,
            "risk": 0.25
        }

    def analyze_trend(self, stock_code_or_name: str) -> Dict:
        """
        分析股票趋势

        Args:
            stock_code_or_name: 股票代码或名称

        Returns:
            趋势分析结果字典
        """
        # 解析股票代码
        stock_code = self._resolve_stock_code(stock_code_or_name)

        if not stock_code:
            return {
                "success": False,
                "error": f"找不到股票：{stock_code_or_name}",
                "message": "请输入有效的股票代码或名称"
            }

        if stock_code not in self.stock_trend_data:
            return {
                "success": False,
                "error": f"暂无该股票的趋势分析数据：{stock_code}",
                "message": "请确认股票代码是否正确"
            }

        stock_info = self.stock_trend_data[stock_code]

        # 计算综合评分 (0-100分)
        score = self._calculate_composite_score(stock_info)

        # 生成详细分析报告
        analysis = self._generate_analysis_report(stock_info, score)

        return {
            "success": True,
            "stock_code": stock_code,
            "stock_name": stock_info["name"],
            "sector": stock_info["sector"],
            "analysis_date": stock_info["analysis_date"],
            "score": score,
            "trend": stock_info["trend"],
            "momentum": stock_info["momentum"],
            "support_level": stock_info["support_level"],
            "resistance_level": stock_info["resistance_level"],
            "risk_level": stock_info["risk_level"],
            "recommendation": stock_info["recommendation"],
            "analysis": analysis,
            "detailed_indicators": self._get_detailed_indicators(stock_info),
            "query_time": datetime.now().isoformat()
        }

    def _resolve_stock_code(self, code_or_name: str) -> Optional[str]:
        """根据股票代码或名称查找股票代码"""
        # 先直接查找代码
        if code_or_name in self.stock_trend_data:
            return code_or_name

        # 按名称查找
        for code, info in self.stock_trend_data.items():
            if info["name"] == code_or_name:
                return code

        return None

    def _calculate_composite_score(self, stock_info: Dict) -> float:
        """计算综合评分"""
        # 趋势评分
        trend_scores = {"上升": 80, "震荡": 50, "下降": 20}
        trend_score = trend_scores.get(stock_info["trend"], 50)

        # 动量评分
        momentum_scores = {"强": 90, "中等": 65, "弱": 40}
        momentum_score = momentum_scores.get(stock_info["momentum"], 50)

        # 风险评分（风险越低分数越高）
        risk_scores = {"低": 90, "中": 60, "高": 30}
        risk_score = risk_scores.get(stock_info["risk_level"], 50)

        # 支撑阻力评分（基于价格空间）
        price_space = stock_info["resistance_level"] - stock_info["support_level"]
        if price_space > 0:
            support_resistance_score = min(100, (price_space / stock_info["support_level"] * 1000))
        else:
            support_resistance_score = 50

        # 加权计算总分
        total_score = (
            trend_score * self.indicator_weights["trend"] +
            momentum_score * self.indicator_weights["momentum"] +
            support_resistance_score * self.indicator_weights["support_resistance"] +
            risk_score * self.indicator_weights["risk"]
        )

        return round(total_score, 1)

    def _generate_analysis_report(self, stock_info: Dict, score: float) -> str:
        """生成分析报告"""
        report = []

        report.append(f"【{stock_info['name']}】趋势分析报告")
        report.append("-" * 40)

        # 总体评价
        if score >= 70:
            overall = "积极"
        elif score >= 40:
            overall = "中性"
        else:
            overall = "谨慎"

        report.append(f"综合评分: {score}/100 ({overall})")
        report.append(f"趋势方向: {stock_info['trend']}")
        report.append(f"价格动能: {stock_info['momentum']}")

        # 关键价位
        report.append(f"支撑位: ¥{stock_info['support_level']:.2f}")
        report.append(f"阻力位: ¥{stock_info['resistance_level']:.2f}")
        report.append(f"风险等级: {stock_info['risk_level']}")

        # 投资建议
        report.append(f"操作建议: {stock_info['recommendation']}")

        # 详细说明
        if stock_info['trend'] == "上升":
            report.append("\n📈 趋势说明：股价处于上升通道，多头占据主导地位。")
        elif stock_info['trend'] == "下降":
            report.append("\n📉 趋势说明：股价处于下降通道，空头压力较大。")
        else:
            report.append("\n↔️ 趋势说明：股价在区间内震荡，方向不明。")

        return "\n".join(report)

    def _get_detailed_indicators(self, stock_info: Dict) -> Dict:
        """获取详细技术指标"""
        return {
            "moving_averages": {
                "ma5": "金叉" if stock_info["trend"] == "上升" else "死叉",
                "ma10": "向上" if stock_info["trend"] == "上升" else "向下",
                "ma20": "支撑" if stock_info["trend"] == "上升" else "压力"
            },
            "oscillators": {
                "rsi": "中性" if stock_info["momentum"] == "中等" else "超买" if stock_info["momentum"] == "强" else "超卖",
                "macd": "金叉" if stock_info["trend"] == "上升" else "死叉"
            },
            "volatility": {
                "bollinger_bands": "收窄" if stock_info["momentum"] == "弱" else "扩张",
                "atr": "低" if stock_info["risk_level"] == "低" else "高"
            }
        }

    def compare_stocks(self, stock_codes: List[str]) -> Dict:
        """
        比较多只股票的趋势

        Args:
            stock_codes: 股票代码列表

        Returns:
            比较结果字典
        """
        results = []

        for code in stock_codes:
            analysis = self.analyze_trend(code)
            if analysis["success"]:
                results.append({
                    "stock_code": analysis["stock_code"],
                    "stock_name": analysis["stock_name"],
                    "score": analysis["score"],
                    "trend": analysis["trend"],
                    "recommendation": analysis["recommendation"]
                })

        # 按评分排序
        results.sort(key=lambda x: x["score"], reverse=True)

        return {
            "success": True,
            "comparison_date": datetime.now().isoformat(),
            "total_stocks": len(results),
            "results": results,
            "top_pick": results[0] if results else None,
            "bottom_pick": results[-1] if results else None
        }

    def format_output(self, result: Dict) -> str:
        """
        格式化输出结果

        Args:
            result: 分析结果字典

        Returns:
            格式化后的文本
        """
        if not result["success"]:
            return f"❌ {result['error']}\n💡 {result['message']}"

        output = []
        output.append("=" * 60)
        output.append(f"📊 股票趋势分析报告")
        output.append("=" * 60)
        output.append(f"股票代码: {result['stock_code']}")
        output.append(f"股票名称: {result['stock_name']}")
        output.append(f"所属板块: {result['sector']}")
        output.append(f"分析日期: {result['analysis_date']}")
        output.append("-" * 60)

        # 添加分析报告
        output.append(result["analysis"])

        # 详细指标
        output.append("\n📋 技术指标详情:")
        indicators = result["detailed_indicators"]
        output.append(f"  移动平均线: MA5-{indicators['moving_averages']['ma5']}, MA10-{indicators['moving_averages']['ma10']}, MA20-{indicators['moving_averages']['ma20']}")
        output.append(f"  摆动指标: RSI-{indicators['oscillators']['rsi']}, MACD-{indicators['oscillators']['macd']}")
        output.append(f"  波动率: 布林带-{indicators['volatility']['bollinger_bands']}, ATR-{indicators['volatility']['atr']}")

        output.append("=" * 60)

        return "\n".join(output)


def main():
    """主函数 - 演示使用"""
    analyzer = StockTrendAnalyzer()

    print("\n📊 股票趋势分析 Skill 演示")
    print("=" * 60)

    # 示例1：分析单只股票
    print("\n1. 分析平安银行趋势:")
    result1 = analyzer.analyze_trend("000001")
    print(analyzer.format_output(result1))

    # 示例2：按名称分析
    print("\n2. 分析五粮液趋势:")
    result2 = analyzer.analyze_trend("五粮液")
    print(analyzer.format_output(result2))

    # 示例3：比较多只股票
    print("\n3. 比较多只股票:")
    comparison = analyzer.compare_stocks(["000001", "000858", "600000"])
    if comparison["success"]:
        print(f"📈 股票比较结果 (共{comparison['total_stocks']}只):")
        for stock in comparison["results"]:
            print(f"  {stock['stock_name']}({stock['stock_code']}): 评分{stock['score']}, 趋势{stock['trend']}, 建议{stock['recommendation']}")

        if comparison["top_pick"]:
            print(f"\n🏆 首选推荐: {comparison['top_pick']['stock_name']} (评分最高)")
        if comparison["bottom_pick"]:
            print(f"⚠️  谨慎关注: {comparison['bottom_pick']['stock_name']} (评分最低)")

    print("\n✅ 演示完成！")


if __name__ == "__main__":
    main()

