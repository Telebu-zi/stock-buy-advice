#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票投资顾问 Agent API 服务
将Agent包装为HTTP服务，便于部署和集成
"""

import os
import sys
import json
import logging
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from agent.stock_investment_agent import StockInvestmentAgent
    print("✅ Agent导入成功")
except ImportError as e:
    print(f"❌ Agent导入失败: {e}")
    sys.exit(1)

# 尝试导入Flask，如果不存在则使用简单HTTP服务器
try:
    from flask import Flask, request, jsonify, Response
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("⚠️  Flask未安装，使用简单HTTP服务器")

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentAPIServer:
    """Agent API服务器"""

    def __init__(self):
        self.agent = StockInvestmentAgent("股票投资顾问API")
        self.app = None
        self.setup_server()

    def setup_server(self):
        """设置服务器"""
        if HAS_FLASK:
            self.app = Flask(__name__)
            self.setup_flask_routes()
        else:
            self.app = self.setup_simple_server()

    def setup_flask_routes(self):
        """设置Flask路由"""

        @self.app.route('/')
        def index():
            """首页"""
            return jsonify({
                "service": "股票投资顾问API",
                "version": "1.0.0",
                "status": "运行中",
                "endpoints": {
                    "/api/chat": "处理对话 (POST)",
                    "/api/status": "获取状态 (GET)",
                    "/api/health": "健康检查 (GET)",
                    "/api/skills": "获取Skills列表 (GET)"
                },
                "documentation": "查看README.md"
            })

        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            """处理用户消息"""
            try:
                data = request.get_json()
                if not data or 'message' not in data:
                    return jsonify({
                        "success": False,
                        "error": "缺少message字段"
                    }), 400

                message = data['message']
                user_id = data.get('user_id', 'anonymous')
                conversation_id = data.get('conversation_id')

                logger.info(f"处理消息: user={user_id}, message={message[:50]}...")

                if conversation_id:
                    # 继续现有对话
                    result = self.agent.process_message(conversation_id, message)
                else:
                    # 开始新对话
                    result = self.agent.start_conversation(user_id, message)
                    conversation_id = result['conversation_id']

                response = {
                    "success": True,
                    "conversation_id": conversation_id,
                    "agent_response": result['agent_response'],
                    "intent": result.get('intent_analysis', {}).get('primary_intent'),
                    "timestamp": datetime.now().isoformat()
                }

                return jsonify(response)

            except Exception as e:
                logger.error(f"处理消息失败: {e}")
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500

        @self.app.route('/api/status', methods=['GET'])
        def status():
            """获取Agent状态"""
            try:
                status_info = self.agent.get_agent_status()
                return jsonify({
                    "success": True,
                    "status": status_info
                })
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500

        @self.app.route('/api/health', methods=['GET'])
        def health():
            """健康检查"""
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "stock-investment-advisor"
            })

        @self.app.route('/api/skills', methods=['GET'])
        def skills():
            """获取Skills列表"""
            skills_list = [
                {
                    "name": "价格查询",
                    "description": "查询股票价格信息",
                    "endpoint": "内置"
                },
                {
                    "name": "趋势分析",
                    "description": "分析股票技术趋势",
                    "endpoint": "内置"
                },
                {
                    "name": "投资建议",
                    "description": "生成个性化投资建议",
                    "endpoint": "内置"
                },
                {
                    "name": "对话管理",
                    "description": "管理多轮对话上下文",
                    "endpoint": "内置"
                }
            ]

            return jsonify({
                "success": True,
                "skills": skills_list,
                "count": len(skills_list)
            })

    def setup_simple_server(self):
        """设置简单HTTP服务器（备用）"""
        from http.server import BaseHTTPRequestHandler
        import urllib.parse

        class SimpleAgentHandler(BaseHTTPRequestHandler):
            """简单HTTP处理器"""

            def do_GET(self):
                """处理GET请求"""
                parsed_path = urllib.parse.urlparse(self.path)

                if parsed_path.path == '/api/health':
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps({
                        "status": "healthy",
                        "service": "stock-advisor"
                    })
                    self.wfile.write(response.encode())

                elif parsed_path.path == '/':
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps({
                        "service": "股票投资顾问（简单模式）",
                        "note": "请安装Flask以获得完整功能"
                    })
                    self.wfile.write(response.encode())

                else:
                    self.send_response(404)
                    self.end_headers()

            def do_POST(self):
                """处理POST请求"""
                if self.path == '/api/chat':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode())

                    # 简单处理
                    message = data.get('message', '')
                    response_text = f"收到消息: {message}. [简单模式，请安装Flask]"

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps({
                        "success": True,
                        "response": response_text
                    })
                    self.wfile.write(response.encode())
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, format, *args):
                """覆盖日志方法"""
                logger.info(f"{self.address_string()} - {format % args}")

        return SimpleAgentHandler

    def run(self, host='0.0.0.0', port=8080):
        """运行服务器"""
        logger.info(f"启动股票投资顾问API服务，端口: {port}")

        if HAS_FLASK:
            logger.info("使用Flask服务器")
            self.app.run(host=host, port=port, debug=False)
        else:
            logger.info("使用简单HTTP服务器")
            from http.server import HTTPServer
            server = HTTPServer((host, port), self.app)
            logger.info(f"服务器启动: http://{host}:{port}")
            server.serve_forever()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='股票投资顾问API服务')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址')
    parser.add_argument('--port', type=int, default=8080, help='监听端口')
    parser.add_argument('--debug', action='store_true', help='调试模式')

    args = parser.parse_args()

    # 创建并运行服务器
    server = AgentAPIServer()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")

    try:
        server.run(host=args.host, port=args.port)
    except KeyboardInterrupt:
        logger.info("服务停止")
    except Exception as e:
        logger.error(f"服务启动失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

