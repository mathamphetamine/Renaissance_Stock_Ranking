# Bloomberg API Integration Guide

This guide explains how to automate data extraction from Bloomberg using the Bloomberg API (BLPAPI) instead of manually exporting data. This approach saves time and reduces the potential for human error when collecting data for the Renaissance Stock Ranking System.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation and Setup](#installation-and-setup)
3. [Using the Automated Extractor](#using-the-automated-extractor)
4. [Test Mode for Development](#test-mode-for-development)
5. [Internal Implementation Details](#internal-implementation-details)
6. [Enhanced Reliability Features](#enhanced-reliability-features)
7. [Advanced Features (Sector & Metrics)](#advanced-features-sector--metrics)
8. [Troubleshooting API Connection](#troubleshooting-api-connection)
9. [Setting Up Scheduled Extraction](#setting-up-scheduled-extraction)
10. [Bloomberg API vs. Manual Extraction](#bloomberg-api-vs-manual-extraction)
11. [Bloomberg Fields Reference](#bloomberg-fields-reference)
12. [Need More Help?](#need-more-help)

## Prerequisites

Before you can use the Bloomberg API integration, you need:

- **Bloomberg Terminal**: Installed with an active subscription, running, and logged in.
- **Bloomberg Desktop API (DAPI)**: Installed on the same machine (usually part of the Terminal install or available via `WAPI <GO>`).
- **Python**: Version 3.8 or higher installed.
- **Renaissance Stock Ranking System**: Cloned and set up (virtual environment activated).
- **`blpapi` Python Package**: Installed within the activated virtual environment (see below).
- **Network Access**: To Bloomberg services.

## Installation and Setup

Follow these steps within your activated virtual environment for the Renaissance project:

1.  **Install the Core Package (if not already done):**
```bash
    pip install -e .
    ```

2.  **Install the `blpapi` Python Package:**
    *   **Ensure Bloomberg Terminal is running and logged in.**
    *   Run the following command:
    ```bash
    pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
    ```
    *   *(Note: This package cannot be included directly in our `setup.py` because it's hosted on Bloomberg's private index, not PyPI).*

3.  **Verify Installation (Optional but Recommended):**
    Create a simple Python script (`test_blpapi.py`):
```python
import blpapi
import time

    print("Attempting to connect to Bloomberg...")
session_options = blpapi.SessionOptions()
session_options.setServerHost('localhost')
    session_options.setServerPort(8194) # Default DAPI port

session = blpapi.Session(session_options)
if not session.start():
        print("ERROR: Failed to start session. Is Bloomberg Terminal running and logged in?")
    exit(1)

    print("SUCCESS: Session started.")

    if not session.openService("//blp/refdata"):
        print("ERROR: Failed to open //blp/refdata service.")
        session.stop()
        exit(1)

    print("SUCCESS: //blp/refdata service opened.")
    print("Bloomberg API connection successful!")

session.stop()
    print("Session stopped.")
    ```
    Run it from your activated virtual environment:
    ```bash
    python test_blpapi.py
    ```
    A successful run will print connection success messages.

## Using the Automated Extractor

Once `blpapi` is installed, you can use the `renaissance-extract` command to fetch data.

### Step 1: Ensure Bloomberg Terminal is Running
Make sure you are logged into your Bloomberg Terminal session.

### Step 2: Run the Extractor Command

Navigate to your project directory in the terminal (with the virtual environment activated) and run:

```bash
renaissance-extract
```

This command will:
1.  Connect to the Bloomberg API.
2.  Fetch the NIFTY 500 constituent list (including ISIN, Name, Ticker, Sector).
3.  Fetch historical monthly adjusted closing prices for all constituents.
4.  Fetch key financial metrics (P/E, P/B, ROE, etc.).
5.  Save the data into three CSV files in the `data/` directory (by default):
    *   `nifty500_list.csv`
    *   `historical_prices.csv`
    *   `financial_metrics.csv`

### Command Options

*   `--output-dir <path>`: Specify a different directory to save the output CSV files.
*   `--start-date YYYY-MM-DD`: Set a custom start date for historical price data (default is 15 years ago).
*   `--end-date YYYY-MM-DD`: Set a custom end date (default is today).
*   `--test-mode`: Run without connecting to Bloomberg, using sample data (see next section).
*   `--help`: Display all available options.

**Example with Options:**
```bash
renaissance-extract --output-dir ./bloomberg_data --start-date 2015-01-01
```

### Alternative: Using the Script
You can achieve the same result by running the script directly:
```bash
python scripts/extract_bloomberg.py --output-dir ./bloomberg_data
```

## Test Mode for Development

If you don't have Bloomberg access or want to test the rest of the system workflow without making live API calls, use the `--test-mode` flag:

```bash
renaissance-extract --test-mode
```

This will:
- **Skip** all Bloomberg API connections.
- Generate **sample** `nifty500_list.csv`, `historical_prices.csv`, and `financial_metrics.csv` files in the output directory (default: `data/`).
- Allow you to proceed with `renaissance-rank`, `renaissance-analyze`, and `renaissance-visualize` using consistent sample data.

This mode is crucial for development, testing, and users without a Bloomberg license.

## Internal Implementation Details

The core logic resides in `renaissance/data_extraction/bloomberg_data_extractor.py`. Key functions involved:

*   `get_nifty500_constituents()`: Fetches the index members and sector data.
*   `get_historical_prices()`: Fetches adjusted monthly closing prices.
*   `get_additional_metrics()`: Fetches financial ratios.
*   `main()`: Orchestrates the process, handles arguments, and calls the other functions.

These functions use the `blpapi` package to:
1.  Establish a session with the local Bloomberg DAPI.
2.  Open the reference data service (`//blp/refdata`).
3.  Create and send appropriate requests (`ReferenceDataRequest`, `HistoricalDataRequest`).
4.  Parse the responses and format the data into pandas DataFrames.

## Enhanced Reliability Features

*   **Conditional Import**: `blpapi` is imported only when *not* in `--test-mode`, preventing errors if the package isn't installed for test runs.
*   **Automatic Retries**: Connection attempts and requests are retried automatically (up to 3 times with delays) if transient network issues occur.
*   **Timeout Handling**: API requests include timeouts to prevent indefinite hangs.
*   **Batch Processing**: Historical data and metrics requests are processed in batches (e.g., 50 securities at a time) to avoid overloading the API.
*   **Error Recovery**: If fetching optional data like financial metrics fails, the process logs a warning and continues, allowing the core price and constituent data to still be saved.

## Advanced Features (Sector & Metrics)

*   **Sector Information**: The extractor automatically retrieves GICS sector names (`GICS_SECTOR_NAME`) and includes them in `nifty500_list.csv`. This is used by `renaissance-analyze`.
*   **Financial Metrics**: Key ratios (P/E, P/B, ROE, Debt/Asset, Dividend Yield) are fetched and saved to `financial_metrics.csv`. `renaissance-analyze` can use this file to provide richer sector comparisons.

## Troubleshooting API Connection

*(Referenced from main README and User Guide, consolidated here)*

*   **Problem**: `ModuleNotFoundError: No module named 'blpapi'`
    *   **Solution**: Ensure virtual environment is active and `blpapi` was installed correctly via `pip install --index-url=... blpapi`.

*   **Problem**: `Failed to start session` / `Failed to open //blp/refdata service` / Connection errors.
    *   **Solution 1**: **CRITICAL**: Ensure Bloomberg Terminal is running and you are **logged in**.
    *   **Solution 2**: Verify `blpapi` package installed correctly (Step 3 in Installation).
    *   **Solution 3**: Check network connectivity / firewalls.
    *   **Solution 4**: Restart Bloomberg Terminal.
    *   **Solution 5**: Ensure DAPI service is running (check system services or `WAPI <GO>`).
    *   **Solution 6**: Consult official Bloomberg API documentation / Help Desk (`HELP HELP` on Terminal).

*   **Problem**: Data retrieval is slow or times out.
    *   **Solution**: Check network speed. Run during off-peak hours. Potentially reduce date range if requesting very long histories.

*   **Problem**: Missing data for some stocks/fields.
    *   **Solution**: Data may genuinely not be available in Bloomberg for that specific security/field/date range. The extractor attempts to handle missing fields gracefully.

## Setting Up Scheduled Extraction

To automate monthly data updates:

1.  **Create a Script**: Write a simple shell script (`.sh` for Linux/macOS) or batch file (`.bat` for Windows) that activates the virtual environment and runs `renaissance-extract`.

    *Example (`run_extractor.sh`):*
   ```bash
   #!/bin/bash
    # Navigate to the project directory
   cd /path/to/Renaissance_Stock_Ranking
    # Activate virtual environment
   source venv/bin/activate
    # Run the extractor (ensure Bloomberg is running!)
    renaissance-extract --output-dir ./data # Ensure output goes to the right place
    # Optional: Deactivate environment
    # deactivate
    ```

2.  **Schedule the Script**: Use your operating system's task scheduler:
    *   **Windows**: Task Scheduler
    *   **macOS/Linux**: `cron`

    *Example `crontab` entry (runs 6 PM on the first Friday of the month):*
    ```
    0 18 * * 5 [ $(date +\%u) -eq 5 ] && /path/to/run_extractor.sh > /path/to/extractor.log 2>&1
    ```

    **Important**: Scheduled tasks running `renaissance-extract` still require the Bloomberg Terminal to be running and logged in on the machine at the scheduled time.

## Bloomberg API vs. Manual Extraction

| Feature         | Bloomberg API (`renaissance-extract`) | Manual Extraction (Excel Add-in / Terminal) |
| :-------------- | :------------------------------------ | :------------------------------------------ |
| **Speed**       | Fast, automated                       | Slow, manual                                |
| **Accuracy**    | High (programmatic)                   | Prone to copy/paste errors                  |
| **Consistency** | High                                  | Variable                                    |
| **Effort**      | Low (after initial setup)             | High (repetitive monthly task)              |
| **Automation**  | Fully scriptable, schedulable         | Manual process required                     |
| **Features**    | Includes Sectors & Financial Metrics  | Requires extra manual steps for these       |
| **Requirement** | `blpapi` installed, Terminal running  | Bloomberg Terminal access                   |
| **Manual Extraction**: Provides detailed steps for exporting data manually from Bloomberg Terminal and Excel if API access is unavailable or problematic. See [Manual Data Extraction Guide](data_extraction_guide.md).

**Recommendation**: Use the API method (`renaissance-extract`) whenever possible for efficiency and accuracy.

## Bloomberg Fields Reference

Key fields used by `renaissance-extract`:

*   **Constituents**: `INDX_MWEIGHT_HIST` (Members), `ID_ISIN` (ISIN), `NAME` (Name), `TICKER` (Ticker), `GICS_SECTOR_NAME` (Sector)
*   **Prices**: `PX_LAST` (Adjusted Closing Price)
*   **Metrics**: `PE_RATIO`, `PX_TO_BOOK_RATIO`, `RETURN_COM_EQY`, `TOT_DEBT_TO_TOT_ASSET`, `EQY_DVD_YLD_IND`

Use `FLDS <GO>` on the Bloomberg Terminal to search for other available fields.

## Need More Help?

- Check the extractor logs: `output/logs/bloomberg_extractor.log`
- Refer to the main [Troubleshooting Guide](#troubleshooting-api-connection).
- Consult the official Bloomberg API documentation.
- Contact Bloomberg support via the Terminal (`HELP HELP`).