# 对话状态管理 Skill

## 功能描述

管理多轮对话的上下文状态，包括意图识别、实体提取、对话历史维护、用户偏好学习和下一步动作建议。为 Agent 提供对话理解和状态跟踪能力。

## 使用场景

当 Agent 需要：
- 维护跨多轮对话的上下文信息
- 识别用户意图和提取关键实体
- 跟踪对话状态和收集必要信息
- 学习用户偏好并个性化响应
- 建议下一步对话方向

**关键词触发**：
- 所有对话场景（自动触发）
- 需要状态管理的多轮交互
- 用户偏好学习场景

## 输入参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|-------|------|------|------|------|
| user_id | String | 是 | 用户唯一标识符 | "user123" |
| user_message | String | 是 | 用户输入消息 | "平安银行最近怎么样" |
| bot_response | String | 是 | Agent 的回复消息 | "正在查询平安银行..." |
| new_state | String | 否 | 手动设置的对话状态 | "stock_query" |

## 输出格式

```json
{
  "conversation_id": "user123_1741594800",
  "user_id": "user123",
  "created_at": "2026-03-09T10:30:00",
  "updated_at": "2026-03-09T10:30:05",
  "state": "stock_query",
  "context": {
    "agent_name": "股票投资助手",
    "start_time": "2026-03-09T10:30:00"
  },
  "history": [
    {
      "timestamp": "2026-03-09T10:30:00",
      "user_message": "你好",
      "bot_response": "您好！我是股票投资助手...",
      "detected_intents": ["greeting"],
      "extracted_entities": []
    }
  ],
  "slots": {
    "stock_code": "000001",
    "stock_name": "平安银行",
    "risk_tolerance": "保守"
  },
  "intents": ["stock_query", "trend_analysis"],
  "entities": [
    {"type": "stock_name", "value": "平安银行", "confidence": 0.8},
    {"type": "risk_preference", "value": "保守", "confidence": 0.7}
  ]
}
```

## 执行步骤

1. **对话创建**：为新用户或新会话创建对话记录
2. **意图识别**：基于关键词匹配用户意图
3. **实体提取**：从用户消息中提取股票代码、名称、价格、时间等实体
4. **状态更新**：更新对话状态和槽位信息
5. **偏好学习**：更新用户长期偏好和关注股票
6. **上下文摘要**：生成当前对话上下文摘要
7. **动作建议**：基于当前状态建议下一步动作

## 对话状态类型

- **greeting**：问候状态，欢迎用户并询问需求
- **stock_query**：股票查询状态，需要股票代码/名称
- **trend_analysis**：趋势分析状态，需要股票和周期信息
- **investment_advice**：投资建议状态，需要股票和风险偏好
- **comparison**：股票比较状态，需要多只股票信息
- **follow_up**：跟进问题状态，处理连续提问
- **closing**：结束对话状态

## 支持的实体类型

- **stock_code**：6位数字股票代码
- **stock_name**：常见股票名称（平安银行、五粮液等）
- **price**：价格数值（含¥符号）
- **time_period**：时间周期（今天、本周、最近5日等）
- **risk_preference**：风险偏好（保守、平衡、积极）

## 使用示例

**用户输入序列**：
```
用户：你好，我想了解股票投资
Agent：您好！我是股票投资助手...
用户：平安银行最近怎么样
Agent：正在查询平安银行...
用户：帮我分析一下趋势，我风险偏好比较保守
```

**对话管理输出**：
```
💬 对话上下文摘要：
============================================================
当前状态: trend_analysis
已填充槽位: {
  "stock_code": "000001",
  "stock_name": "平安银行",
  "risk_tolerance": "保守"
}
缺失信息: ["分析时间周期"]
用户偏好: {
  "risk_tolerance": "保守",
  "investment_horizon": "中期",
  "watched_stocks": ["000001"]
}
对话历史: 3轮
建议下一步: 询问分析参数
============================================================
```

## 核心方法

### `create_conversation(user_id, initial_context)`
创建新对话，返回对话ID和初始状态。

### `update_conversation(conversation_id, user_message, bot_response, new_state)`
更新对话状态，识别意图和实体，返回更新后的对话。

### `get_conversation_context(conversation_id)`
获取对话上下文摘要，包括当前状态、槽位、缺失信息等。

### `suggest_next_action(conversation_id)`
基于当前状态和缺失信息建议下一步动作。

### `format_conversation_history(conversation_id, max_turns)`
格式化对话历史，便于展示和调试。

## 错误处理

| 错误情况 | 处理方式 |
|--------|--------|
| 对话ID不存在 | 自动创建新对话并返回 |
| 消息格式错误 | 使用默认值并记录警告 |
| 实体识别失败 | 返回空实体列表，依赖后续补充 |

## 相关资源

- 意图识别关键词表
- 实体提取规则文档
- 对话状态机设计图

## 版本记录

- v1.0 (2026-03-09)：初版发布，支持基本对话状态管理

