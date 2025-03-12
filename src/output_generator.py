"""
output_generator.py

This module handles the generation of output files with the results of the stock
ranking analysis. It creates CSV files for:
1. Latest month's stock rankings
2. Latest month's rank delta (change in rank from previous month)
3. (Optional) Historical monthly rankings for all stocks
"""

import os
import pandas as pd
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_output_directory(output_dir: str = '../output') -> str:
    """
    Create the output directory if it doesn't exist.
    
    Args:
        output_dir (str): Path to the output directory
        
    Returns:
        str: Path to the output directory
    """
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
        
        return output_dir
    
    except Exception as e:
        logger.error(f"Error creating output directory: {str(e)}")
        raise


def generate_latest_rankings_output(
    latest_rankings: pd.DataFrame, 
    latest_date: pd.Timestamp,
    nifty500_df: pd.DataFrame,
    output_dir: str = '../output'
) -> str:
    """
    Generate a CSV file with the latest month's stock rankings.
    
    Args:
        latest_rankings (pd.DataFrame): DataFrame with the latest month's rankings
        latest_date (pd.Timestamp): Timestamp of the latest month
        nifty500_df (pd.DataFrame): DataFrame with NIFTY 500 constituent data (for stock names)
        output_dir (str): Path to the output directory
        
    Returns:
        str: Path to the generated CSV file
    """
    logger.info("Generating output file for latest rankings")
    
    try:
        # Create the output directory if it doesn't exist
        output_dir = create_output_directory(output_dir)
        
        # Format the date as a string for the filename
        date_str = latest_date.strftime('%Y%m%d')
        
        # Merge with NIFTY 500 data to include stock names if available
        if 'Name' in nifty500_df.columns:
            output_df = pd.merge(latest_rankings, nifty500_df[['ISIN', 'Name']], on='ISIN', how='left')
        else:
            output_df = latest_rankings.copy()
        
        # Reorder columns for clarity
        column_order = ['ISIN']
        if 'Name' in output_df.columns:
            column_order.append('Name')
        column_order.extend(['Date', 'YearlyReturn', 'Rank'])
        output_df = output_df[column_order]
        
        # Sort by rank
        output_df = output_df.sort_values('Rank')
        
        # Generate the output filename
        output_file = os.path.join(output_dir, f'NIFTY500_Rankings_{date_str}.csv')
        
        # Write to CSV
        output_df.to_csv(output_file, index=False)
        
        logger.info(f"Generated latest rankings output file: {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error generating latest rankings output: {str(e)}")
        raise


def generate_rank_delta_output(
    latest_delta: pd.DataFrame, 
    latest_date: pd.Timestamp,
    nifty500_df: pd.DataFrame,
    output_dir: str = '../output'
) -> str:
    """
    Generate a CSV file with the latest month's rank delta.
    
    Args:
        latest_delta (pd.DataFrame): DataFrame with the latest month's rank delta
        latest_date (pd.Timestamp): Timestamp of the latest month
        nifty500_df (pd.DataFrame): DataFrame with NIFTY 500 constituent data (for stock names)
        output_dir (str): Path to the output directory
        
    Returns:
        str: Path to the generated CSV file
    """
    logger.info("Generating output file for latest rank delta")
    
    try:
        # Create the output directory if it doesn't exist
        output_dir = create_output_directory(output_dir)
        
        # Format the date as a string for the filename
        date_str = latest_date.strftime('%Y%m%d')
        
        # Merge with NIFTY 500 data to include stock names if available
        if 'Name' in nifty500_df.columns:
            output_df = pd.merge(latest_delta, nifty500_df[['ISIN', 'Name']], on='ISIN', how='left')
        else:
            output_df = latest_delta.copy()
        
        # Reorder columns for clarity
        column_order = ['ISIN']
        if 'Name' in output_df.columns:
            column_order.append('Name')
        column_order.extend(['Date', 'YearlyReturn', 'Rank', 'PreviousRank', 'RankDelta'])
        output_df = output_df[column_order]
        
        # Sort by absolute rank delta (largest changes first)
        output_df['AbsRankDelta'] = output_df['RankDelta'].abs()
        output_df = output_df.sort_values('AbsRankDelta', ascending=False)
        output_df = output_df.drop('AbsRankDelta', axis=1)
        
        # Generate the output filename
        output_file = os.path.join(output_dir, f'NIFTY500_RankDelta_{date_str}.csv')
        
        # Write to CSV
        output_df.to_csv(output_file, index=False)
        
        logger.info(f"Generated rank delta output file: {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error generating rank delta output: {str(e)}")
        raise


def generate_historical_rankings_output(
    ranked_df: pd.DataFrame,
    nifty500_df: pd.DataFrame,
    output_dir: str = '../output'
) -> str:
    """
    Generate a CSV file with historical monthly rankings for all stocks.
    
    Args:
        ranked_df (pd.DataFrame): DataFrame with historical rankings for all stocks
        nifty500_df (pd.DataFrame): DataFrame with NIFTY 500 constituent data (for stock names)
        output_dir (str): Path to the output directory
        
    Returns:
        str: Path to the generated CSV file
    """
    logger.info("Generating output file for historical rankings")
    
    try:
        # Create the output directory if it doesn't exist
        output_dir = create_output_directory(output_dir)
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Merge with NIFTY 500 data to include stock names if available
        if 'Name' in nifty500_df.columns:
            output_df = pd.merge(ranked_df, nifty500_df[['ISIN', 'Name']], on='ISIN', how='left')
        else:
            output_df = ranked_df.copy()
        
        # Reorder columns for clarity
        column_order = ['ISIN']
        if 'Name' in output_df.columns:
            column_order.append('Name')
        column_order.extend(['Date', 'YearlyReturn', 'Rank'])
        output_df = output_df[column_order]
        
        # Sort by date and rank
        output_df = output_df.sort_values(['Date', 'Rank'])
        
        # Generate the output filename
        output_file = os.path.join(output_dir, f'NIFTY500_Historical_Rankings_{timestamp}.csv')
        
        # Write to CSV
        output_df.to_csv(output_file, index=False)
        
        logger.info(f"Generated historical rankings output file: {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error generating historical rankings output: {str(e)}")
        raise


def generate_summary_statistics(
    ranked_df: pd.DataFrame,
    delta_df: pd.DataFrame,
    nifty500_df: pd.DataFrame,
    output_dir: str = '../output'
) -> str:
    """
    Generate a text file with summary statistics from the ranking analysis.
    
    Args:
        ranked_df (pd.DataFrame): DataFrame with historical rankings for all stocks
        delta_df (pd.DataFrame): DataFrame with rank delta information
        nifty500_df (pd.DataFrame): DataFrame with NIFTY 500 constituent data
        output_dir (str): Path to the output directory
        
    Returns:
        str: Path to the generated text file
    """
    logger.info("Generating summary statistics")
    
    try:
        # Create the output directory if it doesn't exist
        output_dir = create_output_directory(output_dir)
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate the output filename
        output_file = os.path.join(output_dir, f'NIFTY500_Ranking_Summary_{timestamp}.txt')
        
        # Calculate summary statistics
        num_stocks = ranked_df['ISIN'].nunique()
        num_months = ranked_df['Date'].nunique()
        date_range = f"{ranked_df['Date'].min().strftime('%Y-%m-%d')} to {ranked_df['Date'].max().strftime('%Y-%m-%d')}"
        
        avg_return = ranked_df['YearlyReturn'].mean()
        max_return = ranked_df['YearlyReturn'].max()
        min_return = ranked_df['YearlyReturn'].min()
        
        # Calculate rank volatility (standard deviation of rank) for each stock
        rank_volatility = ranked_df.groupby('ISIN')['Rank'].std().mean()
        
        # Calculate the average absolute rank delta
        filtered_delta_df = delta_df.dropna(subset=['RankDelta'])
        avg_abs_delta = filtered_delta_df['RankDelta'].abs().mean()
        
        # Write the summary to a text file
        with open(output_file, 'w') as f:
            f.write("NIFTY 500 Stock Ranking Analysis - Summary Statistics\n")
            f.write("=================================================\n\n")
            
            f.write("Data Coverage:\n")
            f.write(f"- Number of stocks analyzed: {num_stocks}\n")
            f.write(f"- Number of months analyzed: {num_months}\n")
            f.write(f"- Date range: {date_range}\n\n")
            
            f.write("Return Statistics:\n")
            f.write(f"- Average yearly return: {avg_return:.2%}\n")
            f.write(f"- Maximum yearly return: {max_return:.2%}\n")
            f.write(f"- Minimum yearly return: {min_return:.2%}\n\n")
            
            f.write("Ranking Statistics:\n")
            f.write(f"- Average rank volatility (std dev): {rank_volatility:.2f}\n")
            f.write(f"- Average absolute rank change: {avg_abs_delta:.2f} positions\n\n")
            
            f.write("Analysis generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        logger.info(f"Generated summary statistics file: {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error generating summary statistics: {str(e)}")
        raise
