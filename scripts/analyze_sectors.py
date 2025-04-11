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

# Remove sys.path manipulation - rely on package installation or running with python -m
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import should work if package installed or run via python -m
from renaissance.cli.analyze import main

if __name__ == "__main__":
    sys.exit(main()) 