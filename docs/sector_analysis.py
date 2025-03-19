#!/usr/bin/env python
"""
Sector Analysis for Renaissance Stock Ranking System

This script performs sector-based analysis on the ranking outputs from the
Renaissance Stock Ranking System. It provides insights by sector, including
sector performance, contribution to overall returns, and sector-wise rankings.

Usage:
    python docs/sector_analysis.py [--output-dir output/sector_analysis]

Features:
- Sector performance analysis
- Top stocks by sector
- Sector concentration analysis
- Sector momentum tracking
- Visualization of sector trends
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import glob

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Sector Analysis for Renaissance Stock Ranking System')
    
    parser.add_argument('--output-dir', type=str, default='output/sector_analysis',
                        help='Directory where analysis outputs will be saved')
    
    parser.add_argument('--rankings-file', type=str, default=None,
                        help='Path to the rankings file. If not provided, the latest one will be used.')
    
    parser.add_argument('--nifty500-file', type=str, default=None,
                        help='Path to the NIFTY 500 list file with sector information. If not provided, the latest one will be used.')
    
    parser.add_argument('--metrics-file', type=str, default=None,
                        help='Path to the financial metrics file. If not provided, the latest one will be used.')
    
    return parser.parse_args()

def find_latest_file(pattern):
    """Find the most recent file matching a pattern."""
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def load_data(args):
    """Load all required data files."""
    # Find the latest files if not specified
    rankings_file = args.rankings_file or find_latest_file('output/NIFTY500_Rankings_*.csv')
    nifty500_file = args.nifty500_file or find_latest_file('data/nifty500_list.csv')
    metrics_file = args.metrics_file or find_latest_file('output/financial_metrics.csv')
    
    if not rankings_file:
        raise FileNotFoundError("No rankings file found. Please run the main system first.")
    
    if not nifty500_file:
        raise FileNotFoundError("No NIFTY 500 list file found. Please extract data first.")
    
    # Load data files
    print(f"Loading rankings from: {rankings_file}")
    rankings = pd.read_csv(rankings_file)
    
    print(f"Loading NIFTY 500 list from: {nifty500_file}")
    nifty500 = pd.read_csv(nifty500_file)
    
    # Check if sector information is available
    if 'Sector' not in nifty500.columns:
        print("Warning: Sector information not found in NIFTY 500 list. Analysis will be limited.")
        nifty500['Sector'] = 'Unknown'
    
    # Load financial metrics if available
    metrics = None
    if metrics_file and os.path.exists(metrics_file):
        print(f"Loading financial metrics from: {metrics_file}")
        metrics = pd.read_csv(metrics_file)
    else:
        print("Financial metrics file not found. Some analyses will be skipped.")
    
    # Merge rankings with sector information
    data = pd.merge(rankings, nifty500[['ISIN', 'Sector']], on='ISIN', how='left')
    
    # Add metrics if available
    if metrics is not None:
        data = pd.merge(data, metrics, on='ISIN', how='left')
    
    # Fill any missing sectors
    data['Sector'] = data['Sector'].fillna('Unknown')
    
    return data

def analyze_sector_performance(data, output_dir):
    """Analyze performance by sector."""
    print("\nAnalyzing sector performance...")
    
    # Group by sector and calculate statistics
    sector_stats = data.groupby('Sector').agg({
        'YearlyReturn': ['mean', 'median', 'std', 'min', 'max', 'count'],
        'Rank': ['mean', 'median', 'min']
    })
    
    # Rename and sort columns for clarity
    sector_stats.columns = [f"{col[0]}_{col[1]}" for col in sector_stats.columns]
    sector_stats = sector_stats.sort_values('YearlyReturn_mean', ascending=False)
    
    # Add rank percentile (lower is better)
    sector_stats['Rank_Percentile'] = sector_stats['Rank_mean'] / data['Rank'].max() * 100
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    sector_stats.to_csv(f"{output_dir}/sector_performance.csv")
    print(f"Sector performance statistics saved to {output_dir}/sector_performance.csv")
    
    # Create visualizations
    plt.figure(figsize=(12, 8))
    ax = sector_stats.sort_values('YearlyReturn_mean').plot(
        y='YearlyReturn_mean', kind='barh', 
        xerr=sector_stats['YearlyReturn_std'],
        color=plt.cm.viridis(np.linspace(0, 1, len(sector_stats))),
        legend=False
    )
    
    # Add count annotations
    for i, v in enumerate(sector_stats['YearlyReturn_count']):
        ax.text(0.5, i, f"n={int(v)}", va='center', fontsize=10)
    
    plt.title('Average Yearly Return by Sector', fontsize=14)
    plt.xlabel('Yearly Return (%)', fontsize=12)
    plt.ylabel('Sector', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/sector_returns.png", dpi=300)
    
    return sector_stats

def analyze_top_stocks_by_sector(data, output_dir):
    """Find top performing stocks in each sector."""
    print("\nIdentifying top stocks by sector...")
    
    sectors = sorted(data['Sector'].unique())
    top_stocks_by_sector = {}
    
    # Create a nice formatted output
    with open(f"{output_dir}/top_stocks_by_sector.txt", 'w') as f:
        f.write(f"Top Performing Stocks by Sector\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*80}\n\n")
        
        for sector in sectors:
            sector_data = data[data['Sector'] == sector].sort_values('Rank')
            f.write(f"\n## {sector} Sector\n\n")
            f.write(f"Average Return: {sector_data['YearlyReturn'].mean():.2f}%\n")
            f.write(f"Number of Stocks: {len(sector_data)}\n\n")
            
            if len(sector_data) > 0:
                f.write("Top 5 Stocks:\n")
                for i, (_, row) in enumerate(sector_data.head(5).iterrows()):
                    f.write(f"{i+1}. {row['Name']} (ISIN: {row['ISIN']})\n")
                    f.write(f"   - Yearly Return: {row['YearlyReturn']:.2f}%\n")
                    f.write(f"   - Overall Rank: {row['Rank']}\n")
                    
                    # Add financial metrics if available
                    metrics_cols = [col for col in sector_data.columns if col in ['PE_Ratio', 'PB_Ratio', 'ROE', 'DebtToAsset', 'DividendYield']]
                    for metric in metrics_cols:
                        if not pd.isna(row[metric]):
                            f.write(f"   - {metric}: {row[metric]:.2f}\n")
                    f.write("\n")
            
            # Save top 10 stocks from each sector to a dictionary for later visualization
            top_stocks_by_sector[sector] = sector_data.head(10)
    
    print(f"Top stocks by sector analysis saved to {output_dir}/top_stocks_by_sector.txt")
    
    # Create a visual comparison of top stocks across sectors
    plt.figure(figsize=(15, 10))
    
    # Plot only sectors with at least 3 stocks
    valid_sectors = [sector for sector in sectors if len(data[data['Sector'] == sector]) >= 3]
    num_sectors = len(valid_sectors)
    
    if num_sectors > 0:
        colors = plt.cm.viridis(np.linspace(0, 1, num_sectors))
        
        for i, sector in enumerate(valid_sectors):
            sector_data = data[data['Sector'] == sector].sort_values('YearlyReturn', ascending=False).head(3)
            positions = np.array([j + i*0.3 for j in range(len(sector_data))])
            returns = sector_data['YearlyReturn'].values
            
            plt.bar(positions, returns, width=0.2, color=colors[i], label=sector, alpha=0.7)
            
            # Add stock names as annotations
            for j, (_, row) in enumerate(sector_data.iterrows()):
                plt.text(positions[j], returns[j] + 1, row['Name'], 
                        ha='center', va='bottom', rotation=90, fontsize=8)
        
        plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
        plt.xlabel('Top 3 Stocks by Sector', fontsize=12)
        plt.ylabel('Yearly Return (%)', fontsize=12)
        plt.title('Top 3 Performing Stocks by Sector', fontsize=14)
        plt.xticks([])
        plt.legend(title='Sector', loc='best', fontsize=10)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/top_stocks_comparison.png", dpi=300)
    
    return top_stocks_by_sector

def analyze_sector_concentration(data, output_dir):
    """Analyze concentration of stocks within sectors."""
    print("\nAnalyzing sector concentration...")
    
    # Sector distribution
    sector_counts = data['Sector'].value_counts()
    sector_percentages = data['Sector'].value_counts(normalize=True) * 100
    
    # Sector contribution to overall market (based on ranked stocks)
    sector_contribution = data.groupby('Sector')['YearlyReturn'].sum() / data['YearlyReturn'].sum() * 100
    
    # Combine metrics
    concentration = pd.DataFrame({
        'Count': sector_counts,
        'Percentage': sector_percentages,
        'ReturnContribution': sector_contribution
    }).fillna(0).sort_values('Count', ascending=False)
    
    # Save to CSV
    concentration.to_csv(f"{output_dir}/sector_concentration.csv")
    print(f"Sector concentration analysis saved to {output_dir}/sector_concentration.csv")
    
    # Visualize concentration
    plt.figure(figsize=(12, 6))
    
    # Plot count and contribution
    plt.subplot(1, 2, 1)
    concentration.plot.pie(y='Count', autopct='%1.1f%%', 
                           startangle=90, shadow=False, 
                           title='Stock Distribution by Sector', ax=plt.gca())
    
    plt.subplot(1, 2, 2)
    concentration.plot.pie(y='ReturnContribution', autopct='%1.1f%%',
                           startangle=90, shadow=False, 
                           title='Return Contribution by Sector', ax=plt.gca())
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/sector_concentration.png", dpi=300)
    
    return concentration

def analyze_sector_metrics(data, output_dir):
    """Analyze financial metrics by sector."""
    print("\nAnalyzing financial metrics by sector...")
    
    # Check if we have financial metrics
    metrics_cols = [col for col in data.columns if col in ['PE_Ratio', 'PB_Ratio', 'ROE', 'DebtToAsset', 'DividendYield']]
    
    if not metrics_cols:
        print("No financial metrics available. Skipping sector metrics analysis.")
        return None
    
    # Mean metrics by sector
    metrics_by_sector = data.groupby('Sector')[metrics_cols].mean()
    metrics_by_sector.to_csv(f"{output_dir}/sector_metrics.csv")
    print(f"Sector financial metrics saved to {output_dir}/sector_metrics.csv")
    
    # Visualize metrics by sector
    n_metrics = len(metrics_cols)
    fig, axes = plt.subplots(n_metrics, 1, figsize=(12, n_metrics * 4))
    
    if n_metrics == 1:
        axes = [axes]  # Handle single metric case
    
    for i, metric in enumerate(metrics_cols):
        # Sort for this specific metric
        sorted_metrics = metrics_by_sector.sort_values(metric)
        sorted_metrics[metric].plot(kind='barh', ax=axes[i])
        axes[i].set_title(f'{metric} by Sector', fontsize=12)
        axes[i].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/sector_metrics.png", dpi=300)
    
    return metrics_by_sector

def generate_sector_report(sector_stats, concentration, metrics_by_sector, output_dir):
    """Generate a comprehensive sector analysis report."""
    print("\nGenerating sector analysis report...")
    
    with open(f"{output_dir}/sector_analysis_report.txt", 'w') as f:
        f.write("Renaissance Stock Ranking System - Sector Analysis Report\n")
        f.write("=====================================================\n\n")
        f.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Sector performance summary
        f.write("1. Sector Performance Summary\n")
        f.write("-----------------------------\n\n")
        f.write("Top 3 performing sectors:\n")
        for i, (sector, row) in enumerate(sector_stats.head(3).iterrows()):
            f.write(f"{i+1}. {sector}: {row['YearlyReturn_mean']:.2f}% avg. return (n={int(row['YearlyReturn_count'])})\n")
        
        f.write("\nBottom 3 performing sectors:\n")
        for i, (sector, row) in enumerate(sector_stats.tail(3).iterrows()):
            f.write(f"{i+1}. {sector}: {row['YearlyReturn_mean']:.2f}% avg. return (n={int(row['YearlyReturn_count'])})\n")
        
        # Sector concentration
        f.write("\n\n2. Sector Concentration\n")
        f.write("------------------------\n\n")
        f.write("Sectors by number of ranked stocks:\n")
        for i, (sector, row) in enumerate(concentration.head(5).iterrows()):
            f.write(f"{i+1}. {sector}: {int(row['Count'])} stocks ({row['Percentage']:.1f}% of total)\n")
        
        f.write("\nSectors by contribution to total returns:\n")
        for i, (sector, value) in enumerate(concentration.sort_values('ReturnContribution', ascending=False).head(5)['ReturnContribution'].items()):
            f.write(f"{i+1}. {sector}: {value:.1f}% of total returns\n")
        
        # Financial metrics by sector
        if metrics_by_sector is not None:
            f.write("\n\n3. Financial Metrics by Sector\n")
            f.write("------------------------------\n\n")
            
            metrics_cols = metrics_by_sector.columns
            
            for metric in metrics_cols:
                f.write(f"\n{metric}:\n")
                f.write(f"  Highest: {metrics_by_sector[metric].idxmax()} ({metrics_by_sector[metric].max():.2f})\n")
                f.write(f"  Lowest: {metrics_by_sector[metric].idxmin()} ({metrics_by_sector[metric].min():.2f})\n")
                f.write(f"  Average across all sectors: {metrics_by_sector[metric].mean():.2f}\n")
        
        # Investment implications
        f.write("\n\n4. Investment Implications\n")
        f.write("---------------------------\n\n")
        f.write("Based on the sector analysis, consider the following investment strategies:\n\n")
        
        # Get top performing sectors with low valuation
        if metrics_by_sector is not None and 'PE_Ratio' in metrics_by_sector.columns:
            top_return_sectors = set(sector_stats.head(5).index)
            low_pe_sectors = set(metrics_by_sector.sort_values('PE_Ratio').head(5).index)
            value_sectors = top_return_sectors.intersection(low_pe_sectors)
            
            if value_sectors:
                f.write("a) Value Opportunity Sectors (high returns with lower valuations):\n")
                for sector in value_sectors:
                    f.write(f"   - {sector}: {sector_stats.loc[sector, 'YearlyReturn_mean']:.2f}% return, " + 
                           f"PE: {metrics_by_sector.loc[sector, 'PE_Ratio']:.2f}\n")
            
            # High growth sectors
            high_growth = sector_stats.head(3).index
            f.write("\nb) Growth Focus Sectors (highest returns, regardless of valuation):\n")
            for sector in high_growth:
                f.write(f"   - {sector}: {sector_stats.loc[sector, 'YearlyReturn_mean']:.2f}% average return\n")
            
            # Diversification suggestions
            f.write("\nc) Diversification Opportunities:\n")
            f.write("   Consider allocation across the following sectors for diversification:\n")
            diverse_sectors = sector_stats.iloc[::max(1, len(sector_stats)//5)].index[:5]  # Get 5 sectors across the performance range
            for sector in diverse_sectors:
                f.write(f"   - {sector}\n")
        
        f.write("\n\n5. Conclusion\n")
        f.write("-------------\n\n")
        top_sector = sector_stats.index[0]
        worst_sector = sector_stats.index[-1]
        f.write(f"The {top_sector} sector has shown the strongest performance with " +
               f"{sector_stats.loc[top_sector, 'YearlyReturn_mean']:.2f}% average returns, while the " +
               f"{worst_sector} sector has underperformed with " +
               f"{sector_stats.loc[worst_sector, 'YearlyReturn_mean']:.2f}% average returns.\n\n")
        
        f.write("This sector analysis should be used alongside individual stock analysis to develop a " +
               "comprehensive investment strategy. Market conditions can change rapidly, so regular " +
               "review of sector performance is recommended.\n")
    
    print(f"Comprehensive sector analysis report saved to {output_dir}/sector_analysis_report.txt")

def main():
    """Main function to perform sector analysis."""
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("\nRenaissance Stock Ranking System - Sector Analysis")
    print("==================================================")
    
    try:
        # Load all required data
        data = load_data(args)
        
        # Perform sector analyses
        sector_stats = analyze_sector_performance(data, args.output_dir)
        top_stocks = analyze_top_stocks_by_sector(data, args.output_dir)
        concentration = analyze_sector_concentration(data, args.output_dir)
        metrics_by_sector = analyze_sector_metrics(data, args.output_dir)
        
        # Generate comprehensive report
        generate_sector_report(sector_stats, concentration, metrics_by_sector, args.output_dir)
        
        print("\nSector analysis completed successfully.")
        print(f"Results saved to {args.output_dir}")
        
    except Exception as e:
        print(f"\nError during sector analysis: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 