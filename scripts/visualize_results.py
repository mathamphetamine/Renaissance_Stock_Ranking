#!/usr/bin/env python
"""
Script to generate visualizations for the Renaissance Stock Ranking System.

This script is a convenient wrapper around the visualization functionality,
allowing users to generate charts and graphs with a simple command.

Usage:
    python scripts/visualize_results.py [options]
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from renaissance.cli.visualize import main

if __name__ == "__main__":
    sys.exit(main()) 