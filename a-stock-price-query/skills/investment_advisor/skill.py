#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投资建议生成 Skill
功能：基于股票数据、趋势分析和用户偏好生成投资建议
"""

from datetime import datetime
from typing import Dict, List, Optional


class InvestmentAdvisor:
    """投资建议生成 Skill"""

    def __init__(self):
        """初始化投资顾问"""
        # 投资策略模板
        self.strategy_templates = {
            "保守型": {
                "description": "低风险，稳健收益",
                "max_position": 0.3,  # 最大仓位
                "stop_loss": 0.95,    # 止损比例
                "take_profit": 1.10,  # 止盈比例
                "holding_period": "中长期"
            },
            "平衡型": {
                "description": "风险收益平衡",
                "max_position": 0.5,
                "stop_loss": 0.90,
                "take_profit": 1.15,
                "holding_period": "中期"
            },
            "积极型": {
                "description": "高风险，高收益",
                "max_position": 0.7,
                "stop_loss": 0.85,
                "take_profit": 1.20,
                "holding_period": "短期"
            }
        }

        # 市场环境因素
        self.market_factors = {
            "bullish": {
                "name": "牛市",
                "risk_appetite": "高",
                "suggested_strategy": "积极型",
                "sector_focus": ["科技", "消费", "金融"]
            },
            "neutral": {
                "name": "震荡市",
                "risk_appetite": "中",
                "suggested_strategy": "平衡型",
                "sector_focus": ["消费", "医药", "公用事业"]
            },
            "bearish": {
                "name": "熊市",
                "risk_appetite": "低",
                "suggested_strategy": "保守型",
                "sector_focus": ["防御性", "公用事业", "必需消费品"]
            }
        }

    def generate_advice(self,
                       stock_code: str,
                       stock_name: str,
                       current_price: float,
                       trend_analysis: Dict,
                       user_profile: Optional[Dict] = None) -> Dict:
        """
        生成投资建议

        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            current_price: 当前价格
            trend_analysis: 趋势分析结果
            user_profile: 用户风险偏好

        Returns:
            投资建议字典
        """
        # 默认用户配置
        if user_profile is None:
            user_profile = {
                "risk_tolerance": "平衡型",
                "investment_horizon": "中期",
                "capital": 100000
            }

        # 评估市场环境
        market_env = self._assess_market_environment(trend_analysis)

        # 匹配投资策略
        strategy = self._match_investment_strategy(user_profile, market_env, trend_analysis)

        # 生成具体建议
        specific_advice = self._generate_specific_advice(
            stock_code, stock_name, current_price, trend_analysis, strategy, user_profile
        )

        # 计算目标价位
        target_prices = self._calculate_target_prices(current_price, strategy, trend_analysis)

        # 风险评估
        risk_assessment = self._assess_risk(trend_analysis, strategy, market_env)

        return {
            "success": True,
            "stock_code": stock_code,
            "stock_name": stock_name,
            "current_price": current_price,
            "advice_date": datetime.now().isoformat(),
            "user_profile": user_profile,
            "market_environment": market_env,
            "investment_strategy": strategy,
            "specific_advice": specific_advice,
            "target_prices": target_prices,
            "risk_assessment": risk_assessment,
            "position_sizing": self._calculate_position_size(user_profile["capital"], strategy, risk_assessment),
            "monitoring_plan": self._create_monitoring_plan(trend_analysis, strategy),
            "alternative_options": self._suggest_alternatives(stock_code, trend_analysis)
        }

    def _assess_market_environment(self, trend_analysis: Dict) -> Dict:
        """评估市场环境"""
        score = trend_analysis.get("score", 50)

        if score >= 65:
            env_key = "bullish"
        elif score >= 35:
            env_key = "neutral"
        else:
            env_key = "bearish"

        env = self.market_factors[env_key].copy()
        env["assessment_score"] = score
        env["assessment_reason"] = f"基于股票趋势评分{score}分"

        return env

    def _match_investment_strategy(self,
                                 user_profile: Dict,
                                 market_env: Dict,
                                 trend_analysis: Dict) -> Dict:
        """匹配投资策略"""
        # 获取用户风险偏好
        user_risk = user_profile.get("risk_tolerance", "平衡型")

        # 考虑市场环境调整
        market_suggestion = market_env.get("suggested_strategy", "平衡型")

        # 如果用户偏好与市场建议不同，进行权衡
        if user_risk != market_suggestion:
            # 在牛市中更倾向于积极，在熊市中更倾向于保守
            final_strategy = market_suggestion if market_env["name"] in ["牛市", "熊市"] else user_risk
        else:
            final_strategy = user_risk

        strategy = self.strategy_templates[final_strategy].copy()
        strategy["name"] = final_strategy
        strategy["selection_reason"] = f"用户偏好:{user_risk}, 市场环境:{market_env['name']}"

        return strategy

    def _generate_specific_advice(self,
                                stock_code: str,
                                stock_name: str,
                                current_price: float,
                                trend_analysis: Dict,
                                strategy: Dict,
                                user_profile: Dict) -> Dict:
        """生成具体投资建议"""
        trend = trend_analysis.get("trend", "震荡")
        recommendation = trend_analysis.get("recommendation", "观望")
        score = trend_analysis.get("score", 50)

        # 核心建议
        if recommendation == "买入":
            core_action = "建议买入"
            confidence = "高" if score >= 70 else "中"
        elif recommendation == "持有":
            core_action = "建议持有"
            confidence = "中"
        elif recommendation == "卖出":
            core_action = "建议卖出或减仓"
            confidence = "高" if score <= 30 else "中"
        else:  # 观望
            core_action = "建议观望"
            confidence = "中"

        # 时机建议
        timing_advice = self._get_timing_advice(trend, current_price, trend_analysis)

        # 仓位建议
        position_advice = self._get_position_advice(strategy, score, user_profile)

        return {
            "core_action": core_action,
            "confidence_level": confidence,
            "timing": timing_advice,
            "position": position_advice,
            "reasoning": f"基于趋势分析：{trend}趋势，评分{score}分，建议{recommendation}",
            "considerations": [
                f"关注{trend_analysis.get('support_level', 'N/A')}支撑位",
                f"注意{trend_analysis.get('resistance_level', 'N/A')}阻力位",
                f"风险等级：{trend_analysis.get('risk_level', '中')}",
                f"适合{strategy.get('holding_period', '中期')}持有"
            ]
        }

    def _get_timing_advice(self, trend: str, current_price: float, trend_analysis: Dict) -> str:
        """获取时机建议"""
        support = trend_analysis.get("support_level", current_price * 0.95)
        resistance = trend_analysis.get("resistance_level", current_price * 1.05)

        if trend == "上升":
            if current_price <= support * 1.02:
                return "当前接近支撑位，是较好的买入时机"
            elif current_price >= resistance * 0.98:
                return "当前接近阻力位，可考虑分批买入"
            else:
                return "股价在上升通道中，可逢低买入"
        elif trend == "下降":
            return "下降趋势中，建议等待企稳信号"
        else:  # 震荡
            return f"震荡区间{support:.2f}-{resistance:.2f}，可在区间下沿买入"

    def _get_position_advice(self, strategy: Dict, score: float, user_profile: Dict) -> str:
        """获取仓位建议"""
        max_position = strategy.get("max_position", 0.5)
        capital = user_profile.get("capital", 100000)

        # 根据评分调整仓位
        if score >= 70:
            position_pct = max_position
        elif score >= 50:
            position_pct = max_position * 0.7
        elif score >= 30:
            position_pct = max_position * 0.4
        else:
            position_pct = max_position * 0.2

        position_amount = capital * position_pct

        return f"建议仓位：{position_pct*100:.1f}%，约¥{position_amount:,.0f}元"

    def _calculate_target_prices(self, current_price: float, strategy: Dict, trend_analysis: Dict) -> Dict:
        """计算目标价位"""
        stop_loss_pct = 1 - strategy.get("stop_loss", 0.9)
        take_profit_pct = strategy.get("take_profit", 1.15) - 1

        support = trend_analysis.get("support_level", current_price * 0.95)
        resistance = trend_analysis.get("resistance_level", current_price * 1.05)

        # 止损价
        stop_loss_price = current_price * (1 - stop_loss_pct)

        # 止盈价
        take_profit_price = current_price * (1 + take_profit_pct)

        # 调整基于技术分析
        if trend_analysis.get("trend") == "上升":
            take_profit_price = max(take_profit_price, resistance)
        else:
            take_profit_price = min(take_profit_price, resistance)

        return {
            "stop_loss": round(stop_loss_price, 2),
            "take_profit": round(take_profit_price, 2),
            "support_level": round(support, 2),
            "resistance_level": round(resistance, 2),
            "risk_reward_ratio": round((take_profit_price - current_price) / (current_price - stop_loss_price), 2)
        }

    def _assess_risk(self, trend_analysis: Dict, strategy: Dict, market_env: Dict) -> Dict:
        """风险评估"""
        risk_level = trend_analysis.get("risk_level", "中")

        risk_factors = []

        if trend_analysis.get("trend") == "下降":
            risk_factors.append("下降趋势")

        if trend_analysis.get("score", 50) < 40:
            risk_factors.append("评分较低")

        if market_env["name"] == "熊市":
            risk_factors.append("熊市环境")

        if strategy["name"] == "积极型":
            risk_factors.append("积极策略")

        risk_score = 100 - trend_analysis.get("score", 50)

        return {
            "overall_risk": risk_level,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "mitigation_suggestions": [
                "设置严格止损",
                "分批建仓",
                "定期评估",
                "分散投资"
            ]
        }

    def _calculate_position_size(self, capital: float, strategy: Dict, risk_assessment: Dict) -> Dict:
        """计算仓位大小"""
        max_position = strategy.get("max_position", 0.5)

        # 根据风险调整
        risk_score = risk_assessment.get("risk_score", 50)
        risk_adjustment = 1 - (risk_score / 200)  # 风险越高，仓位越小

        adjusted_position = max_position * risk_adjustment

        return {
            "max_position_percentage": round(max_position * 100, 1),
            "adjusted_position_percentage": round(adjusted_position * 100, 1),
            "suggested_amount": round(capital * adjusted_position, 2),
            "suggested_share_count": "根据股价确定",
            "position_adjustment_note": f"基于风险评分{risk_score}调整"
        }

    def _create_monitoring_plan(self, trend_analysis: Dict, strategy: Dict) -> List[str]:
        """创建监控计划"""
        plan = []

        plan.append(f"每日监控：股价是否突破阻力位{trend_analysis.get('resistance_level', 'N/A')}或跌破支撑位{trend_analysis.get('support_level', 'N/A')}")
        plan.append(f"每周评估：趋势是否变化，技术指标是否恶化")

        if strategy["name"] == "短期":
            plan.append("短期策略：密切关注市场情绪和技术指标变化")
        elif strategy["name"] == "中长期":
            plan.append("中长期策略：关注基本面变化和行业动态")

        plan.append("触发条件：达到止损或止盈价位时执行相应操作")

        return plan

    def _suggest_alternatives(self, current_stock_code: str, trend_analysis: Dict) -> List[Dict]:
        """建议替代选项"""
        # 模拟替代股票
        alternatives = [
            {
                "code": "000002",
                "name": "万科A",
                "sector": "房地产",
                "reason": "同板块估值较低",
                "risk": "中"
            },
            {
                "code": "600036",
                "name": "招商银行",
                "sector": "金融",
                "reason": "行业龙头，稳定性好",
                "risk": "低"
            },
            {
                "code": "000333",
                "name": "美的集团",
                "sector": "消费",
                "reason": "防御性较强",
                "risk": "中低"
            }
        ]

        return alternatives

    def format_output(self, result: Dict) -> str:
        """格式化输出结果"""
        if not result.get("success", False):
            return f"❌ 生成投资建议失败"

        output = []
        output.append("=" * 60)
        output.append(f"💰 投资建议报告")
        output.append("=" * 60)

        # 股票信息
        output.append(f"📈 股票信息:")
        output.append(f"  代码：{result['stock_code']}")
        output.append(f"  名称：{result['stock_name']}")
        output.append(f"  当前价：¥{result['current_price']:.2f}")
        output.append(f"  建议日期：{result['advice_date'][:10]}")

        # 用户配置
        output.append(f"\n👤 用户配置:")
        profile = result['user_profile']
        output.append(f"  风险偏好：{profile.get('risk_tolerance', '平衡型')}")
        output.append(f"  投资期限：{profile.get('investment_horizon', '中期')}")
        output.append(f"  资金规模：¥{profile.get('capital', 0):,.0f}")

        # 市场环境
        market = result['market_environment']
        output.append(f"\n🌍 市场环境:")
        output.append(f"  当前环境：{market.get('name', '中性')}")
        output.append(f"  风险评估：{market.get('risk_appetite', '中')}")
        output.append(f"  关注板块：{', '.join(market.get('sector_focus', []))}")

        # 投资策略
        strategy = result['investment_strategy']
        output.append(f"\n🎯 投资策略:")
        output.append(f"  策略类型：{strategy.get('name', '平衡型')}")
        output.append(f"  策略描述：{strategy.get('description', '')}")
        output.append(f"  持仓周期：{strategy.get('holding_period', '中期')}")

        # 具体建议
        advice = result['specific_advice']
        output.append(f"\n💡 具体建议:")
        output.append(f"  核心操作：{advice.get('core_action', '')}")
        output.append(f"  信心水平：{advice.get('confidence_level', '中')}")
        output.append(f"  操作时机：{advice.get('timing', '')}")
        output.append(f"  仓位建议：{advice.get('position', '')}")

        # 目标价位
        targets = result['target_prices']
        output.append(f"\n🎯 目标价位:")
        output.append(f"  止损价位：¥{targets.get('stop_loss', 0):.2f}")
        output.append(f"  止盈价位：¥{targets.get('take_profit', 0):.2f}")
        output.append(f"  支撑价位：¥{targets.get('support_level', 0):.2f}")
        output.append(f"  阻力价位：¥{targets.get('resistance_level', 0):.2f}")
        output.append(f"  风险收益比：{targets.get('risk_reward_ratio', 0):.2f}")

        # 风险评估
        risk = result['risk_assessment']
        output.append(f"\n⚠️  风险评估:")
        output.append(f"  总体风险：{risk.get('overall_risk', '中')}")
        output.append(f"  风险评分：{risk.get('risk_score', 50)}/100")
        if risk.get('risk_factors'):
            output.append(f"  风险因素：{', '.join(risk['risk_factors'])}")

        # 仓位计算
        position = result['position_sizing']
        output.append(f"\n📊 仓位计算:")
        output.append(f"  建议仓位：{position.get('adjusted_position_percentage', 0)}%")
        output.append(f"  建议金额：¥{position.get('suggested_amount', 0):,.0f}")

        # 监控计划
        output.append(f"\n🔍 监控计划:")
        for i, item in enumerate(result.get('monitoring_plan', []), 1):
            output.append(f"  {i}. {item}")

        # 替代选项
        output.append(f"\n🔄 替代选项:")
        for alt in result.get('alternative_options', [])[:2]:
            output.append(f"  {alt['name']}({alt['code']}) - {alt['sector']}板块，{alt['reason']}")

        output.append("=" * 60)

        return "\n".join(output)


def main():
    """主函数 - 演示使用"""
    advisor = InvestmentAdvisor()

    print("\n💰 投资建议生成 Skill 演示")
    print("=" * 60)

    # 示例趋势分析数据
    sample_trend_analysis = {
        "success": True,
        "stock_code": "000001",
        "stock_name": "平安银行",
        "score": 72.5,
        "trend": "上升",
        "recommendation": "买入",
        "support_level": 15.50,
        "resistance_level": 16.20,
        "risk_level": "低"
    }

    # 用户配置
    user_profile = {
        "risk_tolerance": "平衡型",
        "investment_horizon": "中期",
        "capital": 100000
    }

    print("\n1. 为平安银行生成投资建议:")
    result = advisor.generate_advice(
        stock_code="000001",
        stock_name="平安银行",
        current_price=15.88,
        trend_analysis=sample_trend_analysis,
        user_profile=user_profile
    )

    print(advisor.format_output(result))

    # 不同风险偏好的示例
    print("\n2. 不同风险偏好对比:")

    profiles = [
        {"risk_tolerance": "保守型", "investment_horizon": "长期", "capital": 100000},
        {"risk_tolerance": "平衡型", "investment_horizon": "中期", "capital": 100000},
        {"risk_tolerance": "积极型", "investment_horizon": "短期", "capital": 100000}
    ]

    for profile in profiles:
        result = advisor.generate_advice(
            stock_code="000001",
            stock_name="平安银行",
            current_price=15.88,
            trend_analysis=sample_trend_analysis,
            user_profile=profile
        )
        strategy = result['investment_strategy']['name']
        position = result['position_sizing']['adjusted_position_percentage']
        print(f"  {profile['risk_tolerance']}: 策略={strategy}, 仓位={position}%")

    print("\n✅ 演示完成！")


if __name__ == "__main__":
    main()

