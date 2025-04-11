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
        
        # Initialize variable for metrics data
        metrics_data_for_report = None
        # If financial metrics are available, analyze them and store the result
        if any(col.startswith(('PE_', 'PB_', 'ROE', 'Debt', 'Dividend')) for col in data.columns):
            print("\nAnalyzing financial metrics by sector (detailed - CLI)...")
            metrics_data_for_report = integrate_financial_metrics(data, args.output_dir)
        else:
             print("\nNo financial metrics available. Skipping detailed sector metrics analysis (CLI).")
        
        # Generate consolidated report
        # Pass the correct metrics data (or None) to the report function
        generate_sector_report(sector_stats, concentration, metrics_data_for_report, args.output_dir)
        
        print("\nSector analysis completed successfully.")
        print(f"Results saved to {args.output_dir}")
        return 0
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 