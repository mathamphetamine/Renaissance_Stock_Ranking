# Renaissance Stock Ranking System - User Guide

This guide provides detailed instructions on how to use the Automated Stock Ranking System for Renaissance Investment Managers.

## Table of Contents
1. [System Overview](#system-overview)
2. [Installation and Setup](#installation-and-setup)
3. [Data Requirements](#data-requirements)
4. [Using the System](#using-the-system)
5. [Interpreting Results](#interpreting-results)
6. [Extending the System](#extending-the-system)
7. [Troubleshooting](#troubleshooting)

## System Overview

The Automated Stock Ranking System for Renaissance Investment Managers is designed to:

1. Load NIFTY 500 constituent data and historical price information from CSV files
2. Calculate yearly returns on a monthly rolling basis (12-month returns ending each month)
3. Rank stocks based on these returns
4. Track month-over-month rank changes
5. Generate easy-to-interpret output files with rankings and analysis
6. Analyze sector performance and provide investment insights
7. Create visualizations for better data understanding

This replaces the previous manual process of collecting and analyzing this data in Excel spreadsheets.

### System Workflow Diagram

```
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│ Bloomberg     │         │ CSV Files     │         │ Python System │
│ Terminal      │────────>│ - NIFTY 500   │────────>│ (This Tool)   │
│ (Data Source) │         │ - Prices      │         │               │
└───────────────┘         └───────────────┘         └───────┬───────┘
                                                            │
                                                            ▼
                          ┌───────────────┐         ┌───────────────┐
                          │ Analysis &    │<────────│ Data          │
                          │ Visualization │         │ Processing    │
                          │ (Optional)    │         │ - Returns     │
                          └───────────────┘         │ - Rankings    │
                                                    │ - Rank Changes│
                                                    └───────┬───────┘
                                                            │
                                                            ▼
                                                    ┌───────────────┐
                                                    │ Output Files  │
                                                    │ - Rankings    │
                                                    │ - Rank Delta  │
                                                    │ - Summary     │
                                                    └───────────────┘
```

### For Non-Technical Users

The system works like an assembly line:
1. We get raw data from Bloomberg (like getting ingredients for a recipe)
2. We save this data in simple CSV files (like putting ingredients in containers)
3. The Python system processes this data (like cooking the ingredients)
4. The system produces output files with the results (like serving the finished dish)

## Installation and Setup

### System Requirements
- Python 3.8 or higher
- Bloomberg Terminal access (for data extraction only)
- Bloomberg Desktop API (for automated data extraction)
- Operating System: Windows, macOS, or Linux
- RAM: 4GB minimum (8GB recommended for large datasets)
- Disk Space: 1GB for installation and data

### Installation Steps

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
   cd Renaissance_Stock_Ranking
   ```

2. **Use the installation scripts (Recommended)**
   ```bash
   # On Windows
   install.bat
   
   # On macOS/Linux
   ./install.sh
   ```
   
   These scripts will:
   - Create a virtual environment
   - Install all required dependencies
   - Install the package in development mode
   - Make scripts executable

3. **Verify installation**
   ```bash
   # Activate your virtual environment first
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Test the installation
   renaissance-rank --test-mode
   ```
   
   This should run successfully and indicate that the system is properly installed.

## Data Requirements

The system requires two primary CSV files and one optional file:

### 1. NIFTY 500 Constituent List (`nifty500_list.csv`)

**Required columns:**
- `ISIN`: The International Securities Identification Number (primary identifier)
- `Name`: The company name
- `Ticker`: The Bloomberg ticker (optional but recommended)
- `Sector`: The sector classification (optional, improves analysis)

**Example format:**
```
ISIN,Name,Ticker,Sector
INE009A01021,Infosys Ltd,INFO:IN,Information Technology
INE062A01020,Tata Consultancy Services Ltd,TCS:IN,Information Technology
INE040A01034,HDFC Bank Ltd,HDFCB:IN,Financials
```

### 2. Historical Prices (`historical_prices.csv`)

**Required columns:**
- `ISIN`: The International Securities Identification Number
- `Date`: The date of the price (YYYY-MM-DD format)
- `Price`: The adjusted closing price

**Example format:**
```
ISIN,Date,Price
INE009A01021,2022-01-31,1680.75
INE009A01021,2022-02-28,1722.30
INE062A01020,2022-01-31,3698.15
```

### 3. Financial Metrics (`financial_metrics.csv`) - Optional

**Columns:**
- `ISIN`: The International Securities Identification Number
- `PE_Ratio`: Price-to-earnings ratio
- `PB_Ratio`: Price-to-book ratio
- `ROE`: Return on equity
- `DebtToAsset`: Debt-to-asset ratio
- `DividendYield`: Dividend yield

**Example format:**
```
ISIN,PE_Ratio,PB_Ratio,ROE,DebtToAsset,DividendYield
INE009A01021,28.5,3.2,25.4,0.12,1.5
INE062A01020,30.2,12.5,42.8,0.05,1.2
```

**Important notes:**
- Prices should be month-end closing prices
- Prices must be adjusted for corporate actions (splits, dividends, etc.)
- At least 13 months of data is required to calculate 12-month returns
- Dates should be in YYYY-MM-DD format
- All prices should be in the same currency (preferably INR)

## Using the System

### Data Collection Options

#### Option 1: Automated Bloomberg API Extraction (Recommended)

If you have Bloomberg Terminal access with the Bloomberg Desktop API installed:

```bash
# Extract all necessary data using the Bloomberg API
python scripts/extract_bloomberg.py
```

This will:
- Extract the NIFTY 500 constituent list with sector information
- Retrieve historical prices with corporate action adjustments
- Collect financial metrics for deeper analysis
- Save all files in the required format

For detailed setup instructions, see the [Bloomberg API Guide](bloomberg_api_guide.md).

#### Option 2: Manual Bloomberg Data Extraction

Follow the [Data Extraction Guide](data_extraction_guide.md) to manually:
1. Extract the NIFTY 500 constituent list from Bloomberg
2. Extract historical monthly prices
3. Optionally extract financial metrics
4. Save them as CSV files in the data directory

#### Option 3: Use Sample Data (For Testing)

```bash
# Copy sample data to the data directory
cp data/sample/* data/
```

### Running the Core Ranking System

```bash
# Using the script interface
python scripts/run_ranking.py

# Or using the CLI tool
renaissance-rank
```

Command-line options:
```bash
# Custom file paths
python scripts/run_ranking.py --nifty500-file path/to/nifty500_list.csv --price-file path/to/historical_prices.csv

# Custom output directory
python scripts/run_ranking.py --output-dir path/to/output_directory

# Generate historical rankings file
python scripts/run_ranking.py --generate-historical
```

### Generating Visualizations

```bash
# Using the script interface
python scripts/visualize_results.py

# Or using the CLI tool
renaissance-visualize
```

This creates multiple visualizations in the `output/visualizations/` directory:
- Return distribution charts
- Top and bottom performers
- Rank change distribution
- Return vs. rank scatter plots
- And more

An HTML index file is also created for easy navigation of all visualizations.

### Performing Sector Analysis

```bash
# Using the script interface
python scripts/analyze_sectors.py

# Or using the CLI tool
renaissance-analyze
```

This generates sector-level analysis in the `output/sector_analysis/` directory:
- Sector performance rankings
- Top stocks by sector
- Sector concentration metrics
- Investment recommendations

## Interpreting Results

The system generates the following output files:

### 1. Latest Rankings File (`NIFTY500_Rankings_YYYYMMDD.csv`)

This file contains the latest month's rankings, including:
- ISIN
- Company Name
- Date
- Yearly Return
- Rank

The stock with Rank 1 has the highest yearly return.

### 2. Rank Delta File (`NIFTY500_RankDelta_YYYYMMDD.csv`)

This file shows how each stock's rank has changed from the previous month:
- ISIN
- Company Name
- Date
- Yearly Return
- Current Rank
- Previous Rank
- Rank Delta

A negative rank delta indicates improvement (e.g., moving from Rank 10 to Rank 5 gives a delta of -5).
A positive rank delta indicates decline.

### 3. Summary Statistics File (`NIFTY500_Ranking_Summary_YYYYMMDD_HHMMSS.txt`)

This file provides overall statistics about the analysis:
- Data coverage information (stocks, time period)
- Return statistics (average, min, max)
- Ranking statistics (volatility, average movement)

### 4. Visualization Files

The system generates various charts and graphs in the `output/visualizations/` directory:
- Return distribution charts showing the spread of returns
- Top and bottom performers charts highlighting the best and worst stocks
- Rank change distribution showing how ranks have shifted
- Sector performance visualizations if sector data is available
- HTML index file for easy navigation

### 5. Sector Analysis Files

If sector information is available:
- `sector_performance.csv`: Overall sector performance metrics
- `top_stocks_by_sector.csv`: Best-performing stocks in each sector
- `sector_concentration.csv`: Metrics on sector weighting and concentration

## Extending the System

The system is designed to be modular and extensible. Here are some ways you can extend it:

### Adding New Metrics

To add new metrics (e.g., risk-adjusted returns):

1. Create a new module in the `renaissance/analysis/` directory
2. Implement the calculation logic
3. Update the CLI modules to include the new functionality
4. Update output generation to include the new metrics

### Customizing the Ranking Algorithm

The current system ranks stocks based solely on yearly returns. To modify the ranking criteria:

1. Edit `renaissance/core/ranking_system.py`
2. Modify the `rank_stocks_by_return` function to use different or multiple criteria

### Supporting Different Data Sources

To support data from sources other than Bloomberg:

1. Create a new loader in `renaissance/data_extraction/` directory
2. Implement the logic to convert the data to the format expected by the system
3. Update the CLI modules to use the new loader

## Troubleshooting

### Common Issues and Solutions

#### File Not Found Errors
```
FileNotFoundError: NIFTY 500 ISIN list file not found: data/nifty500_list.csv
```

**Solution**: Ensure the data files are in the correct location. If using custom paths, verify they are correct.

#### Missing Columns
```
Missing required columns in NIFTY 500 ISIN list: ['ISIN']
```

**Solution**: Ensure your CSV files have all the required columns. Check the column names for typos.

#### Date Format Issues
```
ValueError: time data '01/31/2022' does not match format '%Y-%m-%d'
```

**Solution**: Ensure dates in the CSV file are in YYYY-MM-DD format.

#### Insufficient Data
```
Warning: Calculated returns span only 6 months, which is less than a year
```

**Solution**: Ensure you have at least 13 months of price data to calculate 12-month returns.

#### Bloomberg API Connection Issues
```
Failed to start Bloomberg API session
```

**Solution**:
- Ensure the Bloomberg Terminal is running and logged in
- Verify that the Bloomberg Desktop API is installed
- Check your network connection to the Bloomberg service

### Log Files

The system generates log files that contain detailed information about the execution:
- `ranking_system.log`: Main ranking system log
- `bloomberg_extractor.log`: Bloomberg API extraction log

Check these files for error messages and warnings.

### Getting Help

If you encounter issues that are not covered in this guide:

1. Check the logs for detailed error messages
2. Verify that your data files match the required format
3. Run the tests to verify the installation
4. See the specialized guides:
   - [Bloomberg API Guide](bloomberg_api_guide.md)
   - [Data Extraction Guide](data_extraction_guide.md)
   - [Sector Analysis Guide](README_sector_analysis.md)

---

## Quick Reference

### Command-Line Tools

| Tool | Description | Example |
|------|-------------|---------|
| `renaissance-rank` | Run the ranking system | `renaissance-rank --output-dir output` |
| `renaissance-visualize` | Generate visualizations | `renaissance-visualize` |
| `renaissance-analyze` | Analyze sectors | `renaissance-analyze` |
| `renaissance-extract` | Extract Bloomberg data | `renaissance-extract --test-mode` |

### Script Interfaces

| Script | Description | Example |
|--------|-------------|---------|
| `scripts/run_ranking.py` | Run the ranking system | `python scripts/run_ranking.py` |
| `scripts/visualize_results.py` | Generate visualizations | `python scripts/visualize_results.py` |
| `scripts/analyze_sectors.py` | Analyze sectors | `python scripts/analyze_sectors.py` |
| `scripts/extract_bloomberg.py` | Extract Bloomberg data | `python scripts/extract_bloomberg.py` |

### Required Data Columns

| File | Required Columns |
|------|------------------|
| NIFTY 500 List | ISIN, Name (Sector recommended) |
| Historical Prices | ISIN, Date, Price |
| Financial Metrics | ISIN, plus any metrics |

### Output Files

| File | Content |
|------|---------|
| `NIFTY500_Rankings_YYYYMMDD.csv` | Latest month's rankings |
| `NIFTY500_RankDelta_YYYYMMDD.csv` | Rank changes from previous month |
| `NIFTY500_Ranking_Summary_YYYYMMDD_HHMMSS.txt` | Summary statistics |
| Visualization files | Charts and graphs in `output/visualizations/` |
| Sector analysis files | Sector insights in `output/sector_analysis/` | 