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
- Operating System: Windows, macOS, or Linux
- RAM: 4GB minimum (8GB recommended for large datasets)
- Disk Space: 1GB for installation and data

### Installation Steps

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/YourUsername/Renaissance_Stock_Ranking.git
   cd Renaissance_Stock_Ranking
   ```

2. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -m unittest discover tests
   ```
   All tests should pass, indicating that the system is properly installed.

## Data Requirements

The system requires two primary CSV files:

### 1. NIFTY 500 Constituent List (`nifty500_list.csv`)

**Required columns:**
- `ISIN`: The International Securities Identification Number (primary identifier)
- `Name`: The company name
- `Ticker`: The Bloomberg ticker (optional but recommended)

**Example format:**
```
ISIN,Name,Ticker
INE009A01021,Infosys Ltd,INFO:IN
INE062A01020,Tata Consultancy Services Ltd,TCS:IN
INE040A01034,HDFC Bank Ltd,HDFCB:IN
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

**Important notes:**
- Prices should be month-end closing prices
- Prices must be adjusted for corporate actions (splits, dividends, etc.)
- At least 13 months of data is required to calculate 12-month returns
- Dates should be in YYYY-MM-DD format
- All prices should be in the same currency (preferably INR)

## Using the System

### Basic Usage

1. **Extract data from Bloomberg Terminal**
   - See the [Data Extraction Guide](data_extraction_guide.md) for detailed instructions
   - Save the extracted data as CSV files in the required format

2. **Place data files in the correct location**
   - Put `nifty500_list.csv` in the `data/` directory
   - Put `historical_prices.csv` in the `data/` directory

3. **Run the system**
   ```bash
   python src/main.py
   ```

4. **Check the output**
   - Output files will be created in the `output/` directory
   - See [Interpreting Results](#interpreting-results) for details

### Advanced Usage

**Custom file paths:**
```bash
python src/main.py --nifty500-file path/to/nifty500_list.csv --price-file path/to/historical_prices.csv
```

**Custom output directory:**
```bash
python src/main.py --output-dir path/to/output_directory
```

**Generate historical rankings file:**
```bash
python src/main.py --generate-historical
```

**Running with all options:**
```bash
python src/main.py --nifty500-file data/custom_nifty500_list.csv --price-file data/custom_prices.csv --output-dir custom_output --generate-historical
```

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

### 4. Historical Rankings File (Optional)

If generated using the `--generate-historical` flag, this file contains all historical rankings for all stocks over the entire time period.

## Extending the System

The system is designed to be modular and extensible. Here are some ways you can extend it:

### Adding New Metrics

To add new metrics (e.g., risk-adjusted returns):

1. Create a new module in the `src/` directory
2. Implement the calculation logic
3. Update `main.py` to include the new module
4. Update output generation to include the new metrics

### Customizing the Ranking Algorithm

The current system ranks stocks based solely on yearly returns. To modify the ranking criteria:

1. Edit `src/ranking_system.py`
2. Modify the `rank_stocks_by_return` function to use different or multiple criteria

### Supporting Different Data Sources

To support data from sources other than Bloomberg:

1. Create a new loader in `src/data_loader.py` or a new file
2. Implement the logic to convert the data to the format expected by the system
3. Update `main.py` to use the new loader

## Troubleshooting

### Common Issues and Solutions

#### File Not Found Errors
```
FileNotFoundError: NIFTY 500 ISIN list file not found: ../data/nifty500_list.csv
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

#### No Returns Calculated
```
Error calculating yearly returns: Cannot calculate return - no prior price found
```

**Solution**: Verify that your price data has sufficient history (at least 12 months) for each stock.

### Log Files

The system generates a log file (`ranking_system.log`) that contains detailed information about the execution. Check this file for error messages and warnings.

### Getting Help

If you encounter issues that are not covered in this guide:

1. Check the logs for detailed error messages
2. Verify that your data files match the required format
3. Run the tests to verify the installation
4. Contact the system developer for assistance

---

## Quick Reference

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--nifty500-file` | Path to NIFTY 500 constituent list | `../data/nifty500_list.csv` |
| `--price-file` | Path to historical prices file | `../data/historical_prices.csv` |
| `--output-dir` | Directory for output files | `../output/` |
| `--generate-historical` | Generate historical rankings output | Not set (False) |

### Required Data Columns

| File | Required Columns |
|------|------------------|
| NIFTY 500 List | ISIN, Name |
| Historical Prices | ISIN, Date, Price |

### Output Files

| File | Content |
|------|---------|
| `NIFTY500_Rankings_YYYYMMDD.csv` | Latest month's rankings |
| `NIFTY500_RankDelta_YYYYMMDD.csv` | Rank changes from previous month |
| `NIFTY500_Ranking_Summary_YYYYMMDD_HHMMSS.txt` | Summary statistics |
| `NIFTY500_Historical_Rankings_YYYYMMDD_HHMMSS.csv` | (Optional) All historical rankings | 