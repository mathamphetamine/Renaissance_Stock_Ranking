"""
Renaissance Stock Ranking System - A comprehensive package for ranking NIFTY 500 stocks.

This package provides tools for calculating yearly returns, ranking stocks,
analyzing rank changes, visualizing results, and performing sector-based analysis.

Main modules:
    - core: Core functionality for data loading, return calculation, ranking, and output generation
    - analysis: Advanced analysis tools including sector performance analysis
    - visualization: Tools for generating visualizations from ranking data
    - data_extraction: Utilities for extracting data from Bloomberg Terminal
    - cli: Command-line interfaces for all functionality

Example usage:
    from renaissance.core.data_loader import load_and_prepare_all_data
    from renaissance.core.return_calculator import calculate_yearly_returns
    from renaissance.core.ranking_system import rank_stocks_by_return
    
    # Load data
    nifty500_df, prices_df = load_and_prepare_all_data('data/nifty500_list.csv', 
                                                     'data/historical_prices.csv')
    
    # Calculate returns
    returns_df = calculate_yearly_returns(prices_df)
    
    # Rank stocks
    ranked_df = rank_stocks_by_return(returns_df)

Version: 2.0.0
Author: Renaissance Investment Managers
License: Proprietary - For internal use at Renaissance Investment Managers only
"""

__version__ = '2.0.0'
