#!/usr/bin/env python
"""
CLI entry point for the Bloomberg data extraction module.

This script provides a command-line interface to extract data from Bloomberg.

Usage:
    python -m renaissance.cli.extract [options]
"""

import sys
import argparse
from renaissance.data_extraction.bloomberg_data_extractor import parse_arguments, get_nifty500_constituents, get_historical_prices, get_financial_metrics


def main():
    """Main entry point for the Bloomberg data extraction CLI."""
    args = parse_arguments()
    
    try:
        print("Starting Bloomberg data extraction...")
        
        # Get NIFTY 500 constituents
        print("Extracting NIFTY 500 constituents...")
        constituents_df = get_nifty500_constituents(test_mode=args.test_mode)
        
        # Get historical prices
        print("Extracting historical prices...")
        get_historical_prices(
            constituents_df, 
            args.output_dir, 
            args.start_date, 
            args.end_date, 
            test_mode=args.test_mode
        )
        
        # Get financial metrics if not in test mode
        if not args.test_mode:
            print("Extracting financial metrics...")
            get_financial_metrics(constituents_df, args.output_dir)
        
        print("\nBloomberg data extraction completed successfully.")
        print(f"Results saved to {args.output_dir}")
        return 0
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 