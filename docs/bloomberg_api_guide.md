# Bloomberg API Integration Guide

This guide explains how to automate data extraction from Bloomberg using the Bloomberg API (BLPAPI) instead of manually exporting data. This approach can save time and reduce the potential for human error when collecting data for the Renaissance Stock Ranking System.

## Prerequisites

- Bloomberg Terminal installed with an active subscription
- Bloomberg Desktop API (DAPI) installed
- Python 3.8 or higher
- `blpapi` Python package (Bloomberg's official Python API)

## Installation

1. **Install the Bloomberg Python API**

   ```bash
   pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
   ```

   If you have issues with the installation, you can download the package directly from the Bloomberg Terminal by typing `WAPI <GO>` and following the links to the Python API.

2. **Verify your installation**

   ```python
   import blpapi
   print(blpapi.__version__)  # Should print the installed version
   ```

## Usage Example

Below is a complete example script that extracts both the NIFTY 500 constituent list and the historical price data using the Bloomberg API.

```python
#!/usr/bin/env python
"""
Bloomberg Data Extractor

This script automates the extraction of NIFTY 500 constituent data and
historical prices using the Bloomberg API.

Usage:
    python bloomberg_data_extractor.py --output-dir data
"""

import blpapi
import pandas as pd
import datetime
import argparse
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bloomberg API session parameters
SESSION_OPTIONS = blpapi.SessionOptions()
SESSION_OPTIONS.setServerHost('localhost')
SESSION_OPTIONS.setServerPort(8194)  # Default Bloomberg API port

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Bloomberg Data Extractor')
    
    parser.add_argument('--output-dir', type=str, default='data',
                        help='Directory where CSV files will be saved')
    
    parser.add_argument('--start-date', type=str, default=None,
                        help='Start date for historical data (YYYY-MM-DD). Defaults to 15 years ago.')
    
    parser.add_argument('--end-date', type=str, default=None,
                        help='End date for historical data (YYYY-MM-DD). Defaults to today.')
    
    return parser.parse_args()

def get_nifty500_constituents():
    """
    Get the current NIFTY 500 constituents using Bloomberg API.
    
    Returns:
        pd.DataFrame: DataFrame with ISIN, Name, and Ticker columns
    """
    logger.info("Getting NIFTY 500 constituents from Bloomberg")
    
    session = blpapi.Session(SESSION_OPTIONS)
    if not session.start():
        raise Exception("Failed to start Bloomberg API session")
    
    if not session.openService("//blp/refdata"):
        session.stop()
        raise Exception("Failed to open //blp/refdata service")
    
    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("ReferenceDataRequest")
    
    request.append("securities", "NIFTY 500 Index")
    request.append("fields", "INDX_MWEIGHT_HIST")
    
    overrides = request.getElement("overrides")
    override1 = overrides.appendElement()
    override1.setElement("fieldId", "INDX_MWEIGHT_HIST_END_DT")
    override1.setElement("value", datetime.date.today().strftime("%Y%m%d"))
    
    logger.info("Sending request for NIFTY 500 constituents")
    session.sendRequest(request)
    
    constituents = []
    while True:
        ev = session.nextEvent(500)
        for msg in ev:
            if msg.messageType() == blpapi.Name("ReferenceDataResponse"):
                securityData = msg.getElement("securityData")
                fieldData = securityData.getElement("fieldData")
                
                if fieldData.hasElement("INDX_MWEIGHT_HIST"):
                    weightData = fieldData.getElement("INDX_MWEIGHT_HIST")
                    for i in range(weightData.numValues()):
                        constituent = weightData.getValue(i)
                        isin = constituent.getElementAsString("ID_ISIN")
                        name = constituent.getElementAsString("NAME")
                        ticker = constituent.getElementAsString("TICKER")
                        
                        constituents.append({
                            "ISIN": isin,
                            "Name": name,
                            "Ticker": ticker
                        })
        
        if ev.eventType() == blpapi.Event.RESPONSE:
            break
    
    session.stop()
    
    # Create DataFrame
    df = pd.DataFrame(constituents)
    logger.info(f"Retrieved {len(df)} NIFTY 500 constituents")
    
    return df

def get_historical_prices(isins, start_date, end_date):
    """
    Get historical monthly prices for a list of ISINs.
    
    Args:
        isins (list): List of ISINs to get prices for
        start_date (datetime): Start date for historical data
        end_date (datetime): End date for historical data
        
    Returns:
        pd.DataFrame: DataFrame with ISIN, Date, and Price columns
    """
    logger.info(f"Getting historical prices for {len(isins)} stocks")
    
    session = blpapi.Session(SESSION_OPTIONS)
    if not session.start():
        raise Exception("Failed to start Bloomberg API session")
    
    if not session.openService("//blp/refdata"):
        session.stop()
        raise Exception("Failed to open //blp/refdata service")
    
    refDataService = session.getService("//blp/refdata")
    
    all_prices = []
    
    # Process ISINs in batches of 50 to avoid overwhelming the API
    batch_size = 50
    for i in range(0, len(isins), batch_size):
        batch_isins = isins[i:i+batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}/{(len(isins) + batch_size - 1)//batch_size}")
        
        request = refDataService.createRequest("HistoricalDataRequest")
        
        # Add securities (convert ISINs to Bloomberg Equity identifiers)
        for isin in batch_isins:
            request.append("securities", f"{isin} Equity")
        
        # Add fields
        request.append("fields", "PX_LAST")
        
        # Set date range
        request.set("startDate", start_date.strftime("%Y%m%d"))
        request.set("endDate", end_date.strftime("%Y%m%d"))
        
        # Set periodicity to monthly
        request.set("periodicitySelection", "MONTHLY")
        
        # Request prices in INR
        overrides = request.getElement("overrides")
        override1 = overrides.appendElement()
        override1.setElement("fieldId", "CRNCY")
        override1.setElement("value", "INR")
        
        logger.info(f"Sending request for historical prices (batch {i//batch_size + 1})")
        session.sendRequest(request)
        
        batch_prices = []
        while True:
            ev = session.nextEvent(500)
            for msg in ev:
                if msg.messageType() == blpapi.Name("HistoricalDataResponse"):
                    securityData = msg.getElement("securityData")
                    security = securityData.getElementAsString("security")
                    
                    # Extract ISIN from security string (e.g., "INE009A01021 Equity")
                    isin = security.split(" ")[0]
                    
                    fieldData = securityData.getElement("fieldData")
                    for i in range(fieldData.numValues()):
                        point = fieldData.getValue(i)
                        date = point.getElementAsDatetime("date").strftime("%Y-%m-%d")
                        price = point.getElementAsFloat("PX_LAST")
                        
                        batch_prices.append({
                            "ISIN": isin,
                            "Date": date,
                            "Price": price
                        })
            
            if ev.eventType() == blpapi.Event.RESPONSE:
                break
        
        all_prices.extend(batch_prices)
    
    session.stop()
    
    # Create DataFrame
    df = pd.DataFrame(all_prices)
    
    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Sort by ISIN and Date
    df = df.sort_values(["ISIN", "Date"])
    
    logger.info(f"Retrieved {len(df)} historical price records")
    
    return df

def main():
    """Main function to extract data from Bloomberg."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Set default start and end dates if not provided
        end_date = datetime.datetime.now().date() if args.end_date is None else datetime.datetime.strptime(args.end_date, "%Y-%m-%d").date()
        start_date = end_date.replace(year=end_date.year - 15) if args.start_date is None else datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
        
        logger.info(f"Extracting data from Bloomberg")
        logger.info(f"Date range: {start_date} to {end_date}")
        logger.info(f"Output directory: {args.output_dir}")
        
        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Get NIFTY 500 constituents
        nifty500_df = get_nifty500_constituents()
        
        # Save constituents to CSV
        nifty500_file = os.path.join(args.output_dir, "nifty500_list.csv")
        nifty500_df.to_csv(nifty500_file, index=False)
        logger.info(f"Saved NIFTY 500 constituents to {nifty500_file}")
        
        # Get historical prices
        prices_df = get_historical_prices(nifty500_df["ISIN"].tolist(), start_date, end_date)
        
        # Save prices to CSV
        prices_file = os.path.join(args.output_dir, "historical_prices.csv")
        prices_df.to_csv(prices_file, index=False)
        logger.info(f"Saved historical prices to {prices_file}")
        
        logger.info("Data extraction completed successfully")
        
    except Exception as e:
        logger.error(f"Error extracting data: {str(e)}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
```

## Authentication

Bloomberg API authentication is handled through your Bloomberg Terminal installation. The API connects to the locally running Bloomberg Terminal service, which must be logged in with your credentials. Make sure:

1. Your Bloomberg Terminal is running and logged in
2. Your Bloomberg Terminal is on the same machine as your Python script, or
3. You've properly configured the Bloomberg Server API if accessing from a different machine

## Error Handling

Common Bloomberg API issues include:

1. **Connection errors**: Make sure the Bloomberg Terminal is running and that the correct host and port are specified.
2. **Authentication errors**: Ensure your Bloomberg Terminal is logged in with valid credentials.
3. **Rate limits**: Bloomberg may impose limits on the number of requests. If you're extracting data for many stocks, consider batching requests as shown in the example script.
4. **Missing data**: Some securities may not have data for the entire requested period. The script should handle these cases gracefully.

## Bloomberg API vs. Manual Extraction

| Aspect | Bloomberg API | Manual Extraction |
|--------|--------------|-------------------|
| **Speed** | Much faster, especially for large datasets | Slow and labor-intensive |
| **Accuracy** | Reduces human error | Prone to copy-paste errors |
| **Automation** | Can be scheduled to run automatically | Requires manual intervention |
| **Learning Curve** | Requires programming knowledge | Simple but tedious |
| **Flexibility** | Can customize fields and calculation | Limited to Excel functions |

## Setting Up a Scheduled Extraction

For regular updates, you can set up the Bloomberg data extractor to run automatically:

### On Windows:
1. Create a batch file (e.g., `run_extractor.bat`) with the command:
   ```
   @echo off
   cd C:\path\to\Renaissance_Stock_Ranking
   call venv\Scripts\activate
   python bloomberg_data_extractor.py
   ```

2. Use Windows Task Scheduler to run this batch file on your desired schedule.

### On macOS/Linux:
1. Create a shell script (e.g., `run_extractor.sh`) with the command:
   ```bash
   #!/bin/bash
   cd /path/to/Renaissance_Stock_Ranking
   source venv/bin/activate
   python bloomberg_data_extractor.py
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

## Bloomberg Fields Reference

The script above uses these Bloomberg fields:

- `INDX_MWEIGHT_HIST`: Index members weight history
- `PX_LAST`: Last price
- `ID_ISIN`: ISIN code
- `NAME`: Company name
- `TICKER`: Bloomberg ticker

For other useful fields, consult the Bloomberg API documentation or use the FLDS <GO> command in the Bloomberg Terminal.

## Advanced Topics

### Using the Bloomberg Server API

For enterprise deployments, you might want to use the Bloomberg Server API (SAPI) instead of the Desktop API (DAPI). This allows multiple users to access Bloomberg data through a centralized server.

### Working with Multiple Indices

To extract data for multiple indices (not just NIFTY 500), modify the `get_nifty500_constituents()` function to accept an index parameter:

```python
def get_index_constituents(index_name="NIFTY 500 Index"):
    # Same code, but use the index_name parameter instead of hardcoding
    request.append("securities", index_name)
    # ...
```

### Adding More Fields

You can extract additional data fields, such as:
- `PE_RATIO`: Price-to-earnings ratio
- `PX_TO_BOOK_RATIO`: Price-to-book ratio
- `RETURN_COM_EQY`: Return on equity
- `TOT_DEBT_TO_TOT_ASSET`: Debt-to-asset ratio

Simply add these fields to the relevant request in the API call.

## Advanced Features

### Sector Information

The Bloomberg API integration now automatically retrieves sector information for all NIFTY 500 constituents using the GICS (Global Industry Classification Standard) sector classification. This allows you to:

1. Analyze performance by sector
2. Identify sector trends
3. Compare stocks within their respective sectors
4. Diversify your portfolio across sectors

The sector information is added directly to the `nifty500_list.csv` file as an additional column. You can use this data in your analysis without any additional steps.

### Financial Metrics

In addition to price data, the system now retrieves key financial metrics for each stock:

1. **Price-to-Earnings Ratio (PE_Ratio)**: Indicates how much investors are willing to pay for each rupee of earnings
2. **Price-to-Book Ratio (PB_Ratio)**: Compares a company's market value to its book value
3. **Return on Equity (ROE)**: Measures a company's profitability relative to shareholders' equity
4. **Debt-to-Asset Ratio (DebtToAsset)**: Indicates what proportion of a company's assets are financed by debt
5. **Dividend Yield (DividendYield)**: Annual dividend payments relative to share price

These metrics are saved to a separate file called `financial_metrics.csv` in your output directory.

### Using Financial Metrics

You can use these financial metrics in your analysis to:

1. **Filter Stocks**: For example, focus on stocks with high ROE and low PE ratios
2. **Create Multi-factor Models**: Combine metrics with return data for more sophisticated analysis
3. **Identify Value Stocks**: Look for stocks with low PE and PB ratios relative to their sector
4. **Find Dividend Opportunities**: Focus on stocks with high dividend yields

Example Python code to incorporate financial metrics in your analysis:

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

## Enhanced Reliability

The Bloomberg data extractor now includes several features to improve reliability:

### Automatic Retries

The system will automatically retry Bloomberg API requests up to 3 times if connection issues occur. This helps handle temporary network disruptions or Bloomberg service availability issues.

### Timeout Handling

API requests now have a timeout mechanism to prevent the system from hanging indefinitely if Bloomberg is unresponsive.

### Batch Processing

Data is retrieved in batches of 50 securities at a time to avoid overwhelming the Bloomberg API and to make more efficient use of the connection. This helps prevent rate limiting and improves overall reliability.

### Error Recovery

If sector information or financial metrics cannot be retrieved, the system will continue with the core functionality (price data and stock ranking) rather than failing completely.

## Test Mode

For development and testing purposes, you can run the data extractor in test mode without an actual Bloomberg connection:

```bash
python src/bloomberg_data_extractor.py --output-dir data --test-mode
```

This will generate synthetic data with realistic properties, allowing you to test the rest of the system without Bloomberg access.

## Performance Considerations

### Connection Efficiency

The system optimizes Bloomberg API usage by:

1. Reusing session connections where possible
2. Requesting multiple data fields in a single request
3. Processing data in batches of appropriate size
4. Releasing Bloomberg resources promptly

### Data Volume Management

When working with the full NIFTY 500 index and many years of historical data, the API requests can generate substantial data volume. If you experience performance issues:

1. Consider reducing the date range (e.g., 5 years instead of 15)
2. Focus on a subset of stocks if you only need specific sectors
3. Increase batch timeout values if you're on a slower network connection

## Troubleshooting Bloomberg API Connection

### Unable to Connect to Bloomberg

If you see errors like "Failed to start Bloomberg API session":

1. Verify that the Bloomberg Terminal application is running and logged in
2. Check that you're using the correct host and port (default: localhost:8194)
3. Ensure that the Bloomberg API service is enabled (can be checked in the Terminal)
4. Check your network connectivity to the Bloomberg service

### Missing Sector Data

If sector information is missing for some stocks:

1. Verify that the stocks are still active and part of the NIFTY 500 index
2. Check if the GICS sector classification is available for these stocks
3. Consider manually adding sector information for these stocks if needed

### Handling Rate Limits

If you encounter rate limiting from Bloomberg:

1. Increase the sleep time between batch requests
2. Reduce the batch size (e.g., from 50 to 25 stocks per batch)
3. Run the extraction during off-peak hours
4. Split your extraction into multiple runs (e.g., get constituents in one run, prices in another) 