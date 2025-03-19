#!/usr/bin/env python
"""
Script to run the Renaissance Stock Ranking System.

This script is a convenient wrapper around the main functionality,
allowing users to run the ranking system with a simple command.

Usage:
    python scripts/run_ranking.py [options]
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from renaissance.cli.main import main

if __name__ == "__main__":
    sys.exit(main()) 