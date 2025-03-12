"""
data_loader.py

This module handles loading data from CSV files containing:
1. NIFTY 500 constituent list with ISINs
2. Historical monthly closing prices for NIFTY 500 stocks

The data is expected to be extracted from Bloomberg Terminal in the office and
saved to CSV files, which are then processed by this module.
"""

import os
import pandas as pd
from typing import Tuple, Dict, Optional, List
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_nifty500_isins(file_path: str) -> pd.DataFrame:
    """
    Load NIFTY 500 constituent list with ISINs from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing NIFTY 500 constituent data
        
    Returns:
        pd.DataFrame: DataFrame with columns for ISIN, Name, Ticker, etc.
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If the file doesn't contain required columns
    """
    logger.info(f"Loading NIFTY 500 ISIN list from {file_path}")
    
    if not os.path.exists(file_path):
        error_msg = f"NIFTY 500 ISIN list file not found: {file_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    try:
        # Load the CSV file
        nifty500_df = pd.read_csv(file_path)
        
        # Check for required columns
        required_columns = ['ISIN']
        missing_columns = [col for col in required_columns if col not in nifty500_df.columns]
        
        if missing_columns:
            error_msg = f"Missing required columns in NIFTY 500 ISIN list: {missing_columns}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"Successfully loaded {len(nifty500_df)} NIFTY 500 constituents")
        return nifty500_df
    
    except Exception as e:
        logger.error(f"Error loading NIFTY 500 ISIN list: {str(e)}")
        raise


def load_historical_prices(file_path: str) -> pd.DataFrame:
    """
    Load historical monthly closing prices from a CSV file.
    
    Expected format:
    - CSV file with columns for ISIN, Date, and Closing Price
    - Dates should be in a format parseable by pandas (YYYY-MM-DD recommended)
    
    Args:
        file_path (str): Path to the CSV file containing historical price data
        
    Returns:
        pd.DataFrame: DataFrame with columns for ISIN, Date, and Price
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If the file doesn't contain required columns
    """
    logger.info(f"Loading historical price data from {file_path}")
    
    if not os.path.exists(file_path):
        error_msg = f"Historical price file not found: {file_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    try:
        # Load the CSV file
        prices_df = pd.read_csv(file_path)
        
        # Check for required columns (ISIN, Date, Price)
        required_columns = ['ISIN', 'Date', 'Price']
        missing_columns = [col for col in required_columns if col not in prices_df.columns]
        
        if missing_columns:
            error_msg = f"Missing required columns in historical price data: {missing_columns}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Convert Date column to datetime
        prices_df['Date'] = pd.to_datetime(prices_df['Date'])
        
        # Filter for month-end dates only
        prices_df = prices_df.sort_values(by=['ISIN', 'Date'])
        
        logger.info(f"Successfully loaded historical prices with {len(prices_df)} records")
        return prices_df
    
    except Exception as e:
        logger.error(f"Error loading historical price data: {str(e)}")
        raise


def prepare_monthly_price_data(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the historical price data to ensure we have month-end prices.
    If the data already contains month-end prices only, this function will
    simply return the data as is.
    
    Args:
        prices_df (pd.DataFrame): DataFrame with historical price data
        
    Returns:
        pd.DataFrame: DataFrame with month-end prices
    """
    logger.info("Preparing monthly price data")
    
    try:
        # Ensure the Date column is datetime
        prices_df['Date'] = pd.to_datetime(prices_df['Date'])
        
        # Extract year and month
        prices_df['Year'] = prices_df['Date'].dt.year
        prices_df['Month'] = prices_df['Date'].dt.month
        
        # Group by ISIN, Year, Month and get the last date (month-end)
        monthly_prices = prices_df.sort_values('Date').groupby(['ISIN', 'Year', 'Month']).last().reset_index()
        
        # Clean up temporary columns if needed
        if 'Year' in monthly_prices.columns and 'Month' in monthly_prices.columns:
            monthly_prices = monthly_prices.drop(['Year', 'Month'], axis=1)
            
        logger.info(f"Prepared monthly price data with {len(monthly_prices)} records")
        return monthly_prices
    
    except Exception as e:
        logger.error(f"Error preparing monthly price data: {str(e)}")
        raise


def load_and_prepare_all_data(
    nifty500_file: str, 
    price_file: str
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and prepare all required data for analysis.
    
    Args:
        nifty500_file (str): Path to NIFTY 500 constituent list file
        price_file (str): Path to historical price data file
        
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Tuple containing:
            - NIFTY 500 constituent DataFrame
            - Historical monthly price DataFrame
    """
    logger.info("Loading and preparing all data for analysis")
    
    # Load NIFTY 500 list
    nifty500_df = load_nifty500_isins(nifty500_file)
    
    # Load historical prices
    prices_df = load_historical_prices(price_file)
    
    # Prepare monthly price data
    monthly_prices_df = prepare_monthly_price_data(prices_df)
    
    # Verify that we have data for all ISINs in the NIFTY 500 list
    missing_isins = set(nifty500_df['ISIN']) - set(monthly_prices_df['ISIN'])
    if missing_isins:
        logger.warning(f"Missing price data for {len(missing_isins)} ISINs from NIFTY 500 list")
        logger.debug(f"Missing ISINs: {missing_isins}")
    
    logger.info("Successfully loaded and prepared all data")
    return nifty500_df, monthly_prices_df
