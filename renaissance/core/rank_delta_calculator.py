"""
rank_delta_calculator.py

This module calculates the change in rank (rank delta) for stocks from one month
to the next. A positive rank delta indicates that a stock's rank has declined
(higher number = worse rank), while a negative rank delta indicates improvement.

For example, if a stock moves from Rank 10 to Rank 5, the rank delta is -5,
indicating an improvement of 5 positions.
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


def calculate_rank_delta(ranked_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the change in rank (rank delta) for each stock from the previous month.
    
    Args:
        ranked_df (pd.DataFrame): DataFrame with columns for ISIN, Date, YearlyReturn, and Rank
        
    Returns:
        pd.DataFrame: DataFrame with columns for ISIN, Date, YearlyReturn, Rank, and RankDelta
    """
    logger.info("Calculating rank delta for stocks")
    
    try:
        # Create a copy to avoid modifying the original DataFrame
        delta_df = ranked_df.copy()
        
        # Sort by ISIN and Date
        delta_df = delta_df.sort_values(by=['ISIN', 'Date'])
        
        # Calculate rank delta for each stock across consecutive months
        delta_df['PreviousRank'] = delta_df.groupby('ISIN')['Rank'].shift(1)
        delta_df['RankDelta'] = delta_df['Rank'] - delta_df['PreviousRank']
        
        # RankDelta will be NaN for the first occurrence of each stock
        # Count how many nulls we have
        null_count = delta_df['RankDelta'].isna().sum()
        logger.info(f"Number of stocks without rank delta (first occurrence): {null_count}")
        
        logger.info("Successfully calculated rank delta")
        return delta_df
    
    except Exception as e:
        logger.error(f"Error calculating rank delta: {str(e)}")
        raise


def get_latest_rank_delta(delta_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Timestamp]:
    """
    Get the rank delta for the most recent month in the dataset.
    
    Args:
        delta_df (pd.DataFrame): DataFrame with columns including ISIN, Date, Rank, and RankDelta
        
    Returns:
        Tuple[pd.DataFrame, pd.Timestamp]: Tuple containing:
            - DataFrame with the latest month's rank delta
            - Timestamp of the latest month
    """
    logger.info("Getting latest month's rank delta")
    
    try:
        # Find the most recent date in the dataset
        latest_date = delta_df['Date'].max()
        
        # Filter for the most recent date
        latest_delta = delta_df[delta_df['Date'] == latest_date].copy()
        
        # Sort by rank for clarity
        latest_delta = latest_delta.sort_values('Rank')
        
        logger.info(f"Retrieved rank delta for {len(latest_delta)} stocks for the latest month: {latest_date}")
        
        return latest_delta, latest_date
    
    except Exception as e:
        logger.error(f"Error getting latest rank delta: {str(e)}")
        raise


def analyze_rank_delta(delta_df: pd.DataFrame) -> None:
    """
    Analyze the rank delta to provide insights.
    
    Args:
        delta_df (pd.DataFrame): DataFrame with columns including ISIN, Date, Rank, and RankDelta
    """
    logger.info("Analyzing rank delta")
    
    try:
        # Filter out rows without rank delta (first occurrence of each stock)
        filtered_df = delta_df.dropna(subset=['RankDelta'])
        
        # Calculate statistics on rank delta
        mean_abs_delta = filtered_df['RankDelta'].abs().mean()
        max_improvement = filtered_df['RankDelta'].min()
        max_decline = filtered_df['RankDelta'].max()
        
        logger.info(f"Average absolute rank change: {mean_abs_delta:.2f} positions")
        logger.info(f"Maximum rank improvement: {max_improvement:.0f} positions")
        logger.info(f"Maximum rank decline: {max_decline:.0f} positions")
        
        # Identify stocks with the largest improvement in the latest month
        latest_date = delta_df['Date'].max()
        latest_delta = delta_df[delta_df['Date'] == latest_date].copy()
        
        top_improvers = latest_delta.nsmallest(5, 'RankDelta')
        logger.info("Top 5 stocks with largest rank improvement in the latest month:")
        for _, row in top_improvers.iterrows():
            if not pd.isna(row['RankDelta']):
                logger.info(f"ISIN: {row['ISIN']}, Previous Rank: {row['PreviousRank']:.0f}, " +
                           f"Current Rank: {row['Rank']}, Change: {row['RankDelta']:.0f} positions")
        
        # Identify stocks with the largest decline in the latest month
        top_decliners = latest_delta.nlargest(5, 'RankDelta')
        logger.info("Top 5 stocks with largest rank decline in the latest month:")
        for _, row in top_decliners.iterrows():
            if not pd.isna(row['RankDelta']):
                logger.info(f"ISIN: {row['ISIN']}, Previous Rank: {row['PreviousRank']:.0f}, " +
                           f"Current Rank: {row['Rank']}, Change: {row['RankDelta']:.0f} positions")
                
    except Exception as e:
        logger.error(f"Error analyzing rank delta: {str(e)}")


def identify_consistent_movers(delta_df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Identify stocks that consistently improve or decline in rank.
    
    Args:
        delta_df (pd.DataFrame): DataFrame with columns including ISIN, Date, Rank, and RankDelta
        
    Returns:
        Tuple[List[str], List[str]]: Tuple containing:
            - List of ISINs that consistently improve in rank
            - List of ISINs that consistently decline in rank
    """
    logger.info("Identifying consistent movers in rankings")
    
    try:
        # Create lists to store the consistent improvers and decliners
        consistent_improvers = []
        consistent_decliners = []
        
        # Group by ISIN
        for isin, group in delta_df.groupby('ISIN'):
            # Filter out rows without rank delta
            group = group.dropna(subset=['RankDelta'])
            
            # Skip if we have fewer than 3 data points
            if len(group) < 3:
                continue
            
            # Calculate the percentage of times the rank improved (negative delta)
            improvement_pct = (group['RankDelta'] < 0).mean()
            
            # Calculate the percentage of times the rank declined (positive delta)
            decline_pct = (group['RankDelta'] > 0).mean()
            
            # If improvement occurred in at least 75% of the months
            if improvement_pct >= 0.75:
                consistent_improvers.append(isin)
                
            # If decline occurred in at least 75% of the months
            if decline_pct >= 0.75:
                consistent_decliners.append(isin)
        
        logger.info(f"Identified {len(consistent_improvers)} consistent improvers")
        logger.info(f"Identified {len(consistent_decliners)} consistent decliners")
        
        return consistent_improvers, consistent_decliners
    
    except Exception as e:
        logger.error(f"Error identifying consistent movers: {str(e)}")
        return [], []
