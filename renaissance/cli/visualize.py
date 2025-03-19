#!/usr/bin/env python
"""
CLI entry point for the visualization module.

This script provides a command-line interface to generate visualizations
from the ranking outputs.

Usage:
    python -m renaissance.cli.visualize [options]
"""

import sys
from renaissance.visualization.visualize import create_visualizations


def main():
    """Main entry point for the visualization CLI."""
    try:
        create_visualizations()
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 