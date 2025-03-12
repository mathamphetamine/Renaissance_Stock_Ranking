"""
main.py

This is the main script that orchestrates the entire stock ranking process:
1. Load data from Bloomberg-extracted files
2. Calculate yearly returns on a monthly rolling basis
3. Rank stocks based on these returns
4. Calculate rank delta (month-over-month rank changes)
5. Generate output files with results

Usage:
    python main.py
"""

import os
import sys
import pandas as pd
import argparse
import logging
from pathlib import Path

# Add the parent directory to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import other modules
from src.data_loader import load_and_prepare_all_data
from src.return_calculator import calculate_yearly_returns, validate_returns
from src.ranking_system import rank_stocks_by_return, analyze_rankings, get_latest_rankings
from src.rank_delta_calculator import calculate_rank_delta, get_latest_rank_delta, analyze_rank_delta
from src.output_generator import (
    generate_latest_rankings_output,
    generate_rank_delta_output,
    generate_historical_rankings_output,
    generate_summary_statistics
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ranking_system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='NIFTY 500 Stock Ranking System')
    
    parser.add_argument('--nifty500-file', type=str, default='../data/nifty500_list.csv',
                        help='Path to the CSV file containing NIFTY 500 constituent data with ISINs')
    
    parser.add_argument('--price-file', type=str, default='../data/historical_prices.csv',
                        help='Path to the CSV file containing historical monthly closing prices')
    
    parser.add_argument('--output-dir', type=str, default='../output',
                        help='Directory where output files will be saved')
    
    parser.add_argument('--generate-historical', action='store_true',
                        help='Generate output file with all historical rankings (may be large)')
    
    return parser.parse_args()


def main():
    """Main function to orchestrate the entire stock ranking process."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        logger.info("Starting NIFTY 500 Stock Ranking System")
        logger.info(f"NIFTY 500 constituents file: {args.nifty500_file}")
        logger.info(f"Historical prices file: {args.price_file}")
        logger.info(f"Output directory: {args.output_dir}")
        
        # Ensure files exist
        for file_path in [args.nifty500_file, args.price_file]:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                logger.info("Please ensure that you have extracted the necessary data from Bloomberg Terminal")
                logger.info("and placed the files in the correct location.")
                return
        
        # 1. Load data
        logger.info("Step 1: Loading data")
        nifty500_df, monthly_prices_df = load_and_prepare_all_data(
            args.nifty500_file, args.price_file
        )
        
        # 2. Calculate yearly returns
        logger.info("Step 2: Calculating yearly returns")
        returns_df = calculate_yearly_returns(monthly_prices_df)
        
        # Validate the calculated returns
        returns_df = validate_returns(returns_df)
        
        # 3. Rank stocks
        logger.info("Step 3: Ranking stocks")
        ranked_df = rank_stocks_by_return(returns_df)
        
        # Analyze the rankings
        analyze_rankings(ranked_df)
        
        # Get the latest month's rankings
        latest_rankings, latest_date = get_latest_rankings(ranked_df)
        
        # 4. Calculate rank delta
        logger.info("Step 4: Calculating rank delta")
        delta_df = calculate_rank_delta(ranked_df)
        
        # Analyze the rank delta
        analyze_rank_delta(delta_df)
        
        # Get the latest month's rank delta
        latest_delta, _ = get_latest_rank_delta(delta_df)
        
        # 5. Generate output files
        logger.info("Step 5: Generating output files")
        
        # Create the output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
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
        
        logger.info("NIFTY 500 Stock Ranking System completed successfully")
        logger.info(f"Output files have been saved to {args.output_dir}")
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}", exc_info=True)
        

if __name__ == "__main__":
    main()
