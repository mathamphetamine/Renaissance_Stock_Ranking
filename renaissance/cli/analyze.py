#!/usr/bin/env python
"""
CLI entry point for the sector analysis module.

This script provides a command-line interface to run the sector analysis
functionality.

Usage:
    python -m renaissance.cli.analyze [options]
"""

import argparse
import sys
from renaissance.analysis.sector_analysis import parse_arguments, load_data, analyze_sector_performance, analyze_top_stocks_by_sector, analyze_sector_concentration, generate_sector_report, integrate_financial_metrics


def main():
    """Main entry point for the sector analysis CLI."""
    args = parse_arguments()
    
    try:
        # Load the data
        data = load_data(args)
        
        # Perform the various analyses
        sector_stats = analyze_sector_performance(data, args.output_dir)
        top_stocks = analyze_top_stocks_by_sector(data, args.output_dir)
        concentration = analyze_sector_concentration(data, args.output_dir)
        
        # If financial metrics are available, analyze them
        if any(col.startswith(('PE_', 'PB_', 'ROE', 'Debt', 'Dividend')) for col in data.columns):
            integrate_financial_metrics(data, args.output_dir)
        
        # Generate consolidated report
        generate_sector_report(sector_stats, concentration, top_stocks, args.output_dir)
        
        print("\nSector analysis completed successfully.")
        print(f"Results saved to {args.output_dir}")
        return 0
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 