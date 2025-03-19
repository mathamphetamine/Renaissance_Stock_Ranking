# Automated Stock Ranking System for Renaissance Investment Managers

## Project Overview
This project implements an automated stock ranking system for Renaissance Investment Managers. The system is designed to replace a manual process of collecting and analyzing stock data with an efficient Python-based solution. It automates the calculation of yearly returns for NIFTY 500 stocks on a monthly rolling basis, ranks stocks based on these returns, and analyzes rank changes month-over-month.

```
┌───────────────────────────────────────────────────────────┐
│                                                             │
│                 Renaissance Stock Ranking System            │
│                                                             │
└─────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Bloomberg     │     │ CSV Files     │     │ Data          │
│ Terminal      │────>│ - NIFTY 500   │────>│ Loader        │
│ (Data Source) │     │ - Prices      │     │               │
└───────────────┘     └───────────────┘     └───────┬───────┘
                                                    │
                                                    ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Output        │     │ Rank Delta    │     │ Return        │
│ Generator     │<────│ Calculator    │<────│ Calculator    │
│               │     │               │     │               │
└───────┬───────┘     └───────┬───────┘     └───────────────┘
        │                     │
        │                     ▼
        │             ┌───────────────┐
        │             │ Ranking       │
        │             │ System        │
        │             │               │
        │             └───────┬───────┘
        │                     │
        ▼                     │
┌───────────────┐             │
│ Output Files  │<────────────┘
│ - Rankings    │
│ - Rank Delta  │
│ - Summary     │
└───────────────┘
```

## Package Architecture (New!)
```
┌─────────────────────────────────────────────────────────────────┐
│                   Renaissance Package Structure                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │    core     │  │  analysis   │  │visualization│  │   cli   │ │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────┤ │
│  │data_loader  │  │    sector   │  │             │  │  main   │ │
│  │return_calc  │──▶│   analysis  │◀─┤  visualize  │◀─┤ analyze │ │
│  │ranking_sys  │  │             │  │             │  │visualize│ │
│  │output_gen   │  └─────────────┘  └─────────────┘  └─────────┘ │
│  └─────────────┘         ▲                ▲              │      │
│        │                 │                │              │      │
│        │                 └────────────────┼──────────────┘      │
│        │                                  │                     │
│        │                                  │                     │
│  ┌─────▼────────┐                  ┌─────▼─────────┐            │
│  │      data    │                  │ data_extraction│            │
│  │  extraction  │◀─────────────────┤     cli       │            │
│  │              │                  │               │            │
│  └──────────────┘                  └───────────────┘            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Problem Statement
Previously, Renaissance Investment Managers relied on a manual process for:
- Downloading historical month-end closing prices from various sources
- Maintaining this data in Excel spreadsheets
- Performing calculations manually
- Manually adjusting historical data for corporate actions (splits, dividends, etc.)

This manual approach had several drawbacks:
- **Time inefficiency**: Hours spent on data collection and manipulation
- **Data inaccuracy risks**: Manual entry and calculation errors
- **Scalability issues**: Difficult to expand analysis to more stocks or metrics
- **Complex corporate action handling**: Tedious, error-prone adjustments for stock splits, dividends, etc.

## Solution
This Python-based system addresses these issues by:
- Automating the loading and processing of data extracted from Bloomberg Terminal
- Handling calculations programmatically with high accuracy
- Using ISINs for robust security identification (immune to ticker changes)
- Supporting corporate action adjusted data (leveraging Bloomberg's automatic adjustments)
- Generating clear, structured outputs for easy interpretation

## Key Features
- **Historical Data Analysis**: Analyzes historical monthly price data to calculate yearly returns
- **Performance Ranking**: Ranks stocks from best to worst based on calculated yearly returns
- **Rank Change Tracking**: Tracks month-to-month rank changes to identify improving or declining stocks
- **Data Visualization**: Automatically generates insightful charts and graphs from ranked data without requiring Python knowledge
- **Sector Analysis**: Analyzes stock performance by sector, identifying top-performing sectors and sector concentration metrics
- **Financial Metrics Integration**: Incorporates key financial metrics (P/E, P/B, ROE, etc.) for deeper analysis
- **Comprehensive Output**: Produces detailed CSV files with ranking results and performance metrics
- **Flexible Configuration**: Easily customizable through command-line parameters
- **Bloomberg API Integration**: Optional automated data extraction including sector information and financial metrics
- **Modern Package Structure**: Organized as a proper Python package for easy installation and use

## Project Structure
```
Renaissance_Stock_Ranking/
├── data/                  # Directory for storing input data files
│   └── sample/            # Sample data files for testing
├── docs/                  # Documentation
│   ├── data_extraction_guide.md  # Guide for Bloomberg data extraction
│   ├── bloomberg_api_guide.md    # Guide for Bloomberg API integration
│   ├── user_guide.md             # Detailed user guide
│   ├── README_sector_analysis.md # Guide for sector analysis
│   └── img/                      # Images for documentation
├── examples/              # Example notebooks and scripts
│   └── example_usage.ipynb       # Jupyter notebook with examples
├── output/                # Generated output files (created when run)
│   ├── sector_analysis/   # Sector analysis outputs (created when run)
│   └── visualizations/    # Visualization outputs (created when run)
├── renaissance/           # Main package directory
│   ├── analysis/          # Analysis modules
│   │   └── sector_analysis.py    # Sector analysis functionality
│   ├── cli/               # Command-line interfaces
│   │   ├── main.py                # Main entry point
│   │   ├── analyze.py             # Sector analysis CLI
│   │   ├── visualize.py           # Visualization CLI
│   │   └── extract.py             # Bloomberg extraction CLI
│   ├── core/              # Core functionality
│   │   ├── data_loader.py          # Data loading functions
│   │   ├── return_calculator.py    # Return calculation functions
│   │   ├── ranking_system.py       # Ranking functions
│   │   ├── rank_delta_calculator.py # Rank change functions
│   │   └── output_generator.py     # Output generation functions
│   ├── data_extraction/   # Data extraction modules
│   │   └── bloomberg_data_extractor.py # Bloomberg API integration
│   └── visualization/     # Visualization modules
│       └── visualize.py           # Visualization functions
├── scripts/               # Convenience scripts for users
│   ├── run_ranking.py              # Run the ranking system
│   ├── analyze_sectors.py          # Run sector analysis
│   ├── visualize_results.py        # Generate visualizations
│   └── extract_bloomberg.py        # Extract Bloomberg data
├── tests/                 # Test scripts
│   ├── test_ranking_system.py    # Tests for core ranking functionality
│   └── test_sector_analysis.py   # Tests for sector analysis
├── install.sh             # Installation script for macOS/Linux
├── install.bat            # Installation script for Windows
├── README.md              # This file
├── setup.py               # Package installation configuration
├── pyproject.toml         # Modern Python packaging configuration
└── requirements.txt       # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Bloomberg Terminal access (for data extraction in office)
- Git (for deployment from GitHub)

### Quick Installation (5 minutes)

#### Windows Users
```bash
# 1. Clone the repository
git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git

# 2. Run the one-step installation script
cd Renaissance_Stock_Ranking
install.bat

# 3. Verify installation
renaissance-rank --test-mode
```

#### macOS/Linux Users
```bash
# 1. Clone the repository
git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git

# 2. Run the one-step installation script
cd Renaissance_Stock_Ranking
./install.sh

# 3. Verify installation
renaissance-rank --test-mode
```

### Manual Installation
1. Clone this repository or download and extract the project ZIP file
2. Create a virtual environment:
   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Usage Guide

### For Investment Analysts
The system provides multiple ways to access its functionality, depending on your technical comfort level:

#### 1. Using Convenience Scripts (Recommended for Most Users)
These easy-to-use scripts require minimal technical knowledge:

```bash
# Run the main ranking process
python scripts/run_ranking.py

# Generate visualizations from the rankings
python scripts/visualize_results.py

# Perform sector analysis
python scripts/analyze_sectors.py

# Extract data from Bloomberg (when in office)
python scripts/extract_bloomberg.py
```

#### 2. Using Command-Line Tools (After Installation)
If you've installed the package, you can use these commands from anywhere:

```bash
# Run the ranking system
renaissance-rank

# Generate visualizations
renaissance-visualize

# Run sector analysis
renaissance-analyze

# Extract Bloomberg data
renaissance-extract
```

#### 3. Using as a Python Package (For Developers)
For custom analysis or integration with other systems:

```python
# Example: Using the package for custom analysis
from renaissance.core.data_loader import load_and_prepare_all_data
from renaissance.core.return_calculator import calculate_yearly_returns
from renaissance.core.ranking_system import rank_stocks_by_return
from renaissance.analysis.sector_analysis import analyze_sectors_by_performance

# Load data
nifty500_df, prices_df = load_and_prepare_all_data('data/nifty500_list.csv', 'data/historical_prices.csv')

# Calculate returns
returns_df = calculate_yearly_returns(prices_df)

# Rank stocks
ranked_df = rank_stocks_by_return(returns_df)

# Perform sector analysis
sector_report = analyze_sectors_by_performance(ranked_df, nifty500_df)

# Custom output - e.g., filter for specific sectors
tech_stocks = ranked_df[ranked_df['Sector'] == 'Information Technology']
print(f"Top 5 Technology Stocks:\n{tech_stocks.head(5)}")
```

### Data Workflow
This system follows a specific workflow due to restricted Bloomberg Terminal access:

1. **In-Office Data Extraction (Bloomberg Terminal Access Required)**:
   - Use Bloomberg Terminal to extract the NIFTY 500 constituent list with ISINs
   - Extract historical monthly closing prices for all NIFTY 500 stocks
   - Save data to structured CSV files
   - See [Data Extraction Guide](docs/data_extraction_guide.md) for detailed instructions
   - Or use the automated Bloomberg extractor: `python scripts/extract_bloomberg.py`

2. **Data Processing (Can be Done Anywhere)**:
   - Place the extracted data files in the `data/` directory:
     - `nifty500_list.csv`: List of NIFTY 500 constituents with ISINs
     - `historical_prices.csv`: Historical monthly closing prices
   - Run the Python system to process the data

### Advanced Usage with Custom Paths
```bash
python scripts/run_ranking.py --nifty500-file data/custom_nifty500_list.csv --price-file data/custom_prices.csv --output-dir custom_output --generate-historical
```

Command-line arguments:
- `--nifty500-file`: Path to NIFTY 500 constituent list (default: `data/nifty500_list.csv`)
- `--price-file`: Path to historical prices file (default: `data/historical_prices.csv`)
- `--output-dir`: Directory for output files (default: `output/`)
- `--generate-historical`: Generate historical rankings output (optional)

### Testing

Run all tests:
```bash
python -m unittest discover tests
```

Run a specific test:
```bash
python -m unittest tests.test_ranking_system
```

## Input Data Requirements

The system processes two primary data files:

1. **NIFTY 500 constituent list** (`nifty500_list.csv`): A list of all stocks in the NIFTY 500 index, with their ISINs as the primary identifier.
2. **Historical monthly closing prices** (`historical_prices.csv`): Month-end closing prices for all NIFTY 500 stocks.

These files can be created either:
- Manually by extracting data from the Bloomberg Terminal as described in the [Data Extraction Guide](docs/data_extraction_guide.md)
- Automatically using the Bloomberg API integration (see the [Bloomberg API Guide](docs/bloomberg_api_guide.md))

### Sample Data Format

#### nifty500_list.csv
```
ISIN,Name,Ticker,Sector
INE040A01034,HDFC Bank Ltd,HDFCB,Financials
INE009A01021,Infosys Ltd,INFO,Information Technology
INE030A01027,Reliance Industries Ltd,RIL,Energy
...
```

#### historical_prices.csv
```
ISIN,Date,Price
INE040A01034,2023-01-31,1450.75
INE040A01034,2023-02-28,1487.25
INE009A01021,2023-01-31,1486.70
...
```

## Output Files
- **Latest Rankings (`NIFTY500_Rankings_YYYYMMDD.csv`)**: Current month rankings
- **Rank Delta (`NIFTY500_RankDelta_YYYYMMDD.csv`)**: Rank changes from previous month
- **Summary Statistics (`NIFTY500_Ranking_Summary_YYYYMMDD_HHMMSS.txt`)**: Key statistics
- **Historical Rankings (Optional)**: All historical monthly rankings

## Troubleshooting Guide

### Common Issues and Solutions

#### Installation Problems
- **Error**: `pip install` fails with permission errors
  - **Solution**: Use `pip install --user` or create a virtual environment

- **Error**: Package not found after installation
  - **Solution**: Ensure you've activated the virtual environment or installed with `-e` flag

#### File Issues
- **Error**: "File not found" when running the system
  - **Solution**: Ensure data files are in the correct location (`data/` directory)
  - **Check**: Run `ls -la data/` to verify file existence and permissions

- **Error**: "Missing columns in CSV file"
  - **Solution**: Verify your CSV files have the required columns (ISIN, Date, Price for historical_prices.csv)
  - **Check**: Run `head -n 5 data/historical_prices.csv` to see the file structure

#### Date Format Issues
- **Error**: "Cannot parse date" or similar errors
  - **Solution**: Ensure dates are in YYYY-MM-DD format in your CSV files
  - **Check**: Run `grep -v '^\d\d\d\d-\d\d-\d\d' data/historical_prices.csv` to find non-conforming dates

#### Rank Calculation Issues
- **Error**: Empty or partial results in rankings
  - **Solution**: Ensure price data spans at least 13 months to calculate yearly returns
  - **Check**: Run `python -c "import pandas as pd; print(pd.read_csv('data/historical_prices.csv')['Date'].unique())"` to check date coverage

#### Import Errors
- **Error**: "Module not found" or import errors
  - **Solution**: Make sure you've installed the package with `pip install -e .`
  - **Check**: Run `pip list | grep renaissance` to verify the package is installed

For more detailed troubleshooting guide, see [User Guide](docs/user_guide.md).

## Complete Workflow with Sector Analysis

The complete workflow incorporating all features is:

1. **Extract data** (monthly or as needed):
   ```bash
   python scripts/extract_bloomberg.py
   ```
   This extracts NIFTY 500 constituents with sectors, historical prices, and financial metrics.

2. **Run the core ranking system**:
   ```bash
   python scripts/run_ranking.py
   ```
   This generates the stock rankings based on yearly returns.

3. **Generate ranking visualizations**:
   ```bash
   python scripts/visualize_results.py
   ```
   This creates visual charts of the ranking results.

4. **Perform sector analysis**:
   ```bash
   python scripts/analyze_sectors.py
   ```
   This analyzes performance by sector and generates sector-based reports.

5. **Review all results for investment decisions**:
   - Individual stock rankings (`output/NIFTY500_Rankings_*.csv`)
   - Rank changes month-over-month (`output/NIFTY500_RankDelta_*.csv`)
   - Visual charts (`output/visualizations/`)
   - Sector analysis reports (`output/sector_analysis/`)
   - The consolidated sector analysis report (`output/sector_analysis/sector_analysis_report.txt`)

## Portfolio Construction Example

Here's a step-by-step approach to using the system's outputs for portfolio construction:

1. **Identify Top-Performing Sectors**:
   ```python
   # Python code example for sector analysis
   import pandas as pd
   
   # Load the sector analysis results
   sector_performance = pd.read_csv('output/sector_analysis/sector_performance.csv')
   
   # Identify top 3 sectors
   top_sectors = sector_performance.sort_values('Avg_Return', ascending=False).head(3)
   print(f"Top 3 sectors to focus on:\n{top_sectors[['Sector', 'Avg_Return']]}")
   ```

2. **Select Top-Ranked Stocks Within These Sectors**:
   ```python
   # Load latest rankings
   rankings = pd.read_csv('output/NIFTY500_Rankings_20230331.csv')
   
   # Get top 5 stocks from each top sector
   portfolio_candidates = []
   for sector in top_sectors['Sector']:
       sector_stocks = rankings[rankings['Sector'] == sector].head(5)
       portfolio_candidates.append(sector_stocks)
   
   portfolio_df = pd.concat(portfolio_candidates)
   print(f"Portfolio candidates:\n{portfolio_df[['ISIN', 'Name', 'Sector', 'Yearly_Return', 'Rank']]}")
   ```

3. **Consider Diversification Using Sector Concentration Data**:
   ```python
   # Check concentration in the current portfolio
   sector_counts = portfolio_df['Sector'].value_counts()
   print(f"Current sector allocation:\n{sector_counts}")
   
   # Adjust if needed to ensure proper diversification
   # Example: If too concentrated in one sector, add stocks from other sectors
   ```

4. **Apply Financial Metrics for Final Selection**:
   ```python
   # Load financial metrics
   metrics = pd.read_csv('data/financial_metrics.csv')
   
   # Merge with our candidates
   portfolio_with_metrics = portfolio_df.merge(metrics, on='ISIN')
   
   # Example: Select stocks with PE below sector median and ROE above sector median
   final_selection = []
   for sector in top_sectors['Sector']:
       sector_stocks = portfolio_with_metrics[portfolio_with_metrics['Sector'] == sector]
       if len(sector_stocks) > 0:
           median_pe = sector_stocks['PE_Ratio'].median()
           median_roe = sector_stocks['ROE'].median()
           selected = sector_stocks[(sector_stocks['PE_Ratio'] < median_pe) & 
                                  (sector_stocks['ROE'] > median_roe)]
           final_selection.append(selected)
   
   final_portfolio = pd.concat(final_selection)
   print(f"Final portfolio selection:\n{final_portfolio[['Name', 'Sector', 'Yearly_Return', 'PE_Ratio', 'ROE']]}")
   ```

For advanced usage and customization options, see the [Sector Analysis Guide](docs/README_sector_analysis.md).

## GitHub Deployment Instructions

If you need to deploy this project to your own GitHub repository:

1. Create a new repository on GitHub
2. Initialize the local repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
3. Add your GitHub repository as remote and push:
   ```bash
   git remote add origin https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
   git branch -M main
   git push -u origin main
   ```

## Version History
- **v1.0.0** (Mar 2023): Initial release with core ranking functionality
- **v1.1.0** (Jun 2023): Added visualization capabilities
- **v1.2.0** (Sep 2023): Added sector analysis
- **v2.0.0** (Mar 2024): Restructured as proper Python package with Bloomberg API integration

## Author
Renaissance Investment Managers

## License
Proprietary - For use at Renaissance Investment Managers only
