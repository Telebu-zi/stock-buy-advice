"""
A股票价格查询系统 - 主程序入口
带有完整的股票编码输入验证
"""

from input_validator import is_valid_stock_code, normalize_stock_code, check_stock_code_exists

def get_stock_code_from_user():
    """
    从用户获取股票编码，并进行验证。
    如果用户未输入或输入无效，则返回提醒信息。
    
    Returns:
        str: 有效的股票编码，或 None（如果用户取消）
    """
    while True:
        # 获取用户输入
        user_input = input("\n请输入A股股票编码 (例如: 600000): ").strip()
        
        # 检查是否为空
        if not user_input:
            print("❌ 提醒: 您未输入股票编码！")
            print("💡 请输入有效的A股股票编码，例如:")
            print("   • 600000 (浦发银行)")
            print("   • 000001 (平安银行)")
            print("   • 300001 (特锐德)")
            continue
        
        # 验证格式
        if not is_valid_stock_code(user_input):
            print(f"❌ 输入错误: '{user_input}' 不是有效的股票编码格式！")
            print("💡 A股股票编码应为6位数字，例如: 600000")
            continue
        
        # 标准化编码
        normalized_code = normalize_stock_code(user_input)
        
        # 检查股票编码是否存在
        if not check_stock_code_exists(normalized_code):
            print(f"❌ 股票不存在: '{normalized_code}' 未找到！")
            print("💡 请检查股票编码是否正确，然后重试")
            continue
        
        print(f"✅ 股票编码有效: {normalized_code}")
        return normalized_code

def query_stock_info(stock_code):
    """
    查询股票信息（占位函数）
    
    Args:
        stock_code: 股票编码
    """
    print(f"\n🔍 正在查询股票 {stock_code} 的信息...")
    print(f"📊 股票编码: {stock_code}")
    print("📈 价格: [待实现]")
    print("💹 涨跌: [待实现]")
    print("🎯 建议: [待实现]")

def main():
    """主程序入口"""
    print("=" * 60)
    print("     🔍 A股票价格查询和投资建议系统")
    print("=" * 60)
    
    try:
        # 获取并验证股票编码
        stock_code = get_stock_code_from_user()
        
        if stock_code is None:
            print("\n👋 程序已退出")
            return
        
        # 查询股票信息
        query_stock_info(stock_code)
        
        print("\n✨ 查询完成！")
        
    except KeyboardInterrupt:
        print("\n\n👋 程序已被用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")


if __name__ == "__main__":
    main()