#!/usr/bin/env python
"""
Sector Analysis for Renaissance Stock Ranking System

This script performs sector-based analysis on the ranking outputs from the
Renaissance Stock Ranking System. It provides insights by sector, including
sector performance, contribution to overall returns, and sector-wise rankings.

The analysis is designed to help portfolio managers understand sector dynamics,
identify sector trends, and make more informed investment decisions by considering
both individual stock performance and sector perspectives.

Key Features:
- Sector performance analysis: Average returns, risk metrics, and rankings by sector
- Top stocks by sector: Identification of best performers in each sector
- Sector concentration analysis: Distribution of stocks and returns across sectors
- Financial metrics by sector: Valuation and financial health metrics by sector
- Investment strategy suggestions: Recommendations based on sector analysis

This script can be integrated into the Renaissance Stock Ranking System workflow
to provide deeper insights for portfolio construction and sector allocation decisions.

Usage:
    python docs/sector_analysis.py [options]

Options:
    --output-dir DIR         Directory for analysis outputs (default: output/sector_analysis)
    --rankings-file FILE     Path to rankings file (default: latest in output/)
    --nifty500-file FILE     Path to NIFTY 500 list with sectors (default: data/nifty500_list.csv)
    --metrics-file FILE      Path to financial metrics file (default: latest in output/)

Author: Renaissance Investment Managers
Date: March 2025
Version: 1.0.0
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

# Add the project root to the Python path to enable imports from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def parse_arguments():
    """
    Parse command line arguments for the sector analysis script.
    
    This function defines and processes the command line arguments that control
    the behavior of the sector analysis, including input/output paths and options.
    
    Returns:
        argparse.Namespace: Object containing the parsed command-line arguments with:
            - output_dir: Directory where analysis outputs will be saved
            - rankings_file: Path to the rankings file (or None to use latest)
            - nifty500_file: Path to the NIFTY 500 list file (or None to use latest)
            - metrics_file: Path to the financial metrics file (or None to use latest)
    """
    parser = argparse.ArgumentParser(description='Sector Analysis for Renaissance Stock Ranking System')
    
    # Define the output directory where analysis results will be saved
    parser.add_argument('--output-dir', type=str, default='output/sector_analysis',
                        help='Directory where analysis outputs will be saved')
    
    # Optional path to the rankings file (if not provided, the latest one will be used)
    parser.add_argument('--rankings-file', type=str, default=None,
                        help='Path to the rankings file. If not provided, the latest one will be used.')
    
    # Optional path to the NIFTY 500 list file (if not provided, the latest one will be used)
    parser.add_argument('--nifty500-file', type=str, default=None,
                        help='Path to the NIFTY 500 list file with sector information. If not provided, the latest one will be used.')
    
    # Optional path to the financial metrics file (if not provided, the latest one will be used)
    parser.add_argument('--metrics-file', type=str, default=None,
                        help='Path to the financial metrics file. If not provided, the latest one will be used.')
    
    return parser.parse_args()

def find_latest_file(pattern):
    """
    Find the most recent file matching the specified pattern.
    
    This function is used to automatically find the latest rankings, NIFTY 500 list,
    or financial metrics file when specific paths are not provided by the user.
    It's particularly useful for integrating with the regular workflow where
    the latest outputs should be analyzed.
    
    Args:
        pattern (str): Glob pattern to match files, e.g., 'output/NIFTY500_Rankings_*.csv'
    
    Returns:
        str or None: Path to the most recent file matching the pattern, or None if no files found
    """
    files = glob.glob(pattern)
    if not files:
        return None
    # Sort files by creation time and return the most recent one
    return max(files, key=os.path.getctime)

def load_data(args):
    """
    Load all required data files for sector analysis.
    
    This function orchestrates the loading of three key data sources:
    1. The rankings data (output from the ranking system)
    2. The NIFTY 500 constituent list with sector information
    3. Optional financial metrics data
    
    It then merges these datasets to create a comprehensive DataFrame for analysis.
    The function handles various edge cases, such as missing files or missing columns.
    
    Args:
        args (argparse.Namespace): Command-line arguments containing file paths
    
    Returns:
        pd.DataFrame: Merged DataFrame containing all data for sector analysis with columns:
            - ISIN: International Securities Identification Number
            - Name: Company name
            - Ticker: Stock ticker symbol
            - Rank: Current ranking
            - YearlyReturn: Calculated yearly return (%)
            - Sector: GICS sector classification
            - Additional financial metrics if available (PE_Ratio, PB_Ratio, etc.)
    
    Raises:
        FileNotFoundError: If required data files are not found
    """
    # Find the latest files if specific files are not provided
    rankings_file = args.rankings_file or find_latest_file('output/NIFTY500_Rankings_*.csv')
    nifty500_file = args.nifty500_file or find_latest_file('data/nifty500_list.csv')
    metrics_file = args.metrics_file or find_latest_file('output/financial_metrics.csv')
    
    # Ensure required files exist
    if not rankings_file:
        raise FileNotFoundError("No rankings file found. Please run the main system first.")
    
    if not nifty500_file:
        raise FileNotFoundError("No NIFTY 500 list file found. Please extract data first.")
    
    # Load the rankings data
    print(f"Loading rankings from: {rankings_file}")
    rankings = pd.read_csv(rankings_file)
    
    # Load the NIFTY 500 list with sector information
    print(f"Loading NIFTY 500 list from: {nifty500_file}")
    nifty500 = pd.read_csv(nifty500_file)
    
    # Check if sector information is available
    if 'Sector' not in nifty500.columns:
        print("Warning: Sector information not found in NIFTY 500 list. Analysis will be limited.")
        # Create a default sector column if missing
        nifty500['Sector'] = 'Unknown'
    
    # Load financial metrics if available (optional)
    metrics = None
    if metrics_file and os.path.exists(metrics_file):
        print(f"Loading financial metrics from: {metrics_file}")
        metrics = pd.read_csv(metrics_file)
    else:
        print("Financial metrics file not found. Some analyses will be skipped.")
    
    # Merge rankings with sector information
    # Left join ensures we keep all ranked stocks even if they don't have sector info
    data = pd.merge(rankings, nifty500[['ISIN', 'Sector']], on='ISIN', how='left')
    
    # Add metrics if available
    if metrics is not None:
        data = pd.merge(data, metrics, on='ISIN', how='left')
    
    # Fill any missing sectors with 'Unknown'
    data['Sector'] = data['Sector'].fillna('Unknown')
    
    return data

def analyze_sector_performance(data, output_dir):
    """
    Analyze performance metrics by sector.
    
    This function calculates key performance statistics for each sector and ranks
    them based on average yearly returns. It provides a comprehensive view of
    which sectors are outperforming or underperforming, along with risk metrics
    (standard deviation) and ranking information.
    
    The function:
    1. Calculates performance statistics for each sector (mean, median, std, etc.)
    2. Ranks sectors by their average yearly returns
    3. Generates visualizations of sector performance
    4. Saves results to CSV and image files
    
    Args:
        data (pd.DataFrame): Merged data containing rankings and sector information
        output_dir (str): Directory where output files will be saved
    
    Returns:
        pd.DataFrame: DataFrame with sector performance statistics including:
            - YearlyReturn_mean: Average yearly return for the sector
            - YearlyReturn_median: Median yearly return
            - YearlyReturn_std: Standard deviation (risk measure)
            - YearlyReturn_min/max: Range of returns
            - YearlyReturn_count: Number of stocks in the sector
            - Rank_mean, Rank_median, Rank_min: Ranking statistics
            - Rank_Percentile: Normalized rank (0-100, lower is better)
    """
    print("\nAnalyzing sector performance...")
    
    # Group by sector and calculate various statistics
    sector_stats = data.groupby('Sector').agg({
        'YearlyReturn': ['mean', 'median', 'std', 'min', 'max', 'count'],
        'Rank': ['mean', 'median', 'min']
    })
    
    # Rename columns for clarity (e.g., 'YearlyReturn_mean' instead of ('YearlyReturn', 'mean'))
    sector_stats.columns = [f"{col[0]}_{col[1]}" for col in sector_stats.columns]
    
    # Sort sectors by average yearly return in descending order
    sector_stats = sector_stats.sort_values('YearlyReturn_mean', ascending=False)
    
    # Add rank percentile (lower is better)
    sector_stats['Rank_Percentile'] = sector_stats['Rank_mean'] / data['Rank'].max() * 100
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save sector performance statistics to CSV
    sector_stats.to_csv(f"{output_dir}/sector_performance.csv")
    print(f"Sector performance statistics saved to {output_dir}/sector_performance.csv")
    
    # Create visualization of sector performance
    plt.figure(figsize=(12, 8))
    
    # Create horizontal bar chart of average returns by sector
    ax = sector_stats.sort_values('YearlyReturn_mean').plot(
        y='YearlyReturn_mean', kind='barh', 
        xerr=sector_stats['YearlyReturn_std'],  # Error bars showing standard deviation
        color=plt.cm.viridis(np.linspace(0, 1, len(sector_stats))),  # Colormap for visual appeal
        legend=False
    )
    
    # Add sample size annotations to each bar
    for i, v in enumerate(sector_stats['YearlyReturn_count']):
        ax.text(0.5, i, f"n={int(v)}", va='center', fontsize=10)
    
    # Set chart title and labels
    plt.title('Average Yearly Return by Sector', fontsize=14)
    plt.xlabel('Yearly Return (%)', fontsize=12)
    plt.ylabel('Sector', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    
    # Save the visualization
    plt.savefig(f"{output_dir}/sector_returns.png", dpi=300)
    
    return sector_stats

def analyze_top_stocks_by_sector(data, output_dir):
    """
    Identify and analyze top performing stocks in each sector.
    
    This function creates a detailed profile of the best-performing stocks within
    each sector, which is particularly useful for sector-based portfolio construction.
    It helps investors identify sector champions and understand the characteristics
    of top performers in different sectors.
    
    The function:
    1. Finds the top performing stocks in each sector based on ranking
    2. Creates a detailed text report of the top stocks by sector
    3. Generates a visual comparison of top stocks across sectors
    4. Saves results to text and image files
    
    Args:
        data (pd.DataFrame): Merged data containing rankings, sectors, and metrics
        output_dir (str): Directory where output files will be saved
    
    Returns:
        dict: Dictionary mapping sectors to their top stocks, containing:
            - Keys: Sector names (str)
            - Values: DataFrame of top 10 stocks in that sector
    """
    print("\nIdentifying top stocks by sector...")
    
    # Get the list of all sectors and sort alphabetically
    sectors = sorted(data['Sector'].unique())
    
    # Dictionary to store top stocks for each sector
    top_stocks_by_sector = {}
    
    # Create a detailed text report
    with open(f"{output_dir}/top_stocks_by_sector.txt", 'w') as f:
        # Write report header
        f.write(f"Top Performing Stocks by Sector\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*80}\n\n")
        
        # Process each sector
        for sector in sectors:
            # Get data for this sector and sort by rank (best first)
            sector_data = data[data['Sector'] == sector].sort_values('Rank')
            
            # Write sector header
            f.write(f"\n## {sector} Sector\n\n")
            f.write(f"Average Return: {sector_data['YearlyReturn'].mean():.2f}%\n")
            f.write(f"Number of Stocks: {len(sector_data)}\n\n")
            
            # Write information about top stocks in this sector
            if len(sector_data) > 0:
                f.write("Top 5 Stocks:\n")
                for i, (_, row) in enumerate(sector_data.head(5).iterrows()):
                    # Stock name and identifier
                    f.write(f"{i+1}. {row['Name']} (ISIN: {row['ISIN']})\n")
                    
                    # Performance metrics
                    f.write(f"   - Yearly Return: {row['YearlyReturn']:.2f}%\n")
                    f.write(f"   - Overall Rank: {row['Rank']}\n")
                    
                    # Add financial metrics if available
                    metrics_cols = [col for col in sector_data.columns if col in ['PE_Ratio', 'PB_Ratio', 'ROE', 'DebtToAsset', 'DividendYield']]
                    for metric in metrics_cols:
                        if not pd.isna(row[metric]):
                            f.write(f"   - {metric}: {row[metric]:.2f}\n")
                    f.write("\n")
            
            # Save top 10 stocks from each sector for later visualization
            top_stocks_by_sector[sector] = sector_data.head(10)
    
    print(f"Top stocks by sector analysis saved to {output_dir}/top_stocks_by_sector.txt")
    
    # Create a visual comparison of top stocks across sectors
    plt.figure(figsize=(15, 10))
    
    # Plot only sectors that have at least 3 stocks
    valid_sectors = [sector for sector in sectors if len(data[data['Sector'] == sector]) >= 3]
    num_sectors = len(valid_sectors)
    
    if num_sectors > 0:
        # Create a colormap for visual distinction between sectors
        colors = plt.cm.viridis(np.linspace(0, 1, num_sectors))
        
        # Plot top 3 stocks for each sector
        for i, sector in enumerate(valid_sectors):
            # Get top 3 stocks by return in this sector
            sector_data = data[data['Sector'] == sector].sort_values('YearlyReturn', ascending=False).head(3)
            
            # Calculate positions for bars (staggered by sector)
            positions = np.array([j + i*0.3 for j in range(len(sector_data))])
            returns = sector_data['YearlyReturn'].values
            
            # Plot bars for this sector
            plt.bar(positions, returns, width=0.2, color=colors[i], label=sector, alpha=0.7)
            
            # Add stock names as annotations
            for j, (_, row) in enumerate(sector_data.iterrows()):
                plt.text(positions[j], returns[j] + 1, row['Name'], 
                        ha='center', va='bottom', rotation=90, fontsize=8)
        
        # Add a horizontal line at y=0 to show positive/negative returns
        plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
        
        # Set chart labels and title
        plt.xlabel('Top 3 Stocks by Sector', fontsize=12)
        plt.ylabel('Yearly Return (%)', fontsize=12)
        plt.title('Top 3 Performing Stocks by Sector', fontsize=14)
        plt.xticks([])  # Hide x-axis ticks as they're not meaningful
        plt.legend(title='Sector', loc='best', fontsize=10)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Save the visualization
        plt.savefig(f"{output_dir}/top_stocks_comparison.png", dpi=300)
    
    return top_stocks_by_sector

def analyze_sector_concentration(data, output_dir):
    """
    Analyze the concentration of stocks and returns across sectors.
    
    This function evaluates the distribution of stocks across different sectors
    and how each sector contributes to the overall market returns. This information
    is critical for diversification decisions and understanding market structure.
    
    The analysis helps portfolio managers:
    - Identify overrepresented or underrepresented sectors
    - Understand return contribution relative to sector size
    - Make informed sector allocation decisions
    
    Args:
        data (pd.DataFrame): Merged data containing rankings and sector information
        output_dir (str): Directory where output files will be saved
    
    Returns:
        pd.DataFrame: DataFrame with sector concentration metrics including:
            - Count: Number of stocks in each sector
            - Percentage: Percentage of total stocks by sector
            - ReturnContribution: Percentage contribution to total returns
    
    Note:
        If negative returns are present, absolute values are used for
        the return contribution pie chart (which cannot display negative values).
    """
    print("\nAnalyzing sector concentration...")
    
    # Calculate stock count and percentage by sector
    sector_counts = data['Sector'].value_counts()
    sector_percentages = data['Sector'].value_counts(normalize=True) * 100
    
    # Calculate sector contribution to overall market returns
    # Handle case where sum of returns might be negative or zero
    total_returns = data['YearlyReturn'].sum()
    if total_returns != 0:
        sector_contribution = data.groupby('Sector')['YearlyReturn'].sum() / abs(total_returns) * 100
        # Ensure all values are positive for pie chart
        if (sector_contribution < 0).any():
            # If negative values exist, use absolute values and note in output
            sector_contribution = sector_contribution.abs()
            print("Note: Using absolute values for sector contribution due to negative returns")
    else:
        # If total returns are zero, use equal contribution
        sector_contribution = pd.Series(100 / len(sector_counts), index=sector_counts.index)
    
    # Combine metrics into a single DataFrame
    concentration = pd.DataFrame({
        'Count': sector_counts,
        'Percentage': sector_percentages,
        'ReturnContribution': sector_contribution
    }).fillna(0).sort_values('Count', ascending=False)
    
    # Save concentration metrics to CSV
    concentration.to_csv(f"{output_dir}/sector_concentration.csv")
    print(f"Sector concentration analysis saved to {output_dir}/sector_concentration.csv")
    
    # Create visualizations of sector concentration
    plt.figure(figsize=(12, 6))
    
    # Create two pie charts side by side
    # Left: Distribution of stocks by sector
    plt.subplot(1, 2, 1)
    concentration.plot.pie(y='Count', autopct='%1.1f%%', 
                           startangle=90, shadow=False, 
                           title='Stock Distribution by Sector', ax=plt.gca())
    
    # Right: Contribution to total returns by sector
    plt.subplot(1, 2, 2)
    concentration.plot.pie(y='ReturnContribution', autopct='%1.1f%%',
                           startangle=90, shadow=False, 
                           title='Return Contribution by Sector (Absolute)', ax=plt.gca())
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/sector_concentration.png", dpi=300)
    
    return concentration

def analyze_sector_metrics(data, output_dir):
    """
    Analyze financial metrics by sector.
    
    This function calculates average financial metrics (P/E, P/B, ROE, etc.) for
    each sector, providing insights into relative valuations and financial health
    across sectors. This is particularly valuable for identifying value opportunities
    or determining whether a sector's performance is justified by fundamentals.
    
    The function:
    1. Calculates average financial metrics for each sector
    2. Creates visualizations of key metrics by sector
    3. Saves results to CSV and image files
    
    Args:
        data (pd.DataFrame): Merged data containing rankings, sectors, and financial metrics
        output_dir (str): Directory where output files will be saved
    
    Returns:
        pd.DataFrame or None: DataFrame with sector financial metrics (average values),
                             or None if metrics are unavailable
    
    Note:
        This analysis is skipped if financial metrics are not available in the data.
        These metrics are typically provided by the Bloomberg API extractor.
    """
    print("\nAnalyzing financial metrics by sector...")
    
    # Check if we have financial metrics in the data
    metrics_cols = [col for col in data.columns if col in ['PE_Ratio', 'PB_Ratio', 'ROE', 'DebtToAsset', 'DividendYield']]
    
    # Skip this analysis if no metrics are available
    if not metrics_cols:
        print("No financial metrics available. Skipping sector metrics analysis.")
        return None
    
    # Calculate mean metrics by sector
    metrics_by_sector = data.groupby('Sector')[metrics_cols].mean()
    
    # Save metrics to CSV
    metrics_by_sector.to_csv(f"{output_dir}/sector_metrics.csv")
    print(f"Sector financial metrics saved to {output_dir}/sector_metrics.csv")
    
    # Create visualizations of metrics by sector
    n_metrics = len(metrics_cols)
    fig, axes = plt.subplots(n_metrics, 1, figsize=(12, n_metrics * 4))
    
    # Handle the case where there's only one metric
    if n_metrics == 1:
        axes = [axes]
    
    # Create a bar chart for each metric
    for i, metric in enumerate(metrics_cols):
        # Sort sectors by this specific metric for better visualization
        sorted_metrics = metrics_by_sector.sort_values(metric)
        
        # Plot horizontal bar chart
        sorted_metrics[metric].plot(kind='barh', ax=axes[i])
        axes[i].set_title(f'{metric} by Sector', fontsize=12)
        axes[i].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/sector_metrics.png", dpi=300)
    
    return metrics_by_sector

def generate_sector_report(sector_stats, concentration, metrics_by_sector, output_dir):
    """
    Generate a comprehensive sector analysis report with investment implications.
    
    This function synthesizes the results of the various sector analyses into a single,
    comprehensive report with actionable investment insights. The report is designed
    to provide portfolio managers with clear, actionable information to inform
    sector allocation decisions and stock selection within sectors.
    
    The report includes:
    1. Sector performance summary
    2. Concentration analysis
    3. Financial metrics comparison
    4. Investment strategy suggestions
    5. Conclusions and recommendations
    
    Args:
        sector_stats (pd.DataFrame): Sector performance statistics
        concentration (pd.DataFrame): Sector concentration metrics
        metrics_by_sector (pd.DataFrame): Financial metrics by sector
        output_dir (str): Directory where the report will be saved
    """
    print("\nGenerating sector analysis report...")
    
    with open(f"{output_dir}/sector_analysis_report.txt", 'w') as f:
        # Report header
        f.write("Renaissance Stock Ranking System - Sector Analysis Report\n")
        f.write("=====================================================\n\n")
        f.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Section 1: Sector Performance Summary
        f.write("1. Sector Performance Summary\n")
        f.write("-----------------------------\n\n")
        
        # Top performing sectors
        f.write("Top 3 performing sectors:\n")
        for i, (sector, row) in enumerate(sector_stats.head(3).iterrows()):
            f.write(f"{i+1}. {sector}: {row['YearlyReturn_mean']:.2f}% avg. return (n={int(row['YearlyReturn_count'])})\n")
        
        # Bottom performing sectors
        f.write("\nBottom 3 performing sectors:\n")
        for i, (sector, row) in enumerate(sector_stats.tail(3).iterrows()):
            f.write(f"{i+1}. {sector}: {row['YearlyReturn_mean']:.2f}% avg. return (n={int(row['YearlyReturn_count'])})\n")
        
        # Section 2: Sector Concentration
        f.write("\n\n2. Sector Concentration\n")
        f.write("------------------------\n\n")
        
        # Sectors by number of stocks
        f.write("Sectors by number of ranked stocks:\n")
        for i, (sector, row) in enumerate(concentration.head(5).iterrows()):
            f.write(f"{i+1}. {sector}: {int(row['Count'])} stocks ({row['Percentage']:.1f}% of total)\n")
        
        # Sectors by contribution to returns
        f.write("\nSectors by contribution to total returns:\n")
        for i, (sector, value) in enumerate(concentration.sort_values('ReturnContribution', ascending=False).head(5)['ReturnContribution'].items()):
            f.write(f"{i+1}. {sector}: {value:.1f}% of total returns\n")
        
        # Section 3: Financial Metrics by Sector (if available)
        if metrics_by_sector is not None:
            f.write("\n\n3. Financial Metrics by Sector\n")
            f.write("------------------------------\n\n")
            
            metrics_cols = metrics_by_sector.columns
            
            # For each metric, show highest, lowest, and average values
            for metric in metrics_cols:
                f.write(f"\n{metric}:\n")
                f.write(f"  Highest: {metrics_by_sector[metric].idxmax()} ({metrics_by_sector[metric].max():.2f})\n")
                f.write(f"  Lowest: {metrics_by_sector[metric].idxmin()} ({metrics_by_sector[metric].min():.2f})\n")
                f.write(f"  Average across all sectors: {metrics_by_sector[metric].mean():.2f}\n")
        
        # Section 4: Investment Implications
        f.write("\n\n4. Investment Implications\n")
        f.write("---------------------------\n\n")
        f.write("Based on the sector analysis, consider the following investment strategies:\n\n")
        
        # Generate investment strategy suggestions based on the analysis
        if metrics_by_sector is not None and 'PE_Ratio' in metrics_by_sector.columns:
            # Identify value opportunities (high returns + low PE)
            top_return_sectors = set(sector_stats.head(5).index)
            low_pe_sectors = set(metrics_by_sector.sort_values('PE_Ratio').head(5).index)
            value_sectors = top_return_sectors.intersection(low_pe_sectors)
            
            if value_sectors:
                f.write("a) Value Opportunity Sectors (high returns with lower valuations):\n")
                for sector in value_sectors:
                    f.write(f"   - {sector}: {sector_stats.loc[sector, 'YearlyReturn_mean']:.2f}% return, " + 
                           f"PE: {metrics_by_sector.loc[sector, 'PE_Ratio']:.2f}\n")
            
            # High growth sectors (regardless of valuation)
            high_growth = sector_stats.head(3).index
            f.write("\nb) Growth Focus Sectors (highest returns, regardless of valuation):\n")
            for sector in high_growth:
                f.write(f"   - {sector}: {sector_stats.loc[sector, 'YearlyReturn_mean']:.2f}% average return\n")
            
            # Diversification suggestions
            f.write("\nc) Diversification Opportunities:\n")
            f.write("   Consider allocation across the following sectors for diversification:\n")
            # Get 5 sectors distributed across the performance range
            diverse_sectors = sector_stats.iloc[::max(1, len(sector_stats)//5)].index[:5]
            for sector in diverse_sectors:
                f.write(f"   - {sector}\n")
        
        # Section 5: Conclusion
        f.write("\n\n5. Conclusion\n")
        f.write("-------------\n\n")
        
        # Summarize key findings
        top_sector = sector_stats.index[0]
        worst_sector = sector_stats.index[-1]
        f.write(f"The {top_sector} sector has shown the strongest performance with " +
               f"{sector_stats.loc[top_sector, 'YearlyReturn_mean']:.2f}% average returns, while the " +
               f"{worst_sector} sector has underperformed with " +
               f"{sector_stats.loc[worst_sector, 'YearlyReturn_mean']:.2f}% average returns.\n\n")
        
        # Final recommendations
        f.write("This sector analysis should be used alongside individual stock analysis to develop a " +
               "comprehensive investment strategy. Market conditions can change rapidly, so regular " +
               "review of sector performance is recommended.\n")
    
    print(f"Comprehensive sector analysis report saved to {output_dir}/sector_analysis_report.txt")

def main():
    """
    Main function to orchestrate the sector analysis workflow.
    
    This function coordinates the entire sector analysis process from start to finish,
    handling command-line arguments, data loading, performing various analyses, and
    generating the final report. It implements a proper error handling strategy and
    provides informative progress updates throughout the process.
    
    Workflow:
    1. Parse command-line arguments
    2. Load required data files
    3. Perform various sector analyses
    4. Generate comprehensive report
    5. Save all results to the specified output directory
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Print header
    print("\nRenaissance Stock Ranking System - Sector Analysis")
    print("==================================================")
    
    try:
        # Step 1: Load all required data
        data = load_data(args)
        
        # Step 2: Perform sector analyses
        sector_stats = analyze_sector_performance(data, args.output_dir)
        top_stocks = analyze_top_stocks_by_sector(data, args.output_dir)
        concentration = analyze_sector_concentration(data, args.output_dir)
        metrics_by_sector = analyze_sector_metrics(data, args.output_dir)
        
        # Step 3: Generate comprehensive report
        generate_sector_report(sector_stats, concentration, metrics_by_sector, args.output_dir)
        
        # Print success message
        print("\nSector analysis completed successfully.")
        print(f"Results saved to {args.output_dir}")
        
    except Exception as e:
        # Handle any errors that occur during processing
        print(f"\nError during sector analysis: {str(e)}")
        return 1  # Return error code
    
    return 0  # Return success code

if __name__ == "__main__":
    # Execute the main function and exit with the returned status code
    exit(main()) 