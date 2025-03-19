"""
ranking_system.py

This module ranks NIFTY 500 stocks based on their calculated yearly returns
for each month in the dataset. The stock with the highest return receives Rank 1,
the second-highest Rank 2, and so on.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def rank_stocks_by_return(returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank stocks based on their yearly returns for each month.
    
    For each month in the dataset, stocks are ranked from 1 to N based on their
    yearly returns, with Rank 1 being the stock with the highest return.
    
    Args:
        returns_df (pd.DataFrame): DataFrame with columns for ISIN, Date, and YearlyReturn
        
    Returns:
        pd.DataFrame: DataFrame with columns for ISIN, Date, YearlyReturn, and Rank
    """
    logger.info("Ranking stocks by yearly returns for each month")
    
    try:
        # Create a copy to avoid modifying the original DataFrame
        ranked_df = returns_df.copy()
        
        # Group by Date and rank stocks within each month
        # Use ascending=False to rank higher returns better (Rank 1 is highest)
        ranked_df['Rank'] = ranked_df.groupby('Date')['YearlyReturn'].rank(ascending=False, method='min')
        
        # Convert rank to integer for clarity
        ranked_df['Rank'] = ranked_df['Rank'].astype(int)
        
        # Log some statistics about the rankings
        num_months = ranked_df['Date'].nunique()
        avg_stocks_per_month = ranked_df.groupby('Date')['ISIN'].count().mean()
        
        logger.info(f"Successfully ranked stocks for {num_months} months")
        logger.info(f"Average number of ranked stocks per month: {avg_stocks_per_month:.1f}")
        
        return ranked_df
    
    except Exception as e:
        logger.error(f"Error ranking stocks: {str(e)}")
        raise


def analyze_rankings(ranked_df: pd.DataFrame) -> None:
    """
    Analyze the rankings to provide insights.
    
    Args:
        ranked_df (pd.DataFrame): DataFrame with columns for ISIN, Date, YearlyReturn, and Rank
    """
    logger.info("Analyzing stock rankings")
    
    try:
        # Calculate the number of unique stocks that achieved Rank 1
        top_ranked_stocks = ranked_df[ranked_df['Rank'] == 1]['ISIN'].nunique()
        logger.info(f"Number of unique stocks that achieved Rank 1: {top_ranked_stocks}")
        
        # Calculate the number of stocks that maintained top 10 ranking for consecutive months
        top10_consecutive = 0
        for isin in ranked_df['ISIN'].unique():
            stock_ranks = ranked_df[ranked_df['ISIN'] == isin].sort_values('Date')
            if len(stock_ranks) >= 2:
                consecutive_top10 = (stock_ranks['Rank'] <= 10).rolling(window=2).min().sum() > 0
                if consecutive_top10:
                    top10_consecutive += 1
        
        logger.info(f"Number of stocks that maintained top 10 ranking for consecutive months: {top10_consecutive}")
        
        # Calculate rank volatility (standard deviation of rank) for each stock
        rank_volatility = ranked_df.groupby('ISIN')['Rank'].std()
        avg_rank_volatility = rank_volatility.mean()
        logger.info(f"Average rank volatility (std dev of rank): {avg_rank_volatility:.2f}")
        
        # Identify stocks with the most stable ranks (lowest std dev)
        most_stable_stocks = rank_volatility.nsmallest(5)
        logger.info("Top 5 stocks with most stable rankings:")
        for isin, volatility in most_stable_stocks.items():
            logger.info(f"ISIN: {isin}, Rank Volatility: {volatility:.2f}")
        
        # Identify stocks with the most volatile ranks (highest std dev)
        most_volatile_stocks = rank_volatility.nlargest(5)
        logger.info("Top 5 stocks with most volatile rankings:")
        for isin, volatility in most_volatile_stocks.items():
            logger.info(f"ISIN: {isin}, Rank Volatility: {volatility:.2f}")
        
    except Exception as e:
        logger.error(f"Error analyzing rankings: {str(e)}")


def get_latest_rankings(ranked_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Timestamp]:
    """
    Get the rankings for the most recent month in the dataset.
    
    Args:
        ranked_df (pd.DataFrame): DataFrame with columns for ISIN, Date, YearlyReturn, and Rank
        
    Returns:
        Tuple[pd.DataFrame, pd.Timestamp]: Tuple containing:
            - DataFrame with the latest month's rankings
            - Timestamp of the latest month
    """
    logger.info("Getting latest month's rankings")
    
    try:
        # Find the most recent date in the dataset
        latest_date = ranked_df['Date'].max()
        
        # Filter for the most recent date
        latest_rankings = ranked_df[ranked_df['Date'] == latest_date].copy()
        
        # Sort by rank for clarity
        latest_rankings = latest_rankings.sort_values('Rank')
        
        logger.info(f"Retrieved rankings for {len(latest_rankings)} stocks for the latest month: {latest_date}")
        
        return latest_rankings, latest_date
    
    except Exception as e:
        logger.error(f"Error getting latest rankings: {str(e)}")
        raise
