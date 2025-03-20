#!/usr/bin/env python
"""
Script to run the Renaissance Stock Ranking System.

This script is a convenient wrapper around the main functionality,
allowing users to run the ranking system with a simple command.

Usage:
    python scripts/run_ranking.py [options]

Alternative Usage (CLI Tool):
    renaissance-rank [options]

Both methods provide identical functionality, using the same underlying code.
The script approach is often more intuitive for new users, while the CLI tool
is convenient for regular users and automated workflows.

For detailed options, run:
    python scripts/run_ranking.py --help
    
    or
    
    renaissance-rank --help
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from renaissance.cli.main import main

if __name__ == "__main__":
    sys.exit(main()) 