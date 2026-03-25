#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话状态管理 Skill
功能：管理对话上下文，维护用户状态，支持多轮对话
"""

import time
from datetime import datetime
from typing import Dict, List, Optional


class DialogManager:
    """对话状态管理 Skill"""

    def __init__(self):
        """初始化对话管理器"""
        # 对话状态存储
        self.conversations = {}
        # 用户偏好存储
        self.user_profiles = {}
        # 对话历史
        self.dialog_history = {}

        # 对话状态定义
        self.dialog_states = {
            "greeting": "问候",
            "stock_query": "股票查询",
            "trend_analysis": "趋势分析",
            "investment_advice": "投资建议",
            "comparison": "股票比较",
            "follow_up": "跟进问题",
            "closing": "结束对话"
        }

        # 意图识别关键词
        self.intent_keywords = {
            "stock_query": ["查询", "价格", "收盘价", "股票", "代码"],
            "trend_analysis": ["趋势", "分析", "走势", "技术分析", "预测"],
            "investment_advice": ["建议", "投资", "买入", "卖出", "持有", "操作"],
            "comparison": ["比较", "对比", "哪个好", "推荐", "首选"],
            "greeting": ["你好", "嗨", "早上好", "下午好", "晚上好"],
            "closing": ["谢谢", "再见", "拜拜", "结束", "退出"]
        }

    def create_conversation(self, user_id: str, initial_context: Optional[Dict] = None) -> Dict:
        """
        创建新对话

        Args:
            user_id: 用户ID
            initial_context: 初始上下文

        Returns:
            对话状态字典
        """
        conversation_id = f"{user_id}_{int(time.time())}"

        conversation = {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "state": "greeting",
            "context": initial_context or {},
            "history": [],
            "slots": {},  # 对话槽位（需要收集的信息）
            "intents": [],
            "entities": []
        }

        self.conversations[conversation_id] = conversation
        self.dialog_history[conversation_id] = []

        # 初始化用户配置（如果不存在）
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "risk_tolerance": "平衡型",
                "investment_horizon": "中期",
                "preferred_sectors": [],
                "conversation_count": 0
            }

        return conversation

    def update_conversation(self, conversation_id: str, user_message: str,
                           bot_response: str, new_state: Optional[str] = None) -> Dict:
        """
        更新对话状态

        Args:
            conversation_id: 对话ID
            user_message: 用户消息
            bot_response: 机器人回复
            new_state: 新状态（可选）

        Returns:
            更新后的对话状态
        """
        if conversation_id not in self.conversations:
            return self.create_conversation("unknown", {})

        conversation = self.conversations[conversation_id]

        # 识别意图
        intents = self._detect_intents(user_message)

        # 提取实体
        entities = self._extract_entities(user_message)

        # 更新对话历史
        dialog_turn = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": bot_response,
            "detected_intents": intents,
            "extracted_entities": entities
        }

        conversation["history"].append(dialog_turn)
        self.dialog_history[conversation_id].append(dialog_turn)

        # 更新状态
        if new_state:
            conversation["state"] = new_state
        elif intents:
            # 根据意图自动更新状态
            primary_intent = intents[0]
            if primary_intent in self.dialog_states:
                conversation["state"] = primary_intent

        # 更新槽位
        self._update_slots(conversation, entities, user_message)

        # 更新用户偏好
        self._update_user_profile(conversation["user_id"], entities, intents)

        conversation["updated_at"] = datetime.now().isoformat()
        conversation["intents"] = intents
        conversation["entities"] = entities

        return conversation

    def _detect_intents(self, message: str) -> List[str]:
        """检测意图"""
        message_lower = message.lower()
        detected_intents = []

        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    detected_intents.append(intent)
                    break

        # 如果没有检测到意图，尝试基于内容推断
        if not detected_intents:
            if any(word in message_lower for word in ["股票", "代码", "价格"]):
                detected_intents.append("stock_query")
            elif any(word in message_lower for word in ["怎么样", "如何", "建议"]):
                detected_intents.append("investment_advice")
            else:
                detected_intents.append("follow_up")

        return detected_intents

    def _extract_entities(self, message: str) -> List[Dict]:
        """提取实体"""
        entities = []

        # 股票代码模式（6位数字）
        import re
        stock_code_pattern = r'\b[0-9]{6}\b'
        stock_codes = re.findall(stock_code_pattern, message)

        for code in stock_codes:
            entities.append({
                "type": "stock_code",
                "value": code,
                "confidence": 0.9
            })

        # 常见股票名称
        stock_names = ["平安银行", "五粮液", "浦发银行", "茅台", "招商银行", "万科"]
        for name in stock_names:
            if name in message:
                entities.append({
                    "type": "stock_name",
                    "value": name,
                    "confidence": 0.8
                })

        # 价格相关
        price_pattern = r'¥?\d+(?:\.\d+)?元?'
        prices = re.findall(price_pattern, message)
        for price in prices:
            entities.append({
                "type": "price",
                "value": price,
                "confidence": 0.7
            })

        # 时间相关
        time_keywords = ["今天", "昨天", "本周", "本月", "最近", "5日", "10日"]
        for keyword in time_keywords:
            if keyword in message:
                entities.append({
                    "type": "time_period",
                    "value": keyword,
                    "confidence": 0.6
                })

        return entities

    def _update_slots(self, conversation: Dict, entities: List[Dict], message: str):
        """更新对话槽位"""
        slots = conversation.get("slots", {})

        for entity in entities:
            entity_type = entity["type"]
            entity_value = entity["value"]

            if entity_type == "stock_code":
                slots["stock_code"] = entity_value
            elif entity_type == "stock_name":
                slots["stock_name"] = entity_value
            elif entity_type == "time_period":
                slots["time_period"] = entity_value
            elif entity_type == "price" and "target_price" not in slots:
                slots["target_price"] = entity_value

        # 从消息中提取其他信息
        if "风险" in message and "risk_tolerance" not in slots:
            if "高" in message or "激进" in message:
                slots["risk_tolerance"] = "积极型"
            elif "低" in message or "保守" in message:
                slots["risk_tolerance"] = "保守型"
            else:
                slots["risk_tolerance"] = "平衡型"

        conversation["slots"] = slots

    def _update_user_profile(self, user_id: str, entities: List[Dict], intents: List[str]):
        """更新用户偏好"""
        if user_id not in self.user_profiles:
            return

        profile = self.user_profiles[user_id]
        profile["conversation_count"] = profile.get("conversation_count", 0) + 1

        # 根据对话内容更新偏好
        for entity in entities:
            if entity["type"] == "stock_code":
                # 记录用户关注的股票
                if "watched_stocks" not in profile:
                    profile["watched_stocks"] = []
                if entity["value"] not in profile["watched_stocks"]:
                    profile["watched_stocks"].append(entity["value"])

        # 根据意图更新偏好
        if "investment_advice" in intents:
            profile["interest_areas"] = profile.get("interest_areas", [])
            if "投资建议" not in profile["interest_areas"]:
                profile["interest_areas"].append("投资建议")

        if "trend_analysis" in intents:
            profile["interest_areas"] = profile.get("interest_areas", [])
            if "技术分析" not in profile["interest_areas"]:
                profile["interest_areas"].append("技术分析")

    def get_conversation_context(self, conversation_id: str) -> Dict:
        """获取对话上下文"""
        if conversation_id not in self.conversations:
            return {}

        conversation = self.conversations[conversation_id]

        # 构建上下文摘要
        context_summary = {
            "current_state": conversation["state"],
            "state_description": self.dialog_states.get(conversation["state"], "未知"),
            "slots": conversation["slots"],
            "recent_intents": conversation.get("intents", [])[-3:],
            "recent_entities": conversation.get("entities", [])[-5:],
            "history_length": len(conversation["history"]),
            "user_profile": self.user_profiles.get(conversation["user_id"], {}),
            "missing_info": self._identify_missing_info(conversation)
        }

        return context_summary

    def _identify_missing_info(self, conversation: Dict) -> List[str]:
        """识别缺失信息"""
        missing = []
        state = conversation["state"]
        slots = conversation.get("slots", {})

        if state == "stock_query":
            if not slots.get("stock_code") and not slots.get("stock_name"):
                missing.append("股票代码或名称")

        elif state == "trend_analysis":
            if not slots.get("stock_code") and not slots.get("stock_name"):
                missing.append("股票代码或名称")
            if not slots.get("time_period"):
                missing.append("分析时间周期")

        elif state == "investment_advice":
            if not slots.get("stock_code") and not slots.get("stock_name"):
                missing.append("股票代码或名称")
            if not slots.get("risk_tolerance"):
                missing.append("风险偏好")

        return missing

    def suggest_next_action(self, conversation_id: str) -> Dict:
        """建议下一步动作"""
        if conversation_id not in self.conversations:
            return {"suggestion": "创建新对话"}

        conversation = self.conversations[conversation_id]
        state = conversation["state"]
        missing_info = self._identify_missing_info(conversation)

        suggestions = {
            "greeting": {
                "action": "询问用户需求",
                "prompt": "您好！我是股票投资助手。请问您想查询股票信息，还是需要投资建议？",
                "expected_response": "股票查询或投资建议"
            },
            "stock_query": {
                "action": "询问股票代码或名称",
                "prompt": "请问您想查询哪只股票？可以告诉我股票代码或名称。",
                "expected_response": "股票代码或名称"
            },
            "trend_analysis": {
                "action": "询问分析参数",
                "prompt": f"请问您想分析哪只股票的什么时间周期趋势？",
                "expected_response": "股票和时间周期"
            },
            "investment_advice": {
                "action": "收集投资偏好",
                "prompt": "为了给您提供更精准的建议，请告诉我您的风险偏好（保守/平衡/积极）和投资金额。",
                "expected_response": "风险偏好和投资金额"
            },
            "follow_up": {
                "action": "继续对话",
                "prompt": "您还有其他问题吗？",
                "expected_response": "是/否或新问题"
            },
            "closing": {
                "action": "结束对话",
                "prompt": "感谢使用！再见！",
                "expected_response": "无"
            }
        }

        suggestion = suggestions.get(state, suggestions["follow_up"])

        # 如果有缺失信息，调整建议
        if missing_info and state != "greeting":
            missing_text = "、".join(missing_info)
            suggestion = {
                "action": "收集缺失信息",
                "prompt": f"需要补充信息：{missing_text}。请提供这些信息以便继续。",
                "expected_response": missing_text,
                "missing_info": missing_info
            }

        # 添加上下文信息
        suggestion.update({
            "current_state": state,
            "conversation_history_length": len(conversation["history"]),
            "user_profile": self.user_profiles.get(conversation["user_id"], {})
        })

        return suggestion

    def get_conversation_summary(self, conversation_id: str) -> Dict:
        """获取对话摘要"""
        if conversation_id not in self.conversations:
            return {"error": "对话不存在"}

        conversation = self.conversations[conversation_id]

        summary = {
            "conversation_id": conversation_id,
            "user_id": conversation["user_id"],
            "duration": self._calculate_duration(conversation["created_at"]),
            "turn_count": len(conversation["history"]),
            "current_state": conversation["state"],
            "main_topics": self._extract_main_topics(conversation["history"]),
            "user_profile": self.user_profiles.get(conversation["user_id"], {}),
            "slots_filled": conversation.get("slots", {}),
            "recommended_next": self.suggest_next_action(conversation_id)
        }

        return summary

    def _calculate_duration(self, created_at: str) -> str:
        """计算对话持续时间"""
        try:
            created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            now = datetime.now()
            duration = now - created

            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60

            if duration.days > 0:
                return f"{duration.days}天{hours}小时"
            elif hours > 0:
                return f"{hours}小时{minutes}分钟"
            else:
                return f"{minutes}分钟"
        except:
            return "未知"

    def _extract_main_topics(self, history: List[Dict]) -> List[str]:
        """提取主要话题"""
        topics = []

        for turn in history[-5:]:  # 最近5轮
            intents = turn.get("detected_intents", [])
            for intent in intents:
                if intent in self.dialog_states:
                    topic = self.dialog_states[intent]
                    if topic not in topics:
                        topics.append(topic)

        return topics

    def format_conversation_history(self, conversation_id: str, max_turns: int = 10) -> str:
        """格式化对话历史"""
        if conversation_id not in self.dialog_history:
            return "无对话历史"

        history = self.dialog_history[conversation_id][-max_turns:]

        formatted = []
        formatted.append("=" * 60)
        formatted.append(f"💬 对话历史 (最近{len(history)}轮)")
        formatted.append("=" * 60)

        for i, turn in enumerate(history, 1):
            formatted.append(f"\n第{i}轮:")
            formatted.append(f"  用户: {turn['user_message']}")
            formatted.append(f"  助手: {turn['bot_response'][:100]}...")

            if turn.get('detected_intents'):
                formatted.append(f"  意图: {', '.join(turn['detected_intents'])}")

            if turn.get('extracted_entities'):
                entities_str = ", ".join([f"{e['type']}:{e['value']}" for e in turn['extracted_entities'][:3]])
                formatted.append(f"  实体: {entities_str}")

        formatted.append("=" * 60)

        return "\n".join(formatted)


def main():
    """主函数 - 演示使用"""
    manager = DialogManager()

    print("\n💬 对话状态管理 Skill 演示")
    print("=" * 60)

    # 创建新对话
    print("\n1. 创建新对话:")
    conversation = manager.create_conversation("user123", {"source": "demo"})
    print(f"   对话ID: {conversation['conversation_id']}")
    print(f"   初始状态: {conversation['state']}")

    # 模拟对话
    print("\n2. 模拟对话流程:")

    # 第一轮
    print("\n第一轮 - 用户问候:")
    conversation = manager.update_conversation(
        conversation['conversation_id'],
        "你好，我想查询股票",
        "您好！我是股票投资助手。请问您想查询哪只股票？",
        "greeting"
    )
    print(f"   用户: 你好，我想查询股票")
    print(f"   助手: 您好！我是股票投资助手。请问您想查询哪只股票？")
    print(f"   状态: {conversation['state']}")

    # 第二轮
    print("\n第二轮 - 用户提供股票:")
    conversation = manager.update_conversation(
        conversation['conversation_id'],
        "平安银行最近怎么样",
        "正在查询平安银行(000001)的最近表现...",
        "stock_query"
    )
    print(f"   用户: 平安银行最近怎么样")
    print(f"   助手: 正在查询平安银行(000001)的最近表现...")
    print(f"   状态: {conversation['state']}")

    # 第三轮
    print("\n第三轮 - 用户请求分析:")
    conversation = manager.update_conversation(
        conversation['conversation_id'],
        "帮我分析一下它的趋势，我风险偏好比较保守",
        "正在分析平安银行的趋势，基于您的保守风险偏好...",
        "trend_analysis"
    )
    print(f"   用户: 帮我分析一下它的趋势，我风险偏好比较保守")
    print(f"   助手: 正在分析平安银行的趋势，基于您的保守风险偏好...")
    print(f"   状态: {conversation['state']}")

    # 获取上下文
    print("\n3. 获取对话上下文:")
    context = manager.get_conversation_context(conversation['conversation_id'])
    print(f"   当前状态: {context['current_state']}")
    print(f"   已填充槽位: {context['slots']}")
    print(f"   缺失信息: {context['missing_info']}")
    print(f"   用户偏好: 风险偏好={context['user_profile'].get('risk_tolerance', '未知')}")

    # 获取下一步建议
    print("\n4. 下一步建议:")
    suggestion = manager.suggest_next_action(conversation['conversation_id'])
    print(f"   建议动作: {suggestion['action']}")
    print(f"   建议提示: {suggestion['prompt']}")
    print(f"   预期回应: {suggestion['expected_response']}")

    # 获取对话摘要
    print("\n5. 对话摘要:")
    summary = manager.get_conversation_summary(conversation['conversation_id'])
    print(f"   对话时长: {summary['duration']}")
    print(f"   对话轮数: {summary['turn_count']}")
    print(f"   主要话题: {', '.join(summary['main_topics'])}")

    # 格式化历史
    print("\n6. 对话历史:")
    history_formatted = manager.format_conversation_history(conversation['conversation_id'], 3)
    print(history_formatted)

    print("\n✅ 演示完成！")


if __name__ == "__main__":
    main()

