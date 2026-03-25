# Skills package for stock investment advisor
# Standardized skill structure with subdirectories

from .dialog_manager.skill import DialogManager
from .investment_advisor.skill import InvestmentAdvisor
# Re-export skill classes from submodules for backward compatibility
from .stock_price_query.skill import StockPriceQuery
from .trend_analyzer.skill import StockTrendAnalyzer

# Define public API
__all__ = [
    'StockPriceQuery',
    'StockTrendAnalyzer',
    'InvestmentAdvisor',
    'DialogManager',
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Stock Investment Agent Team'
__description__ = 'Standardized skills for stock investment advisory agent'

