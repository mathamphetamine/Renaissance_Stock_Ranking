"""
return_calculator.py

This module handles the calculation of yearly returns on a monthly rolling basis
for NIFTY 500 stocks. For each month in the dataset, it calculates the 1-year return
for each stock using the formula:
Return = (Price at Month End) / (Price 12 Months Prior Month End) - 1
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def calculate_yearly_returns(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate yearly returns on a monthly rolling basis for all stocks.
    
    For each stock (ISIN) and each month, calculate the 1-year return using:
    Return = (Price at Month End) / (Price 12 Months Prior Month End) - 1
    
    Args:
        prices_df (pd.DataFrame): DataFrame with columns for ISIN, Date, and Price
        
    Returns:
        pd.DataFrame: DataFrame with columns for ISIN, Date, and YearlyReturn
        
    Note:
        This function expects the input DataFrame to have month-end prices only.
        Use prepare_monthly_price_data from data_loader.py to ensure this.
    """
    logger.info("Calculating yearly returns on a monthly rolling basis")
    
    try:
        # Ensure the DataFrame is sorted by ISIN and Date
        prices_df = prices_df.sort_values(by=['ISIN', 'Date'])
        
        # Create a copy to avoid modifying the original DataFrame
        returns_df = prices_df.copy()
        
        # Group by ISIN to calculate returns for each stock separately
        grouped = returns_df.groupby('ISIN')
        
        # Lists to store results
        result_isins = []
        result_dates = []
        result_returns = []
        
        for isin, group in grouped:
            # Sort by date
            group = group.sort_values('Date')
            
            # For each month, find the price 12 months ago
            for i in range(len(group)):
                current_date = group.iloc[i]['Date']
                current_price = group.iloc[i]['Price']
                
                # Find the date closest to 12 months ago
                target_date = current_date - pd.DateOffset(months=12)
                
                # Find the closest date in the past that's at least 11 months ago
                # (allowing for some flexibility in month-end dates)
                prior_rows = group[group['Date'] <= target_date + pd.DateOffset(days=15)]
                
                if not prior_rows.empty:
                    # Get the most recent price before the target date
                    prior_row = prior_rows.iloc[-1]
                    prior_date = prior_row['Date']
                    prior_price = prior_row['Price']
                    
                    # Calculate return only if the prior date is close to 12 months ago
                    # (within 1.5 months to account for varying month lengths)
                    date_diff = (current_date - prior_date).days
                    if 330 <= date_diff <= 395:  # Approximately 11-13 months
                        yearly_return = (current_price / prior_price) - 1
                        
                        result_isins.append(isin)
                        result_dates.append(current_date)
                        result_returns.append(yearly_return)
        
        # Create a new DataFrame with the results
        returns_result_df = pd.DataFrame({
            'ISIN': result_isins,
            'Date': result_dates,
            'YearlyReturn': result_returns
        })
        
        logger.info(f"Successfully calculated yearly returns with {len(returns_result_df)} records")
        return returns_result_df
    
    except Exception as e:
        logger.error(f"Error calculating yearly returns: {str(e)}")
        raise


def validate_returns(returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform validation checks on the calculated returns.
    
    Args:
        returns_df (pd.DataFrame): DataFrame with calculated yearly returns
        
    Returns:
        pd.DataFrame: Validated and possibly cleaned returns DataFrame
        
    Raises:
        ValueError: If critical validation issues are found
    """
    logger.info("Validating calculated returns")
    
    # Check for missing values
    missing_values = returns_df['YearlyReturn'].isna().sum()
    if missing_values > 0:
        logger.warning(f"Found {missing_values} missing return values")
        
    # Check for extreme values (potential data errors)
    extremely_high = returns_df[returns_df['YearlyReturn'] > 5].shape[0]  # 500% return
    extremely_low = returns_df[returns_df['YearlyReturn'] < -0.9].shape[0]  # 90% loss
    
    if extremely_high > 0:
        logger.warning(f"Found {extremely_high} extremely high returns (>500%)")
        
    if extremely_low > 0:
        logger.warning(f"Found {extremely_low} extremely low returns (<-90%)")
    
    # List top 5 highest and lowest returns for manual review
    top5_high = returns_df.nlargest(5, 'YearlyReturn')[['ISIN', 'Date', 'YearlyReturn']]
    top5_low = returns_df.nsmallest(5, 'YearlyReturn')[['ISIN', 'Date', 'YearlyReturn']]
    
    logger.info("Top 5 highest returns:")
    for _, row in top5_high.iterrows():
        logger.info(f"ISIN: {row['ISIN']}, Date: {row['Date']}, Return: {row['YearlyReturn']:.2%}")
        
    logger.info("Top 5 lowest returns:")
    for _, row in top5_low.iterrows():
        logger.info(f"ISIN: {row['ISIN']}, Date: {row['Date']}, Return: {row['YearlyReturn']:.2%}")
    
    # Check for sufficient data across time
    date_counts = returns_df['Date'].value_counts().sort_index()
    if len(date_counts) < 12:
        logger.warning(f"Calculated returns span only {len(date_counts)} months, which is less than a year")
    
    # Check for sufficient stocks each month
    avg_stocks_per_month = returns_df.groupby('Date')['ISIN'].nunique().mean()
    min_stocks_per_month = returns_df.groupby('Date')['ISIN'].nunique().min()
    
    logger.info(f"Average number of stocks with returns per month: {avg_stocks_per_month:.1f}")
    logger.info(f"Minimum number of stocks with returns in any month: {min_stocks_per_month}")
    
    if min_stocks_per_month < 100:
        logger.warning(f"Some months have fewer than 100 stocks with calculated returns")
    
    logger.info("Return validation completed")
    return returns_df
