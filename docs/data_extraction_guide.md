# Bloomberg Data Extraction Guide

This guide provides detailed, step-by-step instructions for extracting data from the Bloomberg Terminal for the Renaissance Stock Ranking System. It is designed to be accessible even if you have limited Bloomberg Terminal experience.

## Table of Contents
1. [Visual Workflow Overview](#visual-workflow-overview)
2. [Prepare Your Workspace](#prepare-your-workspace)
3. [Extract NIFTY 500 Constituent List](#extract-nifty-500-constituent-list)
   - [Method A: Using Bloomberg Excel Add-in](#method-a-using-bloomberg-excel-add-in-recommended)
   - [Method B: Manual Extraction via Bloomberg Terminal](#method-b-manual-extraction-via-bloomberg-terminal)
4. [Format and Save Constituent List](#format-and-save-constituent-list)
5. [Extract Historical Price Data](#extract-historical-price-data)
   - [Method A: Using Bloomberg Excel Add-in](#method-a-using-bloomberg-excel-add-in-recommended-1)
   - [Method B: Using Bulk Data Export](#method-b-using-bulk-data-export-from-bloomberg-terminal)
6. [Format and Save Price Data](#format-and-save-price-data)
7. [Extract Financial Metrics (Optional)](#extract-financial-metrics-optional)
8. [Place Files in the Data Folder](#place-files-in-the-data-folder)
9. [Troubleshooting Common Issues](#troubleshooting-common-issues)
10. [Tips for Efficient Extraction](#tips-for-efficient-extraction)
11. [Visual Guide for Non-Technical Users](#for-non-technical-users-visual-guide)
12. [Summary Checklist](#summary-checklist)

## Visual Workflow Overview

```
┌───────────────────────────────────────────────────────────────┐
│ STEP 1: Prepare Your Workspace                                │
│         Open Bloomberg Terminal and have Excel ready          │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 2: Extract NIFTY 500 Constituent List                    │
│         Get the complete list with ISINs, names, and tickers  │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 3: Format and Save Constituent List                      │
│         Ensure proper columns and save as nifty500_list.csv   │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 4: Extract Historical Prices                             │
│         Get monthly closing prices for all constituents       │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 5: Format and Save Price Data                            │
│         Ensure proper format and save as historical_prices.csv│
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 6: (Optional) Extract Financial Metrics                  │
│         Get PE, PB, ROE and other metrics for additional      │
│         analysis capabilities                                 │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│ STEP 7: Place Files in the 'data' Folder                      │
│         Make the files available to the ranking system        │
└───────────────────────────────────────────────────────────────┘
```

## Prepare Your Workspace

Before you begin extracting data, make sure you have the following ready:

1. **Bloomberg Terminal** is open and you are logged in
2. **Microsoft Excel** is installed with the Bloomberg Excel Add-in
3. The `data` folder of the Renaissance Stock Ranking System is accessible

**TIP**: Create a dedicated folder on your desktop to temporarily store the exported files before moving them to the `data` folder.

## Extract NIFTY 500 Constituent List

The constituent list contains all the stocks in the NIFTY 500 index with their identifying information.

### Method A: Using Bloomberg Excel Add-in (Recommended)

1. **Open Microsoft Excel** with a new, blank workbook
2. **Insert the Bloomberg formula**:
   - Click on cell A1
   - Type the following formula:
     ```
     =BDS("NIFTY 500 Index", "INDX_MWEIGHT_HIST", "INDX_MWEIGHT_HIST_END_DT=YYYYMMDD")
     ```
   - Replace `YYYYMMDD` with today's date in the format `20230315` (for March 15, 2023)
   - Press Enter

3. **Wait for data to load**:
   - You should see "Loading..." appear briefly
   - Then a table will populate with the NIFTY 500 constituents

   The resulting table should look something like this:
   ```
   INDEX_MEMBER | NAME                | ID_ISIN       | TICKER
   -------------+---------------------+---------------+----------
   1            | HDFC Bank Ltd       | INE040A01034  | HDFCB IN
   2            | Infosys Ltd         | INE009A01021  | INFO IN
   3            | Reliance Ind Ltd    | INE030A01027  | RIL IN
   ...          | ...                 | ...           | ...
   ```

4. **Add a Sector column**:
   - If your data already includes a sector column, keep it
   - If not, you can add it with another Bloomberg formula:
     - In the first empty column (e.g., column E), add a header "Sector"
     - In the cell below (e.g., E2), type the formula:
       ```
       =BDP(D2&" Equity", "GICS_SECTOR_NAME")
       ```
     - Copy this formula down for all rows (where D2 is the cell containing the ticker)

### Method B: Manual Extraction via Bloomberg Terminal

If the Excel Add-in is not working, you can extract the data directly from the Terminal:

1. In the Bloomberg Terminal, **type** `NIFTY 500 Index <GO>` and press Enter
2. You will see the index information page
3. **Press 4** or click on the "Members" tab
4. You will see a list of NIFTY 500 constituents
5. **Click on the Actions button** (usually at top right)
6. **Select "Export to Excel"**
7. Save the file to your designated folder

## Format and Save Constituent List

Now that you have the constituent data, you need to format it properly:

1. **Ensure the following columns are present**:
   - ISIN (required - this is the unique identifier for each stock)
   - Name (required - the company name)
   - Ticker (optional but useful)
   - Sector (optional but required for sector analysis)

2. **Clean up the data**:
   - Remove any header rows or Bloomberg metadata
   - Ensure column names are exactly: `ISIN`, `Name`, `Ticker`, and `Sector`
   - Remove any extra columns that aren't needed

3. **Save as CSV**:
   - Click "File" → "Save As"
   - Choose "CSV (Comma delimited) (*.csv)" as the file type
   - Name the file `nifty500_list.csv`
   - Save to your designated folder

Your file should look like this when opened in a text editor:
```
ISIN,Name,Ticker,Sector
INE040A01034,HDFC Bank Ltd,HDFCB IN,Financials
INE009A01021,Infosys Ltd,INFO IN,Information Technology
INE030A01027,Reliance Industries Ltd,RIL IN,Energy
...
```

## Extract Historical Price Data

Now you need to get historical monthly closing prices for all the stocks in the NIFTY 500 list.

### Method A: Using Bloomberg Excel Add-in (Recommended)

1. **Create a new Excel workbook** or a new sheet in your existing workbook

2. **Set up the data extraction**:
   - In cell A1, type "ISIN"
   - In cell B1, type "Date"
   - In cell C1, type "Price"

3. **Use Bloomberg's historical data function**:
   - This can be done in several ways:
   
   #### Option 1: Using the Bloomberg Formula for Each Stock (Most Reliable)
   
   For each stock in your NIFTY 500 list:
   
   ```
   =BDH("ISIN Equity", "PX_LAST", "START_DATE", "END_DATE", "CURR=INR", "DAYS=ACTUAL", "FILL=P", "PERIODICTY=MONTHLY")
   ```
   
   Replace:
   - `ISIN` with the stock's ISIN (e.g., INE040A01034)
   - `START_DATE` with your desired start date (e.g., 20080101 for Jan 1, 2008)
   - `END_DATE` with today's date (e.g., 20230315 for Mar 15, 2023)
   
   #### Option 2: Using the Bloomberg Excel Import Wizard (Easier for Beginners)
   
   1. In Excel, click on the Bloomberg tab in the ribbon
   2. Click "Import Data" → "Historical End of Day"
   3. In the dialog that appears:
      - For Securities, click "Multiple Securities" and import your list of ISINs
      - For Fields, select "PX_LAST" (Last Price)
      - For Date, set your desired start and end dates
      - In Settings, set Periodicity to "Monthly"
      - Make sure "All pricing values in base currency" is checked with INR as the currency
   4. Click "Export"

4. **Wait for all data to load** (this may take a while for 500 stocks)

### Method B: Using Bulk Data Export from Bloomberg Terminal

For large datasets, Bloomberg's bulk export might be faster:

1. In the Bloomberg Terminal, type `EXCEL <GO>` and press Enter
2. Click on "Historical Data"
3. Follow the prompts to:
   - Select all NIFTY 500 stocks (you can paste in the list of ISINs)
   - Choose "PX_LAST" as the field
   - Set the date range (try to get at least 15 years of data)
   - Set periodicity to "Monthly"
   - Set currency to INR
4. Click "Export" and wait for the data to be processed
5. Save the file when prompted

## Format and Save Price Data

After extracting the price data, you need to format it correctly:

1. **Consolidate your data** into a three-column format:
   - Column A: ISIN
   - Column B: Date (in YYYY-MM-DD format)
   - Column C: Price

2. **Ensure dates are in the correct format**:
   - Bloomberg often exports dates in MM/DD/YYYY format
   - You need to convert them to YYYY-MM-DD format
   - In Excel, you can do this by:
     - Selecting the date column
     - Right-click → Format Cells → Custom → Type "yyyy-mm-dd"

3. **Save as CSV**:
   - Click "File" → "Save As"
   - Choose "CSV (Comma delimited) (*.csv)" as the file type
   - Name the file `historical_prices.csv`
   - Save to your designated folder

Your file should look like this when opened in a text editor:
```
ISIN,Date,Price
INE040A01034,2022-01-31,1450.75
INE040A01034,2022-02-28,1487.25
INE009A01021,2022-01-31,1486.70
...
```

## Extract Financial Metrics (Optional)

For enhanced analysis capabilities, you can also extract financial metrics:

1. **Create a new Excel workbook** or sheet

2. **Use Bloomberg to extract financial metrics**:
   - You can use a formula like this:
     ```
     =BDP("ISIN Equity", "PE_RATIO,PB_RATIO,RETURN_COM_EQY,TOT_DEBT_TO_TOT_ASSET,EQY_DVD_YLD_IND")
     ```
   - Replace `ISIN` with each stock's ISIN

3. **Format and save**:
   - Ensure the data has these columns: `ISIN,PE_Ratio,PB_Ratio,ROE,DebtToAsset,DividendYield`
   - Save as `financial_metrics.csv` in your designated folder

Your file should look like this when opened in a text editor:
```
ISIN,PE_Ratio,PB_Ratio,ROE,DebtToAsset,DividendYield
INE009A01021,23.8,4.2,25.6,0.12,1.8
INE062A01020,27.6,11.5,41.2,0.07,1.4
INE040A01034,19.5,3.2,16.8,0.56,0.7
```

## Place Files in the Data Folder

Finally, move your extracted files to the correct location:

1. **Locate the `data` folder** in your Renaissance Stock Ranking System directory
2. **Copy the files** you created:
   - `nifty500_list.csv`
   - `historical_prices.csv`
   - `financial_metrics.csv` (if created)
3. **Paste them** into the `data` folder, replacing any existing files

## Troubleshooting Common Issues

### "Formula Error" or "#N/A" in Excel

- **Problem**: Bloomberg formulas return errors
- **Solution**: 
  - Make sure you're logged into Bloomberg
  - Check that the Bloomberg Excel Add-in is properly installed
  - Try restarting Excel or using the Bloomberg Help Desk (HELP <GO>)

### Missing ISINs or Data Gaps

- **Problem**: Some stocks have missing price data
- **Solution**:
  - This is normal for newer listings or recently included stocks
  - Focus on ensuring the data you do have is correctly formatted
  - The system will handle missing data appropriately

### Date Format Issues

- **Problem**: Dates aren't in YYYY-MM-DD format
- **Solution**:
  - Use Excel's date formatting options
  - Or convert using formulas: `=TEXT(your_date_cell,"yyyy-mm-dd")`

### Too Much Data to Handle in Excel

- **Problem**: Excel struggles with large datasets
- **Solution**:
  - Process data in smaller batches (e.g., 100 stocks at a time)
  - Consider using the Bloomberg API if you have programming experience
  - See the [Bloomberg API Guide](bloomberg_api_guide.md) for automated extraction

### Problem: Not all NIFTY 500 constituents are available
**Solution**: Verify that you're looking at the current NIFTY 500 index. Some constituents may have been added or removed recently. Use the most recent official list.

### Problem: Missing historical price data for some stocks
**Solution**: Some stocks might have been newly listed or may not have price data for the entire period. The system can handle these gaps, but try to get as complete data as possible.

### Problem: Dates are not in the correct format
**Solution**: Ensure dates are in YYYY-MM-DD format. In Excel, select the date column and apply formatting: Custom > "yyyy-mm-dd".

### Problem: UTF-8 encoding issues in company names
**Solution**: Save your CSV files with UTF-8 encoding. In Excel: File > Save As > Select CSV > Tools > Web Options > Encoding > "Unicode (UTF-8)".

## Summary Checklist

Before running the ranking system, make sure:

- [  ] `nifty500_list.csv` has columns: ISIN, Name, Ticker, (optional) Sector
- [  ] `historical_prices.csv` has columns: ISIN, Date, Price
- [  ] Dates are in YYYY-MM-DD format
- [  ] (Optional) `financial_metrics.csv` has been created
- [  ] All files are placed in the `data` folder
- [  ] Price data spans at least 13 months (to calculate yearly returns)

Once these steps are complete, you're ready to run the ranking system!

## For Non-Technical Users: Visual Guide

Here's a simplified visual guide to the data formats:

### The NIFTY 500 List File (`nifty500_list.csv`)
This is like a directory of all the companies we're analyzing:

```
┌──────────────────┬──────────────────┬──────────────┬─────────────────────┐
│      ISIN        │       Name       │    Ticker    │        Sector       │
├──────────────────┼──────────────────┼──────────────┼─────────────────────┤
│ INE040A01034     │ HDFC Bank Ltd    │ HDFCB IN     │ Financials          │
│ INE009A01021     │ Infosys Ltd      │ INFO IN      │ Information Tech    │
│ INE030A01027     │ Reliance Ind Ltd │ RIL IN       │ Energy              │
│     ...          │      ...         │    ...       │        ...          │
└──────────────────┴──────────────────┴──────────────┴─────────────────────┘
   ↑                   ↑                  ↑                ↑
   ID number           Company name       Stock symbol     Industry category
```

### The Historical Prices File (`historical_prices.csv`)
This is like a price diary for each company over time:

```
┌──────────────────┬────────────┬───────────┐
│      ISIN        │    Date    │   Price   │
├──────────────────┼────────────┼───────────┤
│ INE040A01034     │ 2022-01-31 │  1450.75  │
│ INE040A01034     │ 2022-02-28 │  1487.25  │
│ INE009A01021     │ 2022-01-31 │  1486.70  │
│     ...          │    ...     │    ...    │
└──────────────────┴────────────┴───────────┘
   ↑                   ↑            ↑
   Same ID number      Month-end    Stock price
   as in list file     date         on that date
```

If you follow this visual guide, you'll have the data in the perfect format for the system to analyze!

## Tips for Efficient Extraction

1. **Use Bulk Operations**: Extract data for all securities at once rather than one by one to save time.

2. **Automate Recurring Extractions**: Consider setting up a Bloomberg API connection for automated extraction (see the [Bloomberg API Guide](bloomberg_api_guide.md)).

3. **Check for Corporate Actions**: Ensure that historical price data is adjusted for stock splits, dividends, etc. In Bloomberg, select "Last Price Adjusted" when available.

4. **Regular Updates**: Update your data monthly for the best results. Schedule a specific day each month for this task.

5. **Data Validation**: Always check a sample of the extracted data against the Bloomberg Terminal values to ensure accuracy.

## Next Steps

After successfully extracting and formatting all the required data files, place them in the `data/` directory of your Renaissance Stock Ranking System installation, and you're ready to run the ranking process using:

```bash
python scripts/run_ranking.py
```

For automated data extraction, see the [Bloomberg API Guide](bloomberg_api_guide.md).