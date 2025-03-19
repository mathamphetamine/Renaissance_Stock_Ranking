#!/usr/bin/env python
"""
Script to run the sector analysis for the Renaissance Stock Ranking System.

This script is a convenient wrapper around the sector analysis functionality,
allowing users to analyze sector performance with a simple command.

Usage:
    python scripts/analyze_sectors.py [options]
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from renaissance.cli.analyze import main

if __name__ == "__main__":
    sys.exit(main()) 