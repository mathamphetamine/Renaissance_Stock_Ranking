#!/usr/bin/env python
"""
Script to extract data from Bloomberg for the Renaissance Stock Ranking System.

This script is a convenient wrapper around the Bloomberg data extraction functionality,
allowing users to retrieve market data with a simple command.

Usage:
    python scripts/extract_bloomberg.py [options]
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from renaissance.cli.extract import main

if __name__ == "__main__":
    sys.exit(main()) 