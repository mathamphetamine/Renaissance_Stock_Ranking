#!/usr/bin/env python
"""
Script to extract data from Bloomberg for the Renaissance Stock Ranking System.

This script is a convenient wrapper around the Bloomberg data extraction functionality,
allowing users to extract NIFTY 500 data with a simple command.

Usage:
    python scripts/extract_bloomberg.py [options]

Alternative Usage (CLI Tool):
    renaissance-extract [options]

Both methods provide identical functionality, using the same underlying code.
The script approach is often more intuitive for new users, while the CLI tool
is convenient for regular users and automated workflows.

For detailed options, run:
    python scripts/extract_bloomberg.py --help
    
    or
    
    renaissance-extract --help
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from renaissance.cli.extract import main

if __name__ == "__main__":
    sys.exit(main()) 