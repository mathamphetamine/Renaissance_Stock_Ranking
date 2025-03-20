#!/usr/bin/env python
"""
Renaissance Stock Ranking System - Visualization Tool

This script creates easy-to-understand visualizations from the Renaissance Stock Ranking System
outputs. It's designed to be user-friendly, especially for those without programming experience.

===== FOR NON-TECHNICAL USERS =====

What this tool does:
1. Creates charts showing stock performance patterns
2. Highlights the best-performing stocks
3. Shows which stocks are gaining momentum (improving rank)
4. Visualizes the distribution of returns across all stocks
5. Saves all charts as image files you can easily view and share

How to use it:
1. Make sure you've run the main system first (python -m renaissance.cli.main)
2. Open a terminal/command prompt
3. Navigate to the Renaissance_Stock_Ranking directory
4. Type: python -m renaissance.cli.visualize
5. Look in the 'output/visualizations' folder for the results

No coding knowledge required! Just run it and view the images.

===== TECHNICAL DETAILS =====

This script:
- Loads the latest ranking outputs
- Creates various visualizations using matplotlib and seaborn
- Saves visualizations to the 'output/visualizations' directory
- Generates CSV files with key statistics

Dependencies: pandas, matplotlib, seaborn
"""

import pandas as pd
import os
import glob
from datetime import datetime
import sys
import numpy as np

# Set matplotlib backend for headless environments
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def get_latest_file(pattern):
    """
    Find the most recent file matching a pattern.
    
    Args:
        pattern (str): Glob pattern to match files (e.g., 'output/NIFTY500_Rankings_*.csv')
        
    Returns:
        str or None: Path to the most recent file, or None if no files found
    """
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def create_visualization_index(viz_dir, timestamp, visualizations):
    """
    Create an HTML index file that displays all visualizations with explanations.
    This makes it easy for non-technical users to view and understand all charts.
    
    Args:
        viz_dir (str): Directory where visualizations are saved
        timestamp (str): Timestamp for the file names
        visualizations (list): List of dictionaries with visualization info
    """
    index_path = os.path.join(viz_dir, f'visualization_index_{timestamp}.html')
    
    with open(index_path, 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Renaissance Stock Ranking - Visualizations</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .vis-container { margin-bottom: 40px; border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
                h1 { color: #2c3e50; }
                h2 { color: #3498db; }
                .description { margin-bottom: 15px; }
                .interpretation { background-color: #f8f9fa; padding: 15px; border-left: 4px solid #4caf50; }
                img { max-width: 100%; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-top: 15px; }
                .footer { margin-top: 30px; font-size: 0.8em; color: #7f8c8d; text-align: center; }
            </style>
        </head>
        <body>
            <h1>Renaissance Stock Ranking System - Visualization Results</h1>
            <p>Generated on: """)
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        f.write("""</p>
            <p>This document contains visualizations generated from the latest stock ranking data. Each visualization includes an explanation to help you interpret the results.</p>
        """)
        
        for viz in visualizations:
            f.write(f"""
            <div class="vis-container">
                <h2>{viz['title']}</h2>
                <div class="description">{viz['description']}</div>
                <img src="{os.path.basename(viz['file'])}" alt="{viz['title']}">
                <div class="interpretation"><strong>How to interpret this chart:</strong> {viz['interpretation']}</div>
            </div>
            """)
        
        f.write("""
            <div class="footer">
                <p>Renaissance Investment Managers - Automated Stock Ranking System</p>
                <p>For more information, please refer to the user guide or contact the team.</p>
            </div>
        </body>
        </html>
        """)
    
    print(f"Created visualization index at {index_path}")
    print(f"👉 Open this HTML file in any web browser for an interactive visualization guide")

def create_visualizations():
    """
    Create and save visualizations from the output files.
    
    This function:
    1. Locates the latest ranking output files
    2. Creates various visualizations
    3. Saves them as image files and CSVs
    4. Creates an HTML index with explanations
    """
    # Set up visualization styles for professional-looking charts
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette('colorblind')
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 12

    # Create output directory if it doesn't exist
    viz_dir = os.path.join('output', 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)

    # Find the latest output files
    rankings_file = get_latest_file('output/NIFTY500_Rankings_*.csv')
    rank_delta_file = get_latest_file('output/NIFTY500_RankDelta_*.csv')

    if not rankings_file or not rank_delta_file:
        print("Error: Output files not found. Please run the main system first (python -m renaissance.cli.main).")
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
    
    # List to store visualization information for the index
    visualizations = []

    # 1. Distribution of yearly returns
    plt.figure(figsize=(12, 6))
    sns.histplot(rankings['YearlyReturn'], kde=True, bins=30, color='#3498db')
    plt.title('Distribution of Yearly Returns', fontsize=16)
    plt.xlabel('Yearly Return (%)', fontsize=14)
    plt.ylabel('Number of Stocks', fontsize=14)
    plt.axvline(rankings['YearlyReturn'].mean(), color='r', linestyle='--', 
                label=f"Mean: {rankings['YearlyReturn'].mean():.2f}%")
    plt.axvline(0, color='black', linestyle='-', label="Zero Return")
    plt.grid(axis='y', alpha=0.3)
    plt.legend(fontsize=12)
    plt.tight_layout()
    return_dist_file = os.path.join(viz_dir, f'return_distribution_{timestamp}.png')
    plt.savefig(return_dist_file, dpi=300)
    print(f"Created return distribution chart")
    
    visualizations.append({
        'title': 'Distribution of Yearly Returns',
        'description': 'This chart shows how stock returns are distributed across the NIFTY 500. The curve indicates the overall pattern, while vertical lines show the average return and zero-return mark.',
        'file': return_dist_file,
        'interpretation': 'Look for whether most stocks had positive returns (distribution mostly to the right of zero line) or negative returns (mostly to the left). The wider the spread, the more varied the stock performance. If the distribution has multiple peaks, it suggests distinct groups of stocks with different performance levels.'
    })

    # 2. Top performers
    top10 = rankings.sort_values('YearlyReturn', ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    bars = sns.barplot(x='YearlyReturn', y='Name', hue='Name', data=top10, palette='viridis', legend=False)
    
    for i, bar in enumerate(bars.patches):
        value = top10.iloc[i]['YearlyReturn'] * 100
        bars.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, f"{value:.1f}%", va='center')
    
    plt.title(f"Top {len(top10)} Performing Stocks", fontsize=16)
    plt.xlabel("Yearly Return", fontsize=12)
    plt.ylabel("Stock", fontsize=12)
    plt.axvline(x=0, color='gray', linestyle='--')
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    top_perf_file = os.path.join(viz_dir, f'top_performers_{timestamp}.png')
    plt.savefig(top_perf_file, dpi=300)
    print(f"Created top performers chart")
    
    visualizations.append({
        'title': 'Top 10 Performers by Yearly Return',
        'description': 'This chart highlights the 10 stocks with the highest yearly returns, showing the best-performing companies in the analysis period.',
        'file': top_perf_file,
        'interpretation': 'These are the stocks that have delivered the highest returns over the past year. Consider investigating these companies further to understand what drove their exceptional performance. Remember that past performance does not guarantee future results, but these stocks have demonstrated strong positive momentum.'
    })

    # 3. Bottom performers
    bottom10 = rankings.sort_values('YearlyReturn').head(10)
    plt.figure(figsize=(12, 8))
    bars = sns.barplot(x='YearlyReturn', y='Name', hue='Name', data=bottom10, palette='viridis', legend=False)
    
    for i, bar in enumerate(bars.patches):
        value = bottom10.iloc[i]['YearlyReturn'] * 100
        bars.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, f"{value:.1f}%", va='center')
    
    plt.title(f"Bottom {len(bottom10)} Performing Stocks", fontsize=16)
    plt.xlabel("Yearly Return", fontsize=12)
    plt.ylabel("Stock", fontsize=12)
    plt.axvline(x=0, color='gray', linestyle='--')
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    bottom_perf_file = os.path.join(viz_dir, f'bottom_performers_{timestamp}.png')
    plt.savefig(bottom_perf_file, dpi=300)
    print(f"Created bottom performers chart")
    
    visualizations.append({
        'title': 'Bottom 10 Performers by Yearly Return',
        'description': 'This chart shows the 10 stocks with the lowest yearly returns, highlighting the worst-performing companies in the analysis period.',
        'file': bottom_perf_file,
        'interpretation': 'These stocks had the poorest performance over the past year. Understand that negative performance may be due to company-specific issues, sector-wide challenges, or market conditions. Some investors look for turnaround opportunities among underperforming stocks, while others prefer to avoid them until positive momentum returns.'
    })

    # 4. Return vs Rank scatterplot
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(x='Rank', y='YearlyReturn', data=rankings, alpha=0.6)
    
    # Fit a trend line
    z = np.polyfit(rankings['Rank'], rankings['YearlyReturn'], 1)
    p = np.poly1d(z)
    plt.plot(rankings['Rank'], p(rankings['Rank']), "r--", alpha=0.8)
    
    plt.title('Yearly Return vs. Rank', fontsize=16)
    plt.xlabel('Rank (1 is best)', fontsize=14)
    plt.ylabel('Yearly Return (%)', fontsize=14)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    scatter_file = os.path.join(viz_dir, f'return_vs_rank_{timestamp}.png')
    plt.savefig(scatter_file, dpi=300)
    print(f"Created return vs rank scatter plot")
    
    visualizations.append({
        'title': 'Yearly Return vs. Rank',
        'description': 'This scatter plot shows the relationship between a stock\'s rank and its yearly return. Each dot represents one stock.',
        'file': scatter_file,
        'interpretation': 'The downward slope confirms that stocks with better ranks (lower numbers) have higher returns. The scatter pattern shows how closely the ranking follows returns. Outliers may indicate stocks with recent significant changes that haven\'t yet affected their overall ranking.'
    })

    # 5. Rank changes (if rank delta data is available)
    if 'RankDelta' in rank_delta.columns:
        # Distribution of rank changes
        plt.figure(figsize=(12, 6))
        sns.histplot(rank_delta['RankDelta'], kde=True, bins=30, color='#2ecc71')
        plt.title('Distribution of Rank Changes', fontsize=16)
        plt.xlabel('Rank Delta (negative values indicate improvement)', fontsize=14)
        plt.ylabel('Number of Stocks', fontsize=14)
        plt.axvline(rank_delta['RankDelta'].mean(), color='r', linestyle='--', 
                    label=f"Mean: {rank_delta['RankDelta'].mean():.2f}")
        plt.axvline(0, color='black', linestyle='-', label="No Change")
        plt.grid(axis='y', alpha=0.3)
        plt.legend(fontsize=12)
        plt.tight_layout()
        rank_delta_file = os.path.join(viz_dir, f'rank_delta_distribution_{timestamp}.png')
        plt.savefig(rank_delta_file, dpi=300)
        print(f"Created rank delta distribution chart")
        
        visualizations.append({
            'title': 'Distribution of Rank Changes',
            'description': 'This chart shows how stock rankings changed from last month. Negative values (left side) indicate improvement, positive values (right side) indicate decline.',
            'file': rank_delta_file,
            'interpretation': 'The distribution shows overall momentum patterns. If most values are negative (left of the black line), it indicates more stocks improved than declined. Conversely, more positive values suggest widespread ranking declines. The spread indicates how dramatic the ranking changes were.'
        })

        # Top improvers (biggest negative rank delta)
        top_improvers = rank_delta.sort_values('RankDelta').head(10)
        plt.figure(figsize=(12, 8))
        bars = sns.barplot(x='RankDelta', y='Name', hue='Name', data=top_improvers, palette='viridis', legend=False)
        
        for i, bar in enumerate(bars.patches):
            value = top_improvers.iloc[i]['RankDelta']
            bars.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f"{int(value)}", va='center')
        
        plt.title(f"Top {len(top_improvers)} Stocks with Greatest Rank Improvement", fontsize=16)
        plt.xlabel("Rank Change (- means improvement)", fontsize=12)
        plt.ylabel("Stock", fontsize=12)
        plt.axvline(x=0, color='gray', linestyle='--')
        plt.grid(True, axis='x', alpha=0.3)
        plt.tight_layout()
        improvers_file = os.path.join(viz_dir, f'top_improvers_{timestamp}.png')
        plt.savefig(improvers_file, dpi=300)
        print(f"Created top improvers chart")
        
        visualizations.append({
            'title': 'Top 10 Rank Improvers (Positive Momentum)',
            'description': 'This chart shows the stocks that improved their ranking the most since the previous month, indicating significant positive momentum.',
            'file': improvers_file,
            'interpretation': 'These stocks are showing strong positive momentum, having climbed the most positions in the rankings. Momentum can be a powerful signal, and these stocks may continue their upward trajectory. The numbers show how many positions each stock climbed (e.g., -50 means the stock moved up 50 positions).'
        })
        
        # Biggest decliners (biggest positive rank delta)
        top_decliners = rank_delta.sort_values('RankDelta', ascending=False).head(10)
        plt.figure(figsize=(12, 8))
        bars = sns.barplot(x='RankDelta', y='Name', hue='Name', data=top_decliners, palette='viridis', legend=False)
        
        for i, bar in enumerate(bars.patches):
            value = top_decliners.iloc[i]['RankDelta']
            bars.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f"{int(value)}", va='center')
        
        plt.title(f"Top {len(top_decliners)} Stocks with Greatest Rank Decline", fontsize=16)
        plt.xlabel("Rank Change (+ means decline)", fontsize=12)
        plt.ylabel("Stock", fontsize=12)
        plt.axvline(x=0, color='gray', linestyle='--')
        plt.grid(True, axis='x', alpha=0.3)
        plt.tight_layout()
        decliners_file = os.path.join(viz_dir, f'top_decliners_{timestamp}.png')
        plt.savefig(decliners_file, dpi=300)
        print(f"Created top decliners chart")
        
        visualizations.append({
            'title': 'Top 10 Rank Decliners (Negative Momentum)',
            'description': 'This chart shows the stocks that declined the most in ranking since the previous month, indicating significant negative momentum.',
            'file': decliners_file,
            'interpretation': 'These stocks are showing strong negative momentum, having dropped the most positions in the rankings. This may indicate underlying problems or changing market conditions affecting these companies. The numbers show how many positions each stock dropped (e.g., 50 means the stock moved down 50 positions).'
        })

    # 6. Return distribution by quartile
    plt.figure(figsize=(12, 8))
    # Create quartiles based on rank
    quartile_labels = ['Top 25%', '25-50%', '50-75%', 'Bottom 25%']
    rankings['Quartile'] = pd.qcut(rankings['Rank'], 4, labels=quartile_labels)
    
    # Create boxplot
    sns.boxplot(x='Quartile', y='YearlyReturn', hue='Quartile', data=rankings, palette='viridis', legend=False)
    plt.title("Return Distribution by Rank Quartile", fontsize=16)
    plt.xlabel("Rank Quartile", fontsize=12)
    plt.ylabel("Yearly Return", fontsize=12)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    quartile_file = os.path.join(viz_dir, f'return_by_quartile_{timestamp}.png')
    plt.savefig(quartile_file, dpi=300)
    print(f"Created return by quartile chart")
    
    visualizations.append({
        'title': 'Return Distribution by Ranking Quartile',
        'description': 'This boxplot shows the distribution of returns within each quartile of the rankings. It helps visualize how returns vary within different ranking groups.',
        'file': quartile_file,
        'interpretation': 'Each box shows the return distribution for a quartile of stocks. The line in the middle of each box is the median return, while the box itself shows the middle 50% of returns. The "whiskers" extend to show the range of returns. This chart helps understand the consistency of returns within each quartile and whether there are significant outliers.'
    })

    # 7. Save summary data as CSV
    top_performers = rankings.sort_values('YearlyReturn', ascending=False).head(20)
    top_performers.to_csv(os.path.join(viz_dir, f'top_performers_{timestamp}.csv'), index=False)
    print(f"Saved top 20 performers data to CSV")

    if 'RankDelta' in rank_delta.columns:
        top_improvers = rank_delta.sort_values('RankDelta').head(20)
        top_improvers.to_csv(os.path.join(viz_dir, f'top_improvers_{timestamp}.csv'), index=False)
        print(f"Saved top 20 improvers data to CSV")
        
        top_decliners = rank_delta.sort_values('RankDelta', ascending=False).head(20)
        top_decliners.to_csv(os.path.join(viz_dir, f'top_decliners_{timestamp}.csv'), index=False)
        print(f"Saved top 20 decliners data to CSV")
    
    # Create the HTML index with explanations
    create_visualization_index(viz_dir, timestamp, visualizations)
    
    print(f"\nAll visualizations have been saved to the '{viz_dir}' directory.")
    print(f"A detailed visualization guide has been created at '{viz_dir}/visualization_index_{timestamp}.html'")
    print("Open this HTML file in any web browser to view all charts with explanations.")

if __name__ == "__main__":
    print("Renaissance Stock Ranking System - Visualization Tool")
    print("====================================================")
    print("Creating visualizations from the latest ranking data...")
    print("This may take a moment depending on the size of your data.")
    print("")
    create_visualizations()
    print("")
    print("Visualization process complete! You can now explore the results.")
    print("For non-technical users: Open the HTML file in the 'output/visualizations' folder")
    print("for an easy-to-understand guide to all the charts.") 