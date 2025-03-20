# Bloomberg API Integration Guide

This guide explains how to automate data extraction from Bloomberg using the Bloomberg API (BLPAPI) instead of manually exporting data. This approach saves time and reduces the potential for human error when collecting data for the Renaissance Stock Ranking System.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Getting Access to Bloomberg API](#getting-access-to-bloomberg-api)
3. [Installation and Setup](#installation-and-setup)
4. [Handling Authentication Securely](#handling-authentication-securely)
5. [Step-by-Step Guide to Using the API](#step-by-step-guide-to-using-the-api)
6. [Internal Implementation Details](#internal-implementation-details)
7. [Enhanced Reliability Features](#enhanced-reliability-features)
8. [Advanced Features](#advanced-features)
9. [Test Mode for Development](#test-mode-for-development)
10. [Performance Considerations](#performance-considerations)
11. [Troubleshooting Bloomberg API Connection](#troubleshooting-bloomberg-api-connection)
12. [Setting Up Scheduled Extraction](#setting-up-scheduled-extraction)
13. [Bloomberg API vs. Manual Extraction](#bloomberg-api-vs-manual-extraction)
14. [Bloomberg Fields Reference](#bloomberg-fields-reference)
15. [Advanced Topics](#advanced-topics)
16. [Need More Help?](#need-more-help)
17. [References](#references)

## Prerequisites

Before you can use the Bloomberg API integration, you need:

- **Bloomberg Terminal** installed with an active subscription
- **Bloomberg Desktop API (DAPI)** installed on the same machine
- **Python 3.8 or higher** installed on your system
- Network access to Bloomberg services (usually via your company network)

## Getting Access to Bloomberg API

### Step 1: Verify Your Bloomberg Terminal Access

1. Ensure you have a valid Bloomberg Terminal license
2. Log in to your Bloomberg Terminal with your credentials
3. Verify that your subscription includes API access (most professional subscriptions do)

### Step 2: Install the Bloomberg Desktop API

1. On your Bloomberg Terminal, type `WAPI <GO>`
2. Click on "API Software Download Center"
3. Download the appropriate Desktop API installer for your operating system
4. Follow the installation instructions in the Bloomberg installer
5. During installation, when prompted, select "typical" installation
6. Verify installation by checking for the "Bloomberg" service in your system services

### Step 3: Install the Bloomberg Python API

After installing the Bloomberg Desktop API, you need to install the Python API package:

```bash
# Option 1: Install directly from Bloomberg's servers (preferred)
pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi

# Option 2: If option 1 fails, download manually from the Terminal
# 1. Type WAPI <GO> in your Bloomberg Terminal
# 2. Navigate to "API Libraries and Documentation" > "Python API"
# 3. Download the appropriate package for your Python version
# 4. Install the downloaded package with pip
pip install C:\path\to\downloaded\blpapi-3.19.3.tar.gz
```

### Step 4: Verify Your Installation

Create a simple test script to verify that your Bloomberg API connection works:

```python
import blpapi
import time

# Set up session options
session_options = blpapi.SessionOptions()
session_options.setServerHost('localhost')
session_options.setServerPort(8194)  # Default Bloomberg API port

# Create and start a session
session = blpapi.Session(session_options)
if not session.start():
    print("Failed to start session. Is Bloomberg running?")
    exit(1)

print("Successfully connected to Bloomberg!")
time.sleep(2)  # Keep the session alive briefly
session.stop()
```

Save this as `test_bloomberg.py` and run it. If successful, you should see "Successfully connected to Bloomberg!"

## Handling Authentication Securely

### Bloomberg Terminal Authentication

The Bloomberg API uses your already authenticated Bloomberg Terminal session for access. This means:

1. **No API keys are needed** in your code – authentication is handled via your logged-in Terminal
2. **No passwords should be stored** in your scripts or configuration files
3. Your access is tied to your Bloomberg Terminal login credentials

### Important Security Considerations

1. **Never hardcode any Bloomberg credentials** in your scripts
2. **Always ensure your Bloomberg Terminal is properly secured** with password protection
3. **Log out of your Bloomberg Terminal** when not in use
4. Do not share scripts that might contain any credential information
5. Consider using environment variables if you need to customize connection parameters

### For Multi-User Environments

If multiple users need to access the Bloomberg API:

1. Consider using Bloomberg Server API (B-PIPE) instead of Desktop API
2. Set up proper access controls for shared scripts
3. Implement logging to track who is making API requests

## Step-by-Step Guide to Using the API with Our System

### Step 1: Ensure Prerequisites Are Met

1. Verify your Bloomberg Terminal is running and logged in
2. Make sure you've installed all required software (see Prerequisites section)
3. Confirm that Python and the `blpapi` package are installed
4. Ensure your terminal/command prompt has access to the Renaissance Stock Ranking System

### Step 2: Understand the Data Extraction Process

Our system extracts three types of data from Bloomberg:

1. **NIFTY 500 constituent list** with ISINs, company names, tickers, and sectors
2. **Historical monthly prices** for all constituents, adjusted for corporate actions
3. **Financial metrics** including P/E ratio, P/B ratio, ROE, etc. (optional)

### Step 3: Run the Bloomberg Extractor

#### Option A: Using the Command Line Interface

```bash
# Activate your virtual environment first
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Basic usage (extracts data for the last 15 years)
python scripts/extract_bloomberg.py

# Customize the date range
python scripts/extract_bloomberg.py --start-date 2018-01-01 --end-date 2023-12-31

# Specify a different output directory
python scripts/extract_bloomberg.py --output-dir custom_data_folder

# Run in test mode (no Bloomberg connection needed)
python scripts/extract_bloomberg.py --test-mode
```

#### Option B: Using the Python API in Your Own Scripts

```python
from renaissance.data_extraction.bloomberg_data_extractor import get_nifty500_constituents, get_historical_prices, get_additional_metrics
import datetime

# Get NIFTY 500 constituents
constituents_df = get_nifty500_constituents()

# Define date range
end_date = datetime.datetime.now().date()
start_date = end_date.replace(year=end_date.year - 5)  # Last 5 years

# Get historical prices
prices_df = get_historical_prices(constituents_df["ISIN"].tolist(), start_date, end_date)

# Get financial metrics (optional)
metrics_df = get_additional_metrics(constituents_df["ISIN"].tolist())

# Save data to files
constituents_df.to_csv("data/nifty500_list.csv", index=False)
prices_df.to_csv("data/historical_prices.csv", index=False)
metrics_df.to_csv("data/financial_metrics.csv", index=False)
```

### Step 4: Verify the Extracted Data

After running the extraction, check that the following files were created:

1. `data/nifty500_list.csv` - Should contain ~500 stocks with ISINs, names, tickers, and sectors
2. `data/historical_prices.csv` - Should contain monthly price data for all constituents
3. `data/financial_metrics.csv` - Should contain financial metrics for all constituents

```bash
# Quick check of the extracted files
head -n 5 data/nifty500_list.csv
head -n 5 data/historical_prices.csv
head -n 5 data/financial_metrics.csv

# Count the number of records
wc -l data/nifty500_list.csv
wc -l data/historical_prices.csv
```

### Step 5: Run the Stock Ranking System with the Extracted Data

Once you have verified the data, you can run the stock ranking system:

```bash
# Run the main ranking system using the extracted data
python scripts/run_ranking.py

# Generate visualizations
python scripts/visualize_results.py

# Analyze sectors (uses the sector information from Bloomberg)
python scripts/analyze_sectors.py
```

## Internal Implementation Details

The `scripts/extract_bloomberg.py` script is a convenient wrapper around the Renaissance Stock Ranking System's Bloomberg extraction functionality. Under the hood, it uses the following implementation:

```python
# Example of the core extraction functionality
def get_nifty500_constituents(test_mode=False):
    """
    Get the current NIFTY 500 constituents with sector information using Bloomberg API.
    
    Args:
        test_mode (bool): If True, returns sample test data without calling Bloomberg API
    
    Returns:
        pd.DataFrame: DataFrame with ISIN, Name, Ticker, and Sector columns
    """
    # Implementation details...
    session = blpapi.Session(SESSION_OPTIONS)
    # ... Bloomberg API connection logic ...
    
    request = refDataService.createRequest("ReferenceDataRequest")
    request.append("securities", "NIFTY 500 Index")
    request.append("fields", "INDX_MWEIGHT_HIST")
    request.append("fields", "GICS_SECTOR_NAME")  # Add sector classification
    
    # ... Request processing and data extraction ...
    
    # Create DataFrame with ISIN, Name, Ticker, and Sector
    df = pd.DataFrame(constituents)
    logger.info(f"Retrieved {len(df)} NIFTY 500 constituents")
    
    return df
```

## Enhanced Reliability Features

Our Bloomberg extraction module includes several features to improve reliability:

### Automatic Retries

The system automatically retries Bloomberg API requests up to 3 times if connection issues occur:

```python
max_attempts = 3
attempt = 0

while attempt < max_attempts:
    attempt += 1
    try:
        session = blpapi.Session(SESSION_OPTIONS)
        if not session.start():
            logger.error(f"Failed to start Bloomberg API session (attempt {attempt}/{max_attempts})")
            if attempt == max_attempts:
                raise Exception("Failed to start Bloomberg API session after multiple attempts")
            time.sleep(5)  # Wait before retrying
            continue
        
        # Rest of the connection logic...
        
    except Exception as e:
        logger.error(f"Error in attempt {attempt}/{max_attempts}: {str(e)}")
        if attempt == max_attempts:
            raise
        else:
            logger.info(f"Retrying in 5 seconds...")
            time.sleep(5)
```

### Timeout Handling

API requests have timeout mechanisms to prevent hanging indefinitely:

```python
timeout_seconds = 60
start_time = time.time()

while True:
    # Check for timeout
    if time.time() - start_time > timeout_seconds:
        raise Exception(f"Bloomberg API request timed out after {timeout_seconds} seconds")
    
    ev = session.nextEvent(500)  # 500ms timeout per event
    # Process events...
    
    if ev.eventType() == blpapi.Event.RESPONSE:
        break
```

### Batch Processing

Data is retrieved in batches to avoid overwhelming the Bloomberg API:

```python
# Process ISINs in batches of 50 to avoid overwhelming the API
batch_size = 50
for i in range(0, len(isins), batch_size):
    batch_isins = isins[i:i+batch_size]
    logger.info(f"Processing batch {i//batch_size + 1}/{(len(isins) + batch_size - 1)//batch_size}")
    
    # Process this batch...
```

### Error Recovery

If sector information or financial metrics cannot be retrieved, the system continues with core functionality:

```python
try:
    metrics_df = get_additional_metrics(nifty500_df["ISIN"].tolist(), test_mode=args.test_mode)
    if len(metrics_df.columns) > 1:  # If we have more than just ISIN column
        metrics_file = os.path.join(args.output_dir, "financial_metrics.csv")
        metrics_df.to_csv(metrics_file, index=False)
        logger.info(f"Saved additional financial metrics to {metrics_file}")
except Exception as e:
    logger.warning(f"Could not retrieve additional financial metrics: {str(e)}")
    logger.info("Continuing without financial metrics")
```

## Advanced Features

### Sector Information

The Bloomberg API integration automatically retrieves sector information using the GICS (Global Industry Classification Standard) sector classification. This allows you to:

1. Analyze performance by sector
2. Identify sector trends
3. Compare stocks within their respective sectors
4. Diversify your portfolio across sectors

The sector information is added directly to the `nifty500_list.csv` file as an additional column.

### Financial Metrics

In addition to price data, the system retrieves key financial metrics for each stock:

1. **Price-to-Earnings Ratio (PE_Ratio)**: Indicates how much investors are willing to pay for each rupee of earnings
2. **Price-to-Book Ratio (PB_Ratio)**: Compares a company's market value to its book value
3. **Return on Equity (ROE)**: Measures a company's profitability relative to shareholders' equity
4. **Debt-to-Asset Ratio (DebtToAsset)**: Indicates what proportion of a company's assets are financed by debt
5. **Dividend Yield (DividendYield)**: Annual dividend payments relative to share price

These metrics are saved to a separate file called `financial_metrics.csv` in your output directory.

### Using Financial Metrics in Analysis

You can use these financial metrics to enhance your stock analysis:

```python
import pandas as pd

# Load rankings and financial metrics
rankings = pd.read_csv('output/NIFTY500_Rankings_20240301.csv')
metrics = pd.read_csv('output/financial_metrics.csv')

# Merge the data
combined = pd.merge(rankings, metrics, on='ISIN')

# Example: Find high-return stocks with reasonable valuations
value_growth = combined[
    (combined['YearlyReturn'] > 20) &  # High return
    (combined['PE_Ratio'] < 25) &      # Reasonable PE ratio
    (combined['DebtToAsset'] < 0.5)    # Low debt
]

print("Top value-growth stocks:")
print(value_growth[['Name', 'YearlyReturn', 'PE_Ratio', 'ROE', 'DebtToAsset']].head(10))
```

## Test Mode for Development

For development or testing without Bloomberg access, use the built-in test mode:

```bash
python scripts/extract_bloomberg.py --test-mode
```

Test mode will:
- Generate realistic sample data for ~10 stocks
- Create appropriate test files in your output directory
- Allow you to test the rest of the system without Bloomberg access

Implementation details:

```python
if test_mode:
    logger.info("TEST MODE: Using sample NIFTY 500 data instead of Bloomberg API")
    sample_data = [
        {"ISIN": "INE009A01021", "Name": "Infosys Ltd", "Ticker": "INFO:IN", "Sector": "Information Technology"},
        {"ISIN": "INE062A01020", "Name": "Tata Consultancy Services Ltd", "Ticker": "TCS:IN", "Sector": "Information Technology"},
        # ... more sample data ...
    ]
    return pd.DataFrame(sample_data)
```

## Performance Considerations

### Connection Efficiency

The system optimizes Bloomberg API usage by:

1. Reusing session connections where possible
2. Requesting multiple data fields in a single request
3. Processing data in batches of appropriate size
4. Releasing Bloomberg resources promptly

### Data Volume Management

When working with the full NIFTY 500 index and many years of historical data, if you experience performance issues:

1. Consider reducing the date range (e.g., 5 years instead of 15)
2. Focus on a subset of stocks if you only need specific sectors
3. Increase batch timeout values if you're on a slower network connection

## Troubleshooting Bloomberg API Connection

### Common Issues and Solutions

#### 1. "Failed to start Bloomberg API session"

**Solution:**
- Ensure the Bloomberg Terminal is running and logged in
- Verify that the Bloomberg Desktop API is installed
- Check your network connection to the Bloomberg service

**Commands to verify:**
```bash
# On Windows
sc query "Bloomberg"

# On macOS/Linux
ps aux | grep -i bloomberg
```

#### 2. "No Bloomberg Service found"

**Solution:**
- Check that you're running on a machine with Bloomberg Terminal
- Bloomberg Terminal might need to be restarted
- Try logging out and back in to the Terminal

#### 3. Data Retrieval is Very Slow

**Solution:**
- Reduce the date range for historical data
- Process in smaller batches (adjust batch_size in the code)
- Check your network connection speed
- Run during off-peak hours

#### 4. Missing Sector Information

**Solution:**
- Some stocks may not have GICS sector classification in Bloomberg
- The system will mark these as "Unknown" sector
- You can manually update the sector information in the output file

#### 5. Authentication Issues

**Solution:**
- Make sure you're logged into your Bloomberg Terminal
- Check your Bloomberg Terminal permissions with your administrator
- Bloomberg API uses the same authentication as your Terminal session

## Setting Up Scheduled Extraction

For regular updates, you can set up the Bloomberg data extractor to run automatically:

### On Windows:
1. Create a batch file (e.g., `run_extractor.bat`) with the command:
   ```
   @echo off
   cd C:\path\to\Renaissance_Stock_Ranking
   call venv\Scripts\activate
   python scripts/extract_bloomberg.py
   ```

2. Use Windows Task Scheduler to run this batch file on your desired schedule.

### On macOS/Linux:
1. Create a shell script (e.g., `run_extractor.sh`) with the command:
   ```bash
   #!/bin/bash
   cd /path/to/Renaissance_Stock_Ranking
   source venv/bin/activate
   python scripts/extract_bloomberg.py
   ```

2. Make the script executable:
   ```bash
   chmod +x run_extractor.sh
   ```

3. Add a crontab entry to run the script on your desired schedule:
   ```
   0 18 * * 5 /path/to/run_extractor.sh
   ```
   (This example runs the script at 6 PM every Friday)

## Bloomberg API vs. Manual Extraction

| Aspect | Bloomberg API | Manual Extraction |
|--------|--------------|-------------------|
| **Speed** | Much faster, especially for large datasets | Slow and labor-intensive |
| **Accuracy** | Reduces human error | Prone to copy-paste errors |
| **Automation** | Can be scheduled to run automatically | Requires manual intervention |
| **Learning Curve** | Requires programming knowledge | Simple but tedious |
| **Flexibility** | Can customize fields and calculation | Limited to Excel functions |

## Bloomberg Fields Reference

The extraction functionality uses these Bloomberg fields:

- `INDX_MWEIGHT_HIST`: Index members weight history
- `PX_LAST`: Last price
- `ID_ISIN`: ISIN code
- `NAME`: Company name
- `TICKER`: Bloomberg ticker
- `GICS_SECTOR_NAME`: Sector classification
- `PE_RATIO`: Price-to-earnings ratio
- `PX_TO_BOOK_RATIO`: Price-to-book ratio
- `RETURN_COM_EQY`: Return on equity
- `TOT_DEBT_TO_TOT_ASSET`: Debt-to-asset ratio
- `EQY_DVD_YLD_IND`: Dividend yield

For other useful fields, consult the Bloomberg API documentation or use the FLDS <GO> command in the Bloomberg Terminal.

## Advanced Topics

### Using the Bloomberg Server API

For enterprise deployments, you might want to use the Bloomberg Server API (B-PIPE) instead of the Desktop API (DAPI). This allows multiple users to access Bloomberg data through a centralized server.

### Working with Multiple Indices

To extract data for multiple indices (not just NIFTY 500), you can modify the extraction function to accept an index parameter.

### Adding More Data Fields

You can extract additional data fields by modifying the module to include more Bloomberg fields in the API requests.

## Need More Help?

If you encounter any issues with the Bloomberg API integration:

1. Check the application logs in `bloomberg_extractor.log`
2. Contact your Bloomberg Terminal administrator
3. Reach out to Bloomberg API support via your Terminal (HELP 4 <GO>)
4. For Renaissance Stock Ranking System specific issues, refer to our documentation

## References

- [Bloomberg API Developer's Guide](https://data.bloomberglp.com/professional/sites/10/2017/03/BLPAPI-Core-Developer-Guide.pdf)
- [Python API Documentation](https://bloomberg.github.io/blpapi-docs/python/3.13/)
- Bloomberg Terminal Help: type HELP <GO> on your Bloomberg Terminal