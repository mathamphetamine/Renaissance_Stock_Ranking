"""
main.py

This is the main script that orchestrates the entire stock ranking process:
1. Load data from Bloomberg-extracted files
2. Calculate yearly returns on a monthly rolling basis
3. Rank stocks based on these returns
4. Calculate rank delta (month-over-month rank changes)
5. Generate output files with results

Usage:
    python -m renaissance.cli.main
"""

import os
import sys
import pandas as pd
import argparse
import logging
from pathlib import Path

# Import other modules
from renaissance.core.data_loader import load_and_prepare_all_data
from renaissance.core.return_calculator import calculate_yearly_returns, validate_returns
from renaissance.core.ranking_system import rank_stocks_by_return, analyze_rankings, get_latest_rankings
from renaissance.core.rank_delta_calculator import calculate_rank_delta, get_latest_rank_delta, analyze_rank_delta
from renaissance.core.output_generator import (
    generate_latest_rankings_output,
    generate_rank_delta_output,
    generate_historical_rankings_output,
    generate_summary_statistics
)

def setup_logging(output_dir=None):
    """Set up logging with appropriate handlers and directory structure."""
    if output_dir is None:
        output_dir = "output"
    
    # Create logs directory
    logs_dir = os.path.join(output_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Set up log file path
    log_file = os.path.join(logs_dir, "ranking_system.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='NIFTY 500 Stock Ranking System')
    
    parser.add_argument('--nifty500-file', type=str, default='data/nifty500_list.csv',
                        help='Path to the CSV file containing NIFTY 500 constituent data with ISINs')
    
    parser.add_argument('--price-file', type=str, default='data/historical_prices.csv',
                        help='Path to the CSV file containing historical monthly closing prices')
    
    parser.add_argument('--output-dir', type=str, default='output',
                        help='Directory where output files will be saved')
    
    parser.add_argument('--generate-historical', action='store_true',
                        help='Generate output file with all historical rankings (may be large)')
    
    return parser.parse_args()


def validate_input_data(nifty500_file: str, price_file: str, logger=None) -> bool:
    """
    Validate input data files before processing.
    
    Args:
        nifty500_file (str): Path to NIFTY 500 list CSV file
        price_file (str): Path to historical prices CSV file
        logger: Logger instance to use, defaults to None
        
    Returns:
        bool: True if data is valid, False otherwise
        
    Raises:
        ValueError: If data validation fails
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    logger.info("Validating input data files")
    
    # Check files exist
    if not os.path.exists(nifty500_file):
        raise FileNotFoundError(f"NIFTY 500 list file not found: {nifty500_file}")
    
    if not os.path.exists(price_file):
        raise FileNotFoundError(f"Historical price file not found: {price_file}")
    
    # Check file formats
    try:
        nifty500_df = pd.read_csv(nifty500_file)
        if "ISIN" not in nifty500_df.columns:
            raise ValueError(f"NIFTY 500 list file missing required 'ISIN' column: {nifty500_file}")
        
        # Check ISIN format (basic check)
        invalid_isins = [isin for isin in nifty500_df["ISIN"] if not isinstance(isin, str) or len(isin) != 12]
        if invalid_isins:
            logger.warning(f"Found {len(invalid_isins)} potentially invalid ISINs in NIFTY 500 list")
            
        logger.info(f"NIFTY 500 list file contains {len(nifty500_df)} stocks")
        
        # Check price file
        prices_df = pd.read_csv(price_file)
        required_columns = ["ISIN", "Date", "Price"]
        missing_columns = [col for col in required_columns if col not in prices_df.columns]
        
        if missing_columns:
            raise ValueError(f"Historical price file missing required columns: {missing_columns}")
        
        # Try to convert dates
        try:
            prices_df["Date"] = pd.to_datetime(prices_df["Date"])
        except Exception as e:
            raise ValueError(f"Error converting dates in historical price file: {str(e)}")
        
        # Check prices are numeric
        try:
            prices_df["Price"] = pd.to_numeric(prices_df["Price"])
        except Exception as e:
            raise ValueError(f"Error converting prices to numeric in historical price file: {str(e)}")
        
        # Check price coverage
        covered_isins = set(prices_df["ISIN"].unique())
        all_isins = set(nifty500_df["ISIN"])
        missing_isins = all_isins - covered_isins
        
        if missing_isins:
            logger.warning(f"Missing price data for {len(missing_isins)} ISINs from NIFTY 500 list")
            logger.debug(f"Examples of missing ISINs: {list(missing_isins)[:5]}")
            
            # If more than 20% of ISINs are missing, this might be a problem
            if len(missing_isins) > len(all_isins) * 0.2:
                logger.warning(f"More than 20% of ISINs are missing price data. This may affect analysis quality.")
        
        # Check date range
        date_range = (prices_df["Date"].min(), prices_df["Date"].max())
        months_covered = len(prices_df["Date"].dt.to_period("M").unique())
        
        logger.info(f"Historical price data covers {months_covered} months from {date_range[0]} to {date_range[1]}")
        
        # For proper analysis, we should have at least 12 months of data
        if months_covered < 12:
            logger.warning(f"Less than 12 months of price data available. This may affect yearly return calculations.")
            
        logger.info("Input data validation completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error validating input data: {str(e)}")
        raise ValueError(f"Input data validation failed: {str(e)}")


def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()
    
    # Set up logging
    logger = setup_logging(args.output_dir)
    
    logger.info("Starting NIFTY 500 Stock Ranking System")
    logger.info(f"NIFTY 500 constituents file: {args.nifty500_file}")
    logger.info(f"Historical prices file: {args.price_file}")
    logger.info(f"Output directory: {args.output_dir}")
    
    # Validate input data
    try:
        validate_input_data(args.nifty500_file, args.price_file, logger)
    except Exception as e:
        logger.error(f"Input data validation failed: {str(e)}")
        logger.info("Please check your input files and try again.")
        return 1
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # 1. Load data
        logger.info("Step 1: Loading data")
        try:
            nifty500_df, monthly_prices_df = load_and_prepare_all_data(
                args.nifty500_file, args.price_file
            )
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return 1
        
        # 2. Calculate yearly returns
        logger.info("Step 2: Calculating yearly returns")
        try:
            returns_df = calculate_yearly_returns(monthly_prices_df)
            returns_df = validate_returns(returns_df)
        except Exception as e:
            logger.error(f"Error calculating returns: {str(e)}")
            return 1
        
        # 3. Rank stocks
        logger.info("Step 3: Ranking stocks")
        try:
            ranked_df = rank_stocks_by_return(returns_df)
            analyze_rankings(ranked_df)
            latest_rankings, latest_date = get_latest_rankings(ranked_df)
        except Exception as e:
            logger.error(f"Error ranking stocks: {str(e)}")
            return 1
        
        # 4. Calculate rank delta
        logger.info("Step 4: Calculating rank delta")
        try:
            delta_df = calculate_rank_delta(ranked_df)
            analyze_rank_delta(delta_df)
            latest_delta, _ = get_latest_rank_delta(delta_df)
        except Exception as e:
            logger.error(f"Error calculating rank delta: {str(e)}")
            return 1
        
        # 5. Generate output files
        logger.info("Step 5: Generating output files")
        try:
            # Generate output files
            generate_latest_rankings_output(
                latest_rankings, latest_date, nifty500_df, args.output_dir
            )
            
            generate_rank_delta_output(
                latest_delta, latest_date, nifty500_df, args.output_dir
            )
            
            # Generate historical rankings output if requested
            if args.generate_historical:
                generate_historical_rankings_output(
                    ranked_df, nifty500_df, args.output_dir
                )
            
            # Generate summary statistics
            generate_summary_statistics(
                ranked_df, delta_df, nifty500_df, args.output_dir
            )
        except Exception as e:
            logger.error(f"Error generating output files: {str(e)}")
            return 1
        
        logger.info("NIFTY 500 Stock Ranking System completed successfully")
        logger.info(f"Output files have been saved to {args.output_dir}")
        return 0
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    main()
