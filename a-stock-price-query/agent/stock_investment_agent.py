#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票投资顾问 Agent
功能：智能协调多个Skills，提供端到端的股票投资咨询服务
与Skill的区别：
- Skill: 单一功能（如查询价格、分析趋势）
- Agent: 组合多个Skills，具有对话管理、决策制定、上下文理解能力
"""

import logging
import os
import sys
from datetime import datetime
from typing import Dict, List

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入Skills
try:
    from skills.stock_price_query.skill import StockPriceQuery
    from skills.trend_analyzer.skill import StockTrendAnalyzer
    from skills.investment_advisor.skill import InvestmentAdvisor
    from skills.dialog_manager.skill import DialogManager
    print("✅ 所有Skills导入成功")
except ImportError as e:
    print(f"⚠️  Skills导入失败: {e}")
    print("正在创建模拟Skills...")

    # 创建模拟类以防导入失败
    class StockPriceQuery:
        def query(self, code): return {"success": True, "stock_code": code, "stock_name": "模拟股票"}
        def format_output(self, result): return f"模拟输出: {result}"

    class StockTrendAnalyzer:
        def analyze_trend(self, code): return {"success": True, "score": 75, "trend": "上升"}
        def format_output(self, result): return f"模拟趋势: {result}"

    class InvestmentAdvisor:
        def generate_advice(self, **kwargs): return {"success": True, "advice": "模拟建议"}
        def format_output(self, result): return f"模拟建议: {result}"

    class DialogManager:
        def create_conversation(self, user_id, ctx): return {"conversation_id": "sim"}
        def update_conversation(self, *args): return {"state": "active"}
        def get_conversation_context(self, conv_id): return {"state": "active"}
        def suggest_next_action(self, conv_id): return {"action": "continue"}


class StockInvestmentAgent:
    """股票投资顾问 Agent"""

    def __init__(self, agent_name: str = "股票投资助手", log_level: str = "INFO"):
        """初始化Agent

        Args:
            agent_name: Agent名称
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.agent_name = agent_name
        self.version = "1.0.0"
        self.description = "智能股票投资顾问，整合多个Skills提供全面服务"

        # 配置日志
        self._setup_logging(log_level)
        self.logger = logging.getLogger(f"{__name__}.{self.agent_name}")
        self.logger.info(f"🚀 初始化 {self.agent_name}...")
        self.logger.info("=" * 60)

        # 核心Skills
        self.price_query = StockPriceQuery()
        self.logger.info("✅ 价格查询Skill已加载")

        self.trend_analyzer = StockTrendAnalyzer()
        self.logger.info("✅ 趋势分析Skill已加载")

        self.investment_advisor = InvestmentAdvisor()
        self.logger.info("✅ 投资建议Skill已加载")

        self.dialog_manager = DialogManager()
        self.logger.info("✅ 对话管理Skill已加载")

        # Agent状态
        self.active_conversations = {}
        self.skill_usage_stats = {
            "price_query": 0,
            "trend_analyzer": 0,
            "investment_advisor": 0,
            "dialog_manager": 0
        }

        # 决策规则
        self.decision_rules = self._load_decision_rules()

        self.logger.info("=" * 60)
        self.logger.info(f"✅ {self.agent_name} 初始化完成！")
        self.logger.info(f"📊 可用Skills: {len(self.skill_usage_stats)}个")

    def _setup_logging(self, log_level: str) -> None:
        """配置日志系统

        Args:
            log_level: 日志级别字符串 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        # 配置根日志记录器
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

        # 设置日志级别
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=numeric_level,
            format=log_format,
            datefmt=date_format
        )

        # 为当前模块设置级别
        logging.getLogger(__name__).setLevel(numeric_level)

    def _load_decision_rules(self) -> Dict:
        """加载决策规则"""
        return {
            "greeting": {
                "skills": ["dialog_manager"],
                "action": "欢迎用户并询问需求"
            },
            "stock_query": {
                "skills": ["price_query"],
                "action": "查询股票价格信息",
                "requires": ["stock_code_or_name"]
            },
            "trend_request": {
                "skills": ["trend_analyzer", "price_query"],
                "action": "分析股票趋势",
                "requires": ["stock_code_or_name"]
            },
            "advice_request": {
                "skills": ["investment_advisor", "trend_analyzer", "price_query"],
                "action": "生成投资建议",
                "requires": ["stock_code_or_name", "user_profile"]
            },
            "comparison_request": {
                "skills": ["trend_analyzer", "price_query"],
                "action": "比较多只股票",
                "requires": ["stock_list"]
            },
            "follow_up": {
                "skills": ["dialog_manager", "trend_analyzer"],
                "action": "处理跟进问题"
            }
        }

    def start_conversation(self, user_id: str, initial_message: str) -> Dict:
        """
        开始新对话

        Args:
            user_id: 用户ID
            initial_message: 初始消息

        Returns:
            对话响应
        """
        print(f"\n💬 开始与用户 {user_id} 的对话")
        print(f"📝 用户消息: {initial_message}")

        # 创建对话
        conversation = self.dialog_manager.create_conversation(user_id, {
            "agent_name": self.agent_name,
            "start_time": datetime.now().isoformat()
        })

        conv_id = conversation["conversation_id"]
        self.active_conversations[conv_id] = {
            "user_id": user_id,
            "start_time": datetime.now().isoformat(),
            "message_count": 0
        }

        self.skill_usage_stats["dialog_manager"] += 1

        # 处理消息
        return self.process_message(conv_id, initial_message)

    def process_message(self, conversation_id: str, user_message: str) -> Dict:
        """
        处理用户消息

        Args:
            conversation_id: 对话ID
            user_message: 用户消息

        Returns:
            处理结果
        """
        print(f"\n📨 处理消息 (对话 {conversation_id}):")
        print(f"  用户: {user_message}")

        # 更新对话状态
        initial_response = f"收到您的消息: {user_message[:50]}..."
        conversation = self.dialog_manager.update_conversation(
            conversation_id, user_message, initial_response
        )

        self.skill_usage_stats["dialog_manager"] += 1

        # 分析用户意图
        intent_analysis = self._analyze_intent(user_message, conversation)
        print(f"  分析结果: 意图={intent_analysis['primary_intent']}, 置信度={intent_analysis['confidence']}")

        # 决策：选择使用哪些Skills
        decision = self._make_decision(intent_analysis, conversation)
        print(f"  决策: 使用{len(decision['skills_to_use'])}个Skills: {decision['skills_to_use']}")

        # 执行Skills
        execution_results = self._execute_skills(decision, user_message, conversation)

        # 生成响应
        final_response = self._generate_response(execution_results, intent_analysis, conversation)

        # 更新对话状态
        final_conversation = self.dialog_manager.update_conversation(
            conversation_id, user_message, final_response, decision["next_state"]
        )

        # 更新统计数据
        if conversation_id in self.active_conversations:
            self.active_conversations[conversation_id]["message_count"] += 1

        # 返回结果
        result = {
            "success": True,
            "conversation_id": conversation_id,
            "user_message": user_message,
            "agent_response": final_response,
            "intent_analysis": intent_analysis,
            "decision": decision,
            "execution_summary": {
                "skills_used": decision["skills_to_use"],
                "results_count": len(execution_results)
            },
            "conversation_state": final_conversation["state"],
            "timestamp": datetime.now().isoformat()
        }

        print(f"  响应生成: {final_response[:80]}...")

        return result

    def _analyze_intent(self, user_message: str, conversation: Dict) -> Dict:
        """分析用户意图"""
        message_lower = user_message.lower()

        # 意图关键词映射
        intent_keywords = {
            "greeting": ["你好", "嗨", "早上好", "下午好", "hello", "hi"],
            "stock_query": ["查询", "价格", "收盘价", "股价", "多少钱", "stock", "price"],
            "trend_request": ["趋势", "走势", "分析", "技术分析", "未来", "预测", "trend"],
            "advice_request": ["建议", "投资", "买入", "卖出", "持有", "操作", "买不买", "advice"],
            "comparison_request": ["比较", "对比", "哪个好", "推荐", "首选", "compare"],
            "follow_up": ["还有", "另外", "其他", "再问", "追问", "follow up"],
            "closing": ["谢谢", "再见", "拜拜", "结束", "退出", "thanks", "bye"]
        }

        # 检测意图
        detected_intents = []
        for intent, keywords in intent_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    detected_intents.append(intent)
                    break

        # 确定主要意图
        primary_intent = "follow_up"
        confidence = 0.5

        if detected_intents:
            primary_intent = detected_intents[0]
            confidence = 0.8
        elif any(word in message_lower for word in ["股票", "代码", "投资"]):
            primary_intent = "stock_query"
            confidence = 0.7

        # 提取实体
        entities = self._extract_entities(user_message)

        return {
            "primary_intent": primary_intent,
            "all_intents": detected_intents,
            "confidence": confidence,
            "entities": entities,
            "message_length": len(user_message),
            "contains_stock_reference": any(e["type"] == "stock_code" for e in entities)
        }

    def _extract_entities(self, message: str) -> List[Dict]:
        """提取实体"""
        entities = []

        # 简单实体提取（实际应用中可以使用更复杂的NLP）
        import re

        # 股票代码
        stock_codes = re.findall(r'\b[0-9]{6}\b', message)
        for code in stock_codes:
            entities.append({"type": "stock_code", "value": code, "source": "regex"})

        # 常见股票名称
        stock_names = ["平安银行", "五粮液", "浦发银行", "茅台", "招商银行", "万科"]
        for name in stock_names:
            if name in message:
                entities.append({"type": "stock_name", "value": name, "source": "keyword"})

        # 价格
        prices = re.findall(r'¥?\d+(?:\.\d+)?元?', message)
        for price in prices:
            entities.append({"type": "price", "value": price, "source": "regex"})

        # 风险偏好
        risk_keywords = {
            "保守": "conservative",
            "稳健": "moderate",
            "平衡": "balanced",
            "积极": "aggressive",
            "激进": "aggressive"
        }

        for kw, risk_type in risk_keywords.items():
            if kw in message:
                entities.append({"type": "risk_preference", "value": risk_type, "source": "keyword"})

        return entities

    def _make_decision(self, intent_analysis: Dict, conversation: Dict) -> Dict:
        """做出决策"""
        primary_intent = intent_analysis["primary_intent"]

        # 获取决策规则
        if primary_intent in self.decision_rules:
            rule = self.decision_rules[primary_intent]
        else:
            rule = self.decision_rules["follow_up"]

        # 检查前提条件
        missing_requirements = []
        if "requires" in rule:
            for req in rule["requires"]:
                # 简化检查，实际中需要更复杂的逻辑
                if req == "stock_code_or_name" and not intent_analysis["contains_stock_reference"]:
                    missing_requirements.append(req)

        # 确定下一步状态
        if missing_requirements:
            next_state = "clarification"
            action = f"需要更多信息: {', '.join(missing_requirements)}"
            skills_to_use = ["dialog_manager"]
        else:
            next_state = primary_intent
            action = rule["action"]
            skills_to_use = rule["skills"]

        return {
            "intent": primary_intent,
            "action": action,
            "skills_to_use": skills_to_use,
            "next_state": next_state,
            "missing_requirements": missing_requirements,
            "rule_applied": rule.get("action", "未知")
        }

    def _execute_skills(self, decision: Dict, user_message: str, conversation: Dict) -> Dict:
        """执行Skills"""
        results = {}
        skills_to_use = decision["skills_to_use"]

        print(f"  🔧 执行Skills: {skills_to_use}")

        # 提取股票信息
        stock_entity = None
        for entity in conversation.get("entities", []):
            if entity["type"] in ["stock_code", "stock_name"]:
                stock_entity = entity
                break

        stock_code_or_name = stock_entity["value"] if stock_entity else None

        # 执行每个Skill
        for skill_name in skills_to_use:
            try:
                if skill_name == "price_query" and stock_code_or_name:
                    print(f"    📊 执行价格查询: {stock_code_or_name}")
                    result = self.price_query.query(stock_code_or_name)
                    results["price_query"] = result
                    self.skill_usage_stats["price_query"] += 1

                elif skill_name == "trend_analyzer" and stock_code_or_name:
                    print(f"    📈 执行趋势分析: {stock_code_or_name}")
                    result = self.trend_analyzer.analyze_trend(stock_code_or_name)
                    results["trend_analyzer"] = result
                    self.skill_usage_stats["trend_analyzer"] += 1

                elif skill_name == "investment_advisor" and stock_code_or_name:
                    print(f"    💰 生成投资建议: {stock_code_or_name}")

                    # 获取趋势分析结果
                    trend_result = results.get("trend_analyzer")
                    if not trend_result and "trend_analyzer" in skills_to_use:
                        # 如果还没执行趋势分析，先执行
                        trend_result = self.trend_analyzer.analyze_trend(stock_code_or_name)
                        results["trend_analyzer"] = trend_result

                    # 获取价格信息
                    price_result = results.get("price_query")
                    if not price_result:
                        price_result = self.price_query.query(stock_code_or_name)
                        results["price_query"] = price_result

                    # 提取当前价格（简化处理）
                    current_price = 15.88  # 默认值
                    if price_result.get("success") and price_result.get("data"):
                        current_price = price_result["data"][0].get("close_price", current_price)

                    # 生成建议
                    result = self.investment_advisor.generate_advice(
                        stock_code=stock_code_or_name,
                        stock_name=price_result.get("stock_name", "未知"),
                        current_price=current_price,
                        trend_analysis=trend_result if trend_result else {"score": 50},
                        user_profile={"risk_tolerance": "平衡型", "capital": 100000}
                    )
                    results["investment_advisor"] = result
                    self.skill_usage_stats["investment_advisor"] += 1

                elif skill_name == "dialog_manager":
                    # 对话管理已在外部处理
                    results["dialog_manager"] = {
                        "state": conversation.get("state"),
                        "context": self.dialog_manager.get_conversation_context(conversation["conversation_id"])
                    }

            except Exception as e:
                print(f"    ❌ Skill执行失败 {skill_name}: {e}")
                results[skill_name] = {"success": False, "error": str(e)}

        return results

    def _generate_response(self, execution_results: Dict, intent_analysis: Dict, conversation: Dict) -> str:
        """生成响应"""
        primary_intent = intent_analysis["primary_intent"]

        # 根据意图和结果生成响应
        response_parts = []

        # 问候响应
        if primary_intent == "greeting":
            response_parts.append(f"👋 您好！我是{self.agent_name}，您的股票投资顾问。")
            response_parts.append("我可以帮助您：查询股票价格、分析趋势、提供投资建议。")
            response_parts.append("请问您需要什么帮助？")

        # 股票查询响应
        elif primary_intent == "stock_query":
            price_result = execution_results.get("price_query")
            if price_result and price_result.get("success"):
                formatted = self.price_query.format_output(price_result)
                response_parts.append("📊 查询结果如下：")
                response_parts.append(formatted)
            else:
                response_parts.append("❌ 查询失败，请确认股票代码或名称是否正确。")
                response_parts.append("💡 支持的股票示例：平安银行(000001)、五粮液(000858)、浦发银行(600000)")

        # 趋势分析响应
        elif primary_intent == "trend_request":
            trend_result = execution_results.get("trend_analyzer")
            if trend_result and trend_result.get("success"):
                formatted = self.trend_analyzer.format_output(trend_result)
                response_parts.append("📈 趋势分析结果如下：")
                response_parts.append(formatted)
            else:
                response_parts.append("❌ 趋势分析失败，请确认股票信息。")

        # 投资建议响应
        elif primary_intent == "advice_request":
            advice_result = execution_results.get("investment_advisor")
            if advice_result and advice_result.get("success"):
                formatted = self.investment_advisor.format_output(advice_result)
                response_parts.append("💰 投资建议如下：")
                response_parts.append(formatted)
            else:
                response_parts.append("❌ 投资建议生成失败。")

        # 比较请求响应
        elif primary_intent == "comparison_request":
            response_parts.append("📊 股票比较功能需要具体的股票列表。")
            response_parts.append("💡 请告诉我您想比较哪些股票，例如：\"比较平安银行和五粮液\"")

        # 跟进问题响应
        elif primary_intent == "follow_up":
            # 基于对话历史生成响应
            context = self.dialog_manager.get_conversation_context(conversation["conversation_id"])
            missing_info = context.get("missing_info", [])

            if missing_info:
                response_parts.append(f"🤔 要回答这个问题，我还需要：{', '.join(missing_info)}")
            else:
                response_parts.append("🔍 我正在分析您的问题，请稍等...")

                # 如果有之前的股票信息，提供更多分析
                if execution_results.get("trend_analyzer"):
                    trend_result = execution_results["trend_analyzer"]
                    if trend_result.get("success"):
                        score = trend_result.get("score", 50)
                        if score >= 70:
                            response_parts.append("💡 基于之前的分析，这只股票表现不错，值得关注。")
                        elif score <= 30:
                            response_parts.append("⚠️  基于之前的分析，这只股票风险较高，建议谨慎。")

        # 结束对话响应
        elif primary_intent == "closing":
            response_parts.append("👋 感谢使用股票投资顾问服务！")
            response_parts.append("📈 祝您投资顺利，再见！")

        # 默认响应
        else:
            response_parts.append("🤔 我理解您的问题了。")

            if intent_analysis["contains_stock_reference"]:
                response_parts.append("📊 正在为您分析相关股票信息...")
                response_parts.append("💡 您可以说：\"查询[股票]价格\"、\"分析[股票]趋势\"、\"[股票]投资建议\"")
            else:
                response_parts.append("💡 您可以：查询股票价格、分析趋势、获取投资建议。")
                response_parts.append("例如：\"平安银行最近怎么样\"、\"分析五粮液趋势\"、\"浦发银行投资建议\"")

        # 添加对话连续性
        if primary_intent not in ["closing", "greeting"]:
            suggestion = self.dialog_manager.suggest_next_action(conversation["conversation_id"])
            if suggestion.get("prompt"):
                response_parts.append(f"\n❓ {suggestion['prompt']}")

        return "\n".join(response_parts)

    def get_agent_status(self) -> Dict:
        """获取Agent状态"""
        return {
            "agent_name": self.agent_name,
            "version": self.version,
            "description": self.description,
            "active_conversations": len(self.active_conversations),
            "skill_usage": self.skill_usage_stats,
            "total_messages": sum(conv["message_count"] for conv in self.active_conversations.values()),
            "uptime": self._get_uptime(),
            "decision_rules": list(self.decision_rules.keys())
        }

    def _get_uptime(self) -> str:
        """获取运行时间（简化版本）"""
        if hasattr(self, "_start_time"):
            from datetime import datetime
            uptime = datetime.now() - self._start_time
            hours = uptime.seconds // 3600
            minutes = (uptime.seconds % 3600) // 60
            return f"{hours}小时{minutes}分钟"
        return "未知"

    def demo_conversation(self):
        """演示对话流程"""
        print("\n" + "=" * 70)
        print(f"🤖 {self.agent_name} 演示对话")
        print("=" * 70)

        # 开始对话
        print("\n【场景1：新用户问候】")
        result1 = self.start_conversation("demo_user", "你好，我想了解股票投资")
        print(f"用户: {result1['user_message']}")
        print(f"助手: {result1['agent_response'][:100]}...")

        print("\n【场景2：查询股票价格】")
        result2 = self.process_message(result1['conversation_id'], "平安银行最近价格怎么样？")
        print(f"用户: {result2['user_message']}")
        print(f"助手: {result2['agent_response'][:150]}...")

        print("\n【场景3：分析趋势】")
        result3 = self.process_message(result1['conversation_id'], "帮我分析一下它的趋势")
        print(f"用户: {result3['user_message']}")
        print(f"助手: {result3['agent_response'][:150]}...")

        print("\n【场景4：投资建议】")
        result4 = self.process_message(result1['conversation_id'], "那应该怎么操作？风险偏好保守")
        print(f"用户: {result4['user_message']}")
        print(f"助手: {result4['agent_response'][:200]}...")

        print("\n【场景5：结束对话】")
        result5 = self.process_message(result1['conversation_id'], "谢谢，再见")
        print(f"用户: {result5['user_message']}")
        print(f"助手: {result5['agent_response']}")

        # 显示Agent状态
        print("\n" + "=" * 70)
        print("📊 Agent状态统计")
        print("=" * 70)
        status = self.get_agent_status()
        for key, value in status.items():
            print(f"  {key}: {value}")

        print("\n✅ 演示完成！")


def main():
    """主函数 - 运行Agent演示"""
    print("\n🚀 启动股票投资顾问 Agent")
    print("=" * 60)
    print("💡 注意：Agent与Skill的区别：")
    print("  • Skill: 单一功能，如查询价格、分析趋势")
    print("  • Agent: 整合多个Skills，具备对话管理、决策制定能力")
    print("=" * 60)

    # 创建Agent实例
    agent = StockInvestmentAgent("智能股票投资顾问")

    # 运行演示
    agent.demo_conversation()

    # 保存Agent配置
    print("\n💾 Agent配置已准备就绪")
    print("📁 项目结构:")
    print("  a-stock-price-query/")
    print("  ├── agent/                    # Agent实现")
    print("  │   └── stock_investment_agent.py")
    print("  ├── skills/                   # 多个Skills")
    print("  │   ├── trend_analyzer.py")
    print("  │   ├── investment_advisor.py")
    print("  │   └── dialog_manager.py")
    print("  ├── fetch_stock_price.py      # 现有价格查询Skill")
    print("  └── ...")

    print("\n🎯 下一步：")
    print("  1. 部署到Agent广场")
    print("  2. 配置catpaw-deploy.yaml")
    print("  3. 测试完整流程")

    return agent


if __name__ == "__main__":
    main()

