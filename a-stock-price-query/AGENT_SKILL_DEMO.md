# Agent 与 Skill 本质区别及示例演示

## 📚 核心概念对比

### Skill（技能）
- **定义**：单一、专注的功能模块
- **特点**：
  - 完成特定任务（如查询价格、分析趋势）
  - 输入明确，输出结构化
  - 可独立测试和使用
  - 无状态或状态简单
- **示例**：
  - `fetch_stock_price.py` - 查询股票价格
  - `trend_analyzer.py` - 分析股票趋势
  - `investment_advisor.py` - 生成投资建议
  - `dialog_manager.py` - 管理对话状态

### Agent（智能体）
- **定义**：协调多个Skills的智能系统
- **特点**：
  - **组合多个Skills**：根据需求调用不同Skills
  - **上下文理解**：维护对话历史和用户状态
  - **自主决策**：基于规则和意图选择行动路径
  - **端到端处理**：从用户输入到最终响应的完整流程
- **示例**：
  - `stock_investment_agent.py` - 股票投资顾问Agent

## 🎯 设计目标演示

### 示例场景：用户咨询股票投资
```
用户: "平安银行最近怎么样？我想了解投资建议，风险偏好保守"
```

### Skill方式（传统）
1. **价格查询Skill**：查询平安银行价格数据
2. **趋势分析Skill**：分析平安银行趋势
3. **投资建议Skill**：生成保守型投资建议
4. **用户需要**：手动协调三个Skills，管理对话状态

### Agent方式（智能）
1. **对话理解**：Agent识别意图（查询+建议+风险偏好）
2. **决策制定**：决定使用价格查询、趋势分析、投资建议三个Skills
3. **Skills协调**：按顺序调用Skills，传递上下文
4. **响应生成**：整合所有结果，生成自然语言回复
5. **状态管理**：更新对话历史，准备下一轮交互

## 🚀 快速开始指南

### 步骤1：环境准备
```bash
# 1. 进入项目目录
cd /Users/telebup/github-project/a-stock-price-query

# 2. 检查Python环境
python --version  # 需要Python 3.7+

# 3. 安装依赖（如有）
pip install -r requirements.txt
```

### 步骤2：运行Skill示例（理解基础功能）
```bash
# 1. 运行原始价格查询Skill
python fetch_stock_price.py

# 2. 运行趋势分析Skill示例
python skills/trend_analyzer.py

# 3. 运行投资建议Skill示例
python skills/investment_advisor.py

# 4. 运行对话管理Skill示例
python skills/dialog_manager.py
```

### 步骤3：运行Agent演示（体验智能协调）
```bash
# 运行股票投资顾问Agent完整演示
python agent/stock_investment_agent.py
```

### 步骤4：启动API服务（可选）
```bash
# 启动HTTP API服务（需要Flask）
python app.py --port 8080

# 测试API（另开终端）
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "平安银行价格怎么样", "user_id": "test"}'
```

## 🔧 代码结构解析

### Skill实现示例（trend_analyzer.py）
```python
class StockTrendAnalyzer:
    """单一功能：分析股票趋势"""

    def analyze_trend(self, stock_code_or_name):
        # 输入：股票代码/名称
        # 输出：趋势分析结果
        # 功能单一，无状态管理
        pass
```

### Agent实现示例（stock_investment_agent.py）
```python
class StockInvestmentAgent:
    """协调多个Skills的智能体"""

    def process_message(self, conversation_id, user_message):
        # 1. 分析用户意图（使用对话管理Skill）
        intent_analysis = self._analyze_intent(user_message)

        # 2. 决策使用哪些Skills
        decision = self._make_decision(intent_analysis)

        # 3. 执行Skills
        results = self._execute_skills(decision)

        # 4. 生成综合响应
        response = self._generate_response(results)

        # 5. 更新对话状态
        self._update_conversation_state(conversation_id, response)

        return response
```

## 📊 核心区别总结

| 维度 | Skill（技能） | Agent（智能体） |
|------|--------------|----------------|
| **功能范围** | 单一、专注 | 综合、协调多个Skills |
| **上下文管理** | 无或简单 | 复杂对话状态管理 |
| **决策能力** | 无自主决策 | 基于规则的智能决策 |
| **输入输出** | 结构化数据 | 自然语言交互 |
| **使用场景** | 功能组件 | 端到端解决方案 |
| **部署单元** | 可单独部署 | 整体系统部署 |

## 🧪 动手实验

### 实验1：理解Skill独立性
```bash
# 创建测试脚本 test_skill.py
cat > test_skill.py << 'EOF'
from fetch_stock_price import StockPriceQuery
from skills.trend_analyzer import StockTrendAnalyzer

# 独立使用价格查询Skill
price_query = StockPriceQuery()
result1 = price_query.query("000001")
print("价格查询结果:", result1["success"])

# 独立使用趋势分析Skill
trend_analyzer = StockTrendAnalyzer()
result2 = trend_analyzer.analyze_trend("平安银行")
print("趋势分析结果:", result2["success"])

print("✅ Skills可独立使用，互不依赖")
EOF

python test_skill.py
```

### 实验2：体验Agent协调能力
```bash
# 创建测试脚本 test_agent.py
cat > test_agent.py << 'EOF'
import sys
sys.path.insert(0, ".")

from agent.stock_investment_agent import StockInvestmentAgent

# 创建Agent
agent = StockInvestmentAgent()

# 模拟多轮对话
print("=== 第1轮：用户问候 ===")
result1 = agent.start_conversation("user1", "你好")
print("Agent响应:", result1["agent_response"][:50])

print("\n=== 第2轮：查询股票 ===")
result2 = agent.process_message(result1["conversation_id"], "平安银行价格")
print("使用的Skills:", result2["execution_summary"]["skills_used"])

print("\n=== 第3轮：请求建议 ===")
result3 = agent.process_message(result1["conversation_id"], "投资建议，风险保守")
print("使用的Skills:", result3["execution_summary"]["skills_used"])

print("\n✅ Agent自动协调了多个Skills")
EOF

python test_agent.py
```

### 实验3：查看Agent决策过程
```bash
# 修改agent代码以输出详细日志
# 然后运行：
python agent/stock_investment_agent.py
```

## 🚢 部署到Agent广场

### 部署配置说明
已创建以下部署文件：
1. **.catpaw/catpaw-deploy.yaml** - 部署配置文件
2. **Dockerfile** - 容器化配置
3. **requirements.txt** - Python依赖
4. **app.py** - API服务入口

### 部署步骤
```bash
# 1. 构建Docker镜像
docker build -t stock-investment-advisor .

# 2. 本地测试运行
docker run -p 8080:8080 stock-investment-advisor

# 3. 推送到镜像仓库（示例）
docker tag stock-investment-advisor your-registry/stock-advisor:v1
docker push your-registry/stock-advisor:v1

# 4. 使用CatPaw部署到Agent广场
catpaw deploy --config .catpaw/catpaw-deploy.yaml
```

### 验证部署
```bash
# 健康检查
curl http://localhost:8080/api/health

# 测试对话
curl -X POST http://localhost:8080/api/chat \
  -d '{"message": "测试股票查询", "user_id": "test"}'

# 获取状态
curl http://localhost:8080/api/status
```

## 🔍 关键代码片段分析

### Skill的独立性
```python
# 每个Skill都有清晰的输入输出接口
class StockPriceQuery:
    def query(self, stock_code_or_name) -> Dict:
        # 输入：股票代码/名称
        # 输出：价格数据字典
        # 不依赖其他Skills
        pass

class StockTrendAnalyzer:
    def analyze_trend(self, stock_code_or_name) -> Dict:
        # 输入：股票代码/名称
        # 输出：趋势分析字典
        # 可以独立调用
        pass
```

### Agent的协调能力
```python
# Agent协调多个Skills
def _execute_skills(self, decision, user_message, conversation):
    results = {}

    # 根据决策调用不同Skills
    for skill_name in decision["skills_to_use"]:
        if skill_name == "price_query":
            results["price_query"] = self.price_query.query(...)
        elif skill_name == "trend_analyzer":
            results["trend_analyzer"] = self.trend_analyzer.analyze_trend(...)
        elif skill_name == "investment_advisor":
            # 需要先获取趋势和价格数据
            trend_data = results.get("trend_analyzer", self.trend_analyzer.analyze_trend(...))
            price_data = results.get("price_query", self.price_query.query(...))
            results["investment_advisor"] = self.investment_advisor.generate_advice(...)

    return results
```

### 决策逻辑
```python
def _make_decision(self, intent_analysis, conversation):
    # 基于意图和对话状态决定使用哪些Skills
    if intent_analysis["primary_intent"] == "advice_request":
        return {
            "skills_to_use": ["price_query", "trend_analyzer", "investment_advisor"],
            "action": "生成投资建议"
        }
    elif intent_analysis["primary_intent"] == "stock_query":
        return {
            "skills_to_use": ["price_query"],
            "action": "查询股票价格"
        }
```

## 📈 学习路径建议

### 阶段1：理解Skill（1-2小时）
1. 阅读每个Skill的源代码
2. 运行独立示例
3. 理解输入输出格式
4. 尝试修改或扩展一个Skill

### 阶段2：理解Agent（2-3小时）
1. 阅读Agent主循环代码
2. 跟踪决策过程
3. 观察Skills协调机制
4. 理解对话状态管理

### 阶段3：实践部署（1-2小时）
1. 本地运行完整系统
2. 测试API接口
3. 构建Docker镜像
4. 了解部署配置

### 阶段4：扩展开发（3-4小时）
1. 添加新的Skill
2. 修改决策规则
3. 优化对话管理
4. 集成真实数据API

## 🐛 故障排除

### 常见问题1：导入错误
```
ModuleNotFoundError: No module named 'skills'
```
**解决方案**：
```bash
# 确保在项目根目录运行
cd /Users/telebup/github-project/a-stock-price-query

# 或者添加项目路径
export PYTHONPATH=/Users/telebup/github-project/a-stock-price-query:$PYTHONPATH
```

### 常见问题2：依赖缺失
```
ImportError: No module named 'flask'
```
**解决方案**：
```bash
# 安装依赖
pip install flask

# 或使用不需要Flask的简单模式
python app.py  # 会自动检测并降级
```

### 常见问题3：端口冲突
```
Address already in use
```
**解决方案**：
```bash
# 使用不同端口
python app.py --port 8081

# 或停止占用端口的进程
lsof -ti:8080 | xargs kill -9
```

## 🎓 学习要点总结

### Skill设计原则
1. **单一职责**：每个Skill只做一件事
2. **清晰接口**：输入输出定义明确
3. **独立测试**：可单独验证功能
4. **无状态性**：尽量设计为无状态

### Agent设计原则
1. **协调能力**：智能调用多个Skills
2. **上下文感知**：维护对话状态
3. **决策逻辑**：基于规则的智能选择
4. **错误处理**：优雅处理失败情况

### 系统架构优势
1. **模块化**：Skills可独立开发维护
2. **可扩展性**：轻松添加新Skills
3. **可测试性**：每个组件可单独测试
4. **可部署性**：支持多种部署方式

## 📞 进一步支持

### 代码仓库
- 项目根目录：`/Users/telebup/github-project/a-stock-price-query`
- 主要文件：
  - `agent/stock_investment_agent.py` - Agent实现
  - `skills/` - 所有Skills目录
  - `.catpaw/catpaw-deploy.yaml` - 部署配置
  - `app.py` - API服务

### 测试命令
```bash
# 完整测试流程
./test_full_demo.sh  # 可创建此脚本

# 或手动测试
python agent/stock_investment_agent.py
python app.py --port 8080
curl http://localhost:8080/api/health
```

### 下一步建议
1. 尝试修改`trend_analyzer.py`添加新的技术指标
2. 在`stock_investment_agent.py`中添加新的决策规则
3. 创建新的Skill，如`risk_assessor.py`
4. 集成真实股票数据API

---

**创建日期**: 2026-03-09
**最后更新**: 2026-03-09
**版本**: 1.0.0
**作者**: CatPaw Assistant

> 通过本示例，您应该能够清晰理解Skill与Agent的本质区别，并能够实际运行、测试和部署完整的股票投资顾问系统。

