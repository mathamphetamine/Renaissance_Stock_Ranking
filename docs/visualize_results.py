#!/usr/bin/env python
"""
Renaissance Stock Ranking System - Visualization Tool

This script helps visualize the results from the Renaissance Stock Ranking System.
It loads the output files and creates simple visualizations to help understand the data.

For users less familiar with Python:
1. Make sure you have run the main system first to generate output files
2. Run this script from the command line: python docs/visualize_results.py
3. The visualizations will be saved to the 'output/visualizations' directory

Requirements: pandas, matplotlib, seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from datetime import datetime
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def get_latest_file(pattern):
    """Find the most recent file matching a pattern."""
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def create_visualizations():
    """Create and save visualizations from the output files."""
    # Set up visualization styles
    plt.style.use('seaborn')
    sns.set_palette('colorblind')
    plt.rcParams['figure.figsize'] = (12, 6)

    # Create output directory if it doesn't exist
    viz_dir = os.path.join('output', 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)

    # Find the latest output files
    rankings_file = get_latest_file('output/NIFTY500_Rankings_*.csv')
    rank_delta_file = get_latest_file('output/NIFTY500_RankDelta_*.csv')

    if not rankings_file or not rank_delta_file:
        print("Error: Output files not found. Please run the system first.")
        return

    print(f"Using rankings file: {rankings_file}")
    print(f"Using rank delta file: {rank_delta_file}")

    # Load the data
    try:
        rankings = pd.read_csv(rankings_file)
        rank_delta = pd.read_csv(rank_delta_file)
        print(f"Loaded {len(rankings)} ranked stocks")
    except Exception as e:
        print(f"Error loading output files: {e}")
        return

    # Create timestamp for filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # 1. Distribution of yearly returns
    plt.figure(figsize=(12, 6))
    sns.histplot(rankings['Yearly_Return'], kde=True)
    plt.title('Distribution of Yearly Returns')
    plt.xlabel('Yearly Return (%)')
    plt.ylabel('Number of Stocks')
    plt.axvline(rankings['Yearly_Return'].mean(), color='r', linestyle='--', 
                label=f"Mean: {rankings['Yearly_Return'].mean():.2f}%")
    plt.axvline(0, color='black', linestyle='-', label="Zero Return")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, f'return_distribution_{timestamp}.png'))
    print(f"Created return distribution chart")

    # 2. Top performers
    top10 = rankings.sort_values('Yearly_Return', ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Yearly_Return', y='Name', data=top10)
    plt.title('Top 10 Performers by Yearly Return')
    plt.xlabel('Yearly Return (%)')
    plt.ylabel('Company')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, f'top_performers_{timestamp}.png'))
    print(f"Created top performers chart")

    # 3. Rank changes (if rank delta data is available)
    if 'Rank_Delta' in rank_delta.columns:
        # Distribution of rank changes
        plt.figure(figsize=(12, 6))
        sns.histplot(rank_delta['Rank_Delta'], kde=True)
        plt.title('Distribution of Rank Changes')
        plt.xlabel('Rank Delta (negative values indicate improvement)')
        plt.ylabel('Number of Stocks')
        plt.axvline(rank_delta['Rank_Delta'].mean(), color='r', linestyle='--', 
                    label=f"Mean: {rank_delta['Rank_Delta'].mean():.2f}")
        plt.axvline(0, color='black', linestyle='-', label="No Change")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f'rank_delta_distribution_{timestamp}.png'))
        print(f"Created rank delta distribution chart")

        # Top improvers (biggest negative rank delta)
        top_improvers = rank_delta.sort_values('Rank_Delta').head(10)
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Rank_Delta', y='Name', data=top_improvers)
        plt.title('Top 10 Rank Improvers (Positive Momentum)')
        plt.xlabel('Rank Delta (negative indicates improvement)')
        plt.ylabel('Company')
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f'top_improvers_{timestamp}.png'))
        print(f"Created top improvers chart")

    # 4. Save summary data as CSV
    top_performers = rankings.sort_values('Yearly_Return', ascending=False).head(20)
    top_performers.to_csv(os.path.join(viz_dir, f'top_performers_{timestamp}.csv'), index=False)
    print(f"Saved top performers data to CSV")

    if 'Rank_Delta' in rank_delta.columns:
        top_improvers = rank_delta.sort_values('Rank_Delta').head(20)
        top_improvers.to_csv(os.path.join(viz_dir, f'top_improvers_{timestamp}.csv'), index=False)
        print(f"Saved top improvers data to CSV")
    
    print(f"\nAll visualizations have been saved to the '{viz_dir}' directory.")
    print("You can open these image files to view the charts.")

if __name__ == "__main__":
    print("Renaissance Stock Ranking System - Visualization Tool")
    print("====================================================")
    create_visualizations() 