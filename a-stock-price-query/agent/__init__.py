# Stock Investment Advisor Agent package
# Standardized agent structure for CatPaw deployment

from .stock_investment_agent import StockInvestmentAgent

# Define public API
__all__ = [
    'StockInvestmentAgent',
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Stock Investment Agent Team'
__description__ = 'Intelligent stock investment advisory agent that coordinates multiple skills'
__license__ = 'MIT'

# Agent capabilities
__capabilities__ = [
    'stock_price_query',
    'trend_analysis',
    'investment_advice',
    'dialog_management',
    'multi_skill_coordination'
]

# Required skills
__required_skills__ = [
    'stock_price_query',
    'trend_analyzer',
    'investment_advisor',
    'dialog_manager'
]

