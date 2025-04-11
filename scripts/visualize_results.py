#!/usr/bin/env python
"""
Script to generate visualizations for the Renaissance Stock Ranking System.

This script is a convenient wrapper around the visualization functionality,
allowing users to create charts and graphs with a simple command.

Usage:
    python scripts/visualize_results.py [options]

Alternative Usage (CLI Tool):
    renaissance-visualize [options]

Both methods provide identical functionality, using the same underlying code.
The script approach is often more intuitive for new users, while the CLI tool
is convenient for regular users and automated workflows.

For detailed options, run:
    python scripts/visualize_results.py --help
    
    or
    
    renaissance-visualize --help
"""

import sys
import os

# Remove sys.path manipulation - rely on package installation or running with python -m
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import should work if package installed or run via python -m
from renaissance.cli.visualize import main

if __name__ == "__main__":
    sys.exit(main()) 