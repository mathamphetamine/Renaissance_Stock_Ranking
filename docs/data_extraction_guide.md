# Bloomberg Data Extraction Guide

This guide outlines the steps to extract the necessary data from the Bloomberg Terminal for the NIFTY 500 Stock Ranking System. This extraction process needs to be performed while in the office with access to the Bloomberg Terminal.

## Quick Reference Workflow

```
┌───────────────────────────────────────────────────────────────┐
│ STEP 1: Open Bloomberg Terminal or Bloomberg Excel Add-in     │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 2: Extract NIFTY 500 Constituent List with ISINs         │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 3: Save as nifty500_list.csv                             │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 4: Extract Monthly Closing Prices for all NIFTY 500      │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 5: Save as historical_prices.csv                         │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 6: Place both files in the 'data' folder                 │
└───────────────────────────────────────────────────────────────┘
```

## Data Requirements

The system requires two primary datasets:

1. **NIFTY 500 Constituent List**: A list of all stocks in the NIFTY 500 index, with their ISINs as the primary identifier.
2. **Historical Monthly Closing Prices**: Month-end closing prices for all NIFTY 500 stocks over a 15-year period.

## Step 1: Extract NIFTY 500 Constituent List

### Using Bloomberg Excel Add-in (Recommended):

1. Open Microsoft Excel with the Bloomberg Add-in installed.
2. Use the following formula to get the NIFTY 500 constituents:
   ```
   =BDS("NIFTY 500 Index", "INDX_MWEIGHT_HIST", "INDX_MWEIGHT_HIST_END_DT=YYYYMMDD")
   ```
   (Replace YYYYMMDD with the current or desired date)

3. Ensure the output includes the following columns:
   - ISIN (required)
   - Company Name
   - Bloomberg Ticker (optional but useful)

4. Save the result as a CSV file named `nifty500_list.csv` with the following structure:

   | ISIN         | Name          | Ticker    |
   |--------------|---------------|-----------|
   | INE009A01021 | Company A Ltd | COMPA:IN  |
   | INE062A01020 | Company B Ltd | COMPB:IN  |
   | ...          | ...           | ...       |

### Alternative: Manual Extraction:

1. In the Bloomberg Terminal, type `NIFTY 500 Index <GO>`.
2. Press `4` (Members) or navigate to the "Members" tab.
3. Export the data to Excel (use the "Export to Excel" option).
4. Ensure that ISINs are included in the exported data.
5. Save as a CSV file with the same structure as above.

## Step 2: Extract Historical Monthly Closing Prices

### Using Bloomberg Excel Add-in (Recommended):

1. Open Microsoft Excel with the Bloomberg Add-in installed.
2. Create a list of all ISINs from the NIFTY 500 constituent list.
3. Use the following formula for each ISIN:
   ```
   =BDH("ISIN Equity", "PX_LAST", "YYYYMMDD", "YYYYMMDD", "CURR=INR", "DAYS=ACTUAL", "FILL=P", "PERIODICTY=MONTHLY")
   ```
   (Replace ISIN with each stock's ISIN, and YYYYMMDD with the start and end dates for the 15-year period)

4. Ensure the output includes the following columns:
   - ISIN
   - Date (month-end dates)
   - Price (adjusted for corporate actions)

5. Combine all the data and save as a CSV file named `historical_prices.csv` with the following structure:

   | ISIN         | Date       | Price   |
   |--------------|------------|---------|
   | INE009A01021 | 2008-01-31 | 250.75  |
   | INE009A01021 | 2008-02-29 | 245.30  |
   | INE062A01020 | 2008-01-31 | 1250.00 |
   | ...          | ...        | ...     |

### Alternative: Batch Export:

1. In the Bloomberg Terminal, use the EXCEL <GO> function to set up a batch export.
2. Create a template with the required fields (ISIN, Date, PX_LAST).
3. Set the periodicity to Monthly.
4. Ensure "Pricing Defaults" are set to include adjustments for corporate actions.
5. Run the batch export for all NIFTY 500 ISINs.
6. Combine the results and save as a CSV file with the same structure as above.

## Important Considerations

### Corporate Actions

Bloomberg data should be adjusted for corporate actions by default. When extracting data, ensure that:

- The "Adjusted Prices" option is selected (this is usually the default).
- The data includes adjustments for stock splits, dividends, and other corporate actions.

### Date Range

- Extract data for at least 15 years to allow for proper historical analysis.
- Ensure all dates are month-end dates for consistency.

### Data Format

- Ensure dates are in a format that pandas can parse (YYYY-MM-DD recommended).
- Verify that all prices are in the same currency (INR recommended).

## Troubleshooting

### Missing Data

If you encounter missing data for some stocks:

1. Check if the stock was listed for the entire period. Newer listings will naturally have missing historical data.
2. For stocks that were delisted or underwent significant corporate restructuring, note this in a separate document.

### Bloomberg API Alternative

If available and approved, you can use the Bloomberg API (BLPAPI) with Python to extract data programmatically. This would require:

1. Bloomberg API access and proper configuration.
2. Python code to connect to Bloomberg and fetch the required data.
3. Knowledge of Bloomberg API functions for retrieving index constituents and historical prices.

## File Placement

After extracting the data:

1. Save the NIFTY 500 constituent list as `nifty500_list.csv`.
2. Save the historical price data as `historical_prices.csv`.
3. Place both files in the `data/` directory of the NIFTY 500 Stock Ranking System.

The system will then process these files to generate the required analysis and outputs. 

## For Non-Technical Users

If you're not familiar with data extraction or CSV files, here's a simplified explanation:

### What Are We Doing?
We need two tables of information:
1. **A list of all companies in the NIFTY 500 index** (with their unique identifiers)
2. **The month-end stock prices for these companies** (over several years)

### What Should the Files Look Like?

#### NIFTY 500 List File (nifty500_list.csv):
This should look like a table with company information:

```
ISIN,Name,Ticker
INE009A01021,Infosys Ltd,INFO IN
INE062A01020,Tata Consultancy Services Ltd,TCS IN
INE040A01034,HDFC Bank Ltd,HDFCB IN
```

#### Historical Prices File (historical_prices.csv):
This should look like a table with stock prices by date:

```
ISIN,Date,Price
INE009A01021,2022-01-31,1680.75
INE009A01021,2022-02-28,1722.30
INE062A01020,2022-01-31,3698.15
```

### Checklist Before Running the System:

- Both files are saved as CSV (you can create these in Excel, then "Save As" CSV)
- The column names are exactly as shown above
- Dates are in YYYY-MM-DD format
- Both files are placed in the "data" folder of the project
- ISIN values are consistent between both files

If you have any trouble with extraction or the file format, please contact the IT department for assistance. 