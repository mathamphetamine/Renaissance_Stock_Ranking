# Sector Analysis for Renaissance Stock Ranking System

## Overview

The sector analysis component enhances the Renaissance Stock Ranking System by providing sector-based insights derived from the individual stock rankings. While the core system ranks stocks based on yearly returns, this module adds another dimension by analyzing performance, concentration, and financial metrics at the sector level.

This additional perspective enables portfolio managers to:

- Identify outperforming and underperforming sectors
- Understand sector dynamics and trends
- Make informed sector allocation decisions
- Find top-performing stocks within specific sectors
- Balance sector exposure for optimal diversification

## Key Features

### 1. Sector Performance Analysis

- **Calculates key statistics by sector**: Average return, median return, standard deviation, min/max returns
- **Ranks sectors** by performance metrics
- **Visualizes sector performance** with informative charts
- **Includes risk metrics** (standard deviation) to understand volatility by sector

### 2. Top Stocks by Sector

- **Identifies the best-performing stocks within each sector**
- **Creates detailed profiles** of top performers in each sector
- **Generates visual comparisons** of top stocks across sectors
- **Highlights sector champions** for targeted investment

### 3. Sector Concentration Analysis

- **Evaluates the distribution of stocks across sectors**
- **Analyzes how each sector contributes to overall market returns**
- **Creates visualizations of sector distribution and contribution**
- **Helps identify overrepresented or underrepresented sectors**

### 4. Financial Metrics by Sector

- **Calculates average financial metrics for each sector**, including:
  - Price-to-Earnings Ratio (P/E)
  - Price-to-Book Ratio (P/B)
  - Return on Equity (ROE)
  - Debt-to-Asset Ratio
  - Dividend Yield
- **Visualizes metrics by sector** for easy comparison
- **Enables identification of value opportunities** (sectors with strong performance but low valuations)

### 5. Comprehensive Report Generation

- **Synthesizes findings into an actionable report**
- **Provides investment strategy suggestions** based on sector analysis
- **Highlights value opportunities, growth sectors, and diversification strategies**
- **Delivers clear, actionable insights** for portfolio managers

## Requirements

- Completed ranking analysis from the main system
- NIFTY 500 constituent list with sector information
- (Optional) Financial metrics for enhanced analysis

## Usage

### Basic Usage

```bash
python docs/sector_analysis.py
```

This will automatically:
1. Find the latest ranking outputs
2. Load the NIFTY 500 list with sector information
3. Load financial metrics if available
4. Perform all sector analyses
5. Generate outputs in the `output/sector_analysis` directory

### Advanced Options

```bash
python docs/sector_analysis.py --output-dir custom/output/path --rankings-file path/to/rankings.csv --nifty500-file path/to/nifty500_with_sectors.csv --metrics-file path/to/metrics.csv
```

### Command-line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--output-dir` | Directory where analysis outputs will be saved | `output/sector_analysis` |
| `--rankings-file` | Path to the rankings file | Latest in `output/` |
| `--nifty500-file` | Path to the NIFTY 500 list with sectors | `data/nifty500_list.csv` |
| `--metrics-file` | Path to the financial metrics file | Latest in `output/` |

## Output Files

The sector analysis generates the following outputs:

| File | Description |
|------|-------------|
| `sector_performance.csv` | Statistical performance metrics for each sector |
| `sector_returns.png` | Visualization of average yearly returns by sector |
| `top_stocks_by_sector.txt` | Detailed report of top performers in each sector |
| `top_stocks_comparison.png` | Visual comparison of top stocks across sectors |
| `sector_concentration.csv` | Analysis of sector distribution and contribution |
| `sector_concentration.png` | Visualization of sector distribution and contribution |
| `sector_metrics.csv` | Financial metrics averaged by sector |
| `sector_metrics.png` | Visualizations of financial metrics by sector |
| `sector_analysis_report.txt` | Comprehensive analysis report with investment implications |

## Using Sector Analysis in Portfolio Construction

The sector analysis outputs can be used in several ways to enhance portfolio construction:

### 1. Sector Rotation Strategy

Use the sector performance analysis to identify the strongest performing sectors and adjust allocations to overweight these sectors in the portfolio.

### 2. Targeted Stock Selection

Combine the main ranking system's stock-level insights with sector analysis to identify the highest-ranked stocks within the top-performing sectors.

### 3. Risk Management Through Diversification

Use the sector concentration analysis to ensure proper diversification across sectors, avoiding overexposure to any single sector.

### 4. Value Opportunity Identification

Look for sectors with strong performance but relatively low valuation metrics (P/E, P/B) as potential value opportunities.

### 5. Quality Enhancement

Use sector-level financial metrics to focus on sectors with high-quality characteristics (high ROE, low debt, sustainable dividends).

## Integration with Bloomberg API

When using the Bloomberg API integration:

1. The `bloomberg_data_extractor.py` script automatically retrieves GICS sector classifications for all NIFTY 500 constituents
2. It also collects key financial metrics that enhance the sector analysis
3. This data is seamlessly integrated into the sector analysis workflow

For more information on the Bloomberg API integration, see the [Bloomberg API Guide](bloomberg_api_guide.md).

## Examples

### Identifying Sector Trends

```python
import pandas as pd

# Load sector performance data
sector_performance = pd.read_csv('output/sector_analysis/sector_performance.csv')

# Identify top 3 sectors by average return
top_sectors = sector_performance.sort_values('YearlyReturn_mean', ascending=False).head(3)
print("Top 3 sectors:", top_sectors.index.tolist())

# Identify sectors with best risk-adjusted returns (return / std)
sector_performance['RiskAdjustedReturn'] = sector_performance['YearlyReturn_mean'] / sector_performance['YearlyReturn_std']
best_risk_adjusted = sector_performance.sort_values('RiskAdjustedReturn', ascending=False).head(3)
print("Best risk-adjusted returns:", best_risk_adjusted.index.tolist())
```

### Creating a Sector-Based Portfolio

```python
import pandas as pd

# Load individual stock rankings and sector data
rankings = pd.read_csv('output/NIFTY500_Rankings_20250315.csv')
nifty500 = pd.read_csv('data/nifty500_list.csv')

# Merge to get sector information
data = pd.merge(rankings, nifty500[['ISIN', 'Sector']], on='ISIN')

# Load sector performance to identify top sectors
sector_performance = pd.read_csv('output/sector_analysis/sector_performance.csv')
top_3_sectors = sector_performance.sort_values('YearlyReturn_mean', ascending=False).head(3).index

# Get top 5 stocks from each of the top 3 sectors
portfolio = []
for sector in top_3_sectors:
    top_stocks = data[data['Sector'] == sector].sort_values('Rank').head(5)
    portfolio.append(top_stocks)

# Combine into a single portfolio DataFrame
portfolio_df = pd.concat(portfolio)
print(f"Portfolio contains {len(portfolio_df)} stocks from the top 3 sectors")
print(portfolio_df[['Name', 'Sector', 'Rank', 'YearlyReturn']])
```

## Author

Renaissance Investment Managers

## Version

1.0.0 (March 2025) 