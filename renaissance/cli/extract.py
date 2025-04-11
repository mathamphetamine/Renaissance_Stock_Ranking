#!/usr/bin/env python
"""
CLI entry point for the Bloomberg data extraction module.

This script provides a command-line interface to extract data from Bloomberg.

Usage:
    python -m renaissance.cli.extract [options]
"""

import sys
# Remove incorrect/unused imports
# from renaissance.data_extraction.bloomberg_data_extractor import parse_arguments, get_nifty500_constituents, get_historical_prices, get_financial_metrics

# Import the main function from the actual extractor script
from renaissance.data_extraction.bloomberg_data_extractor import main as extractor_main


def main():
    """Main entry point for the Bloomberg data extraction CLI."""
    # Directly call the main function from the extractor module,
    # which handles argument parsing, orchestration, and error handling.
    return extractor_main()


if __name__ == "__main__":
    # Use the return value from main as the exit code
    sys.exit(main()) 