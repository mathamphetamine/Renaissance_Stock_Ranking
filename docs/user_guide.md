# Renaissance Stock Ranking System - User Guide

This guide provides detailed instructions on how to use the Automated Stock Ranking System for Renaissance Investment Managers.

## Table of Contents
1. [System Overview](#system-overview)
2. [Installation and Setup](#installation-and-setup)
3. [Data Requirements](#data-requirements)
4. [Running the System](#running-the-system)
5. [Interpreting Results](#interpreting-results)
6. [Extending the System](#extending-the-system)
7. [Troubleshooting](#troubleshooting)
8. [Quick Reference](#quick-reference)

## System Overview

The Automated Stock Ranking System for Renaissance Investment Managers is designed to:

1.  Load NIFTY 500 constituent data and historical price information from CSV files (or extract directly from Bloomberg).
2.  Calculate yearly returns on a monthly rolling basis (12-month returns ending each month).
3.  Rank stocks based on these returns.
4.  Track month-over-month rank changes.
5.  Generate easy-to-interpret output files (Excel, CSV) with rankings and analysis.
6.  Analyze sector performance and provide investment insights.
7.  Create visualizations for better data understanding.

This replaces the previous manual process of collecting and analyzing this data in Excel spreadsheets.

### System Workflow Diagram

```
┌───────────────────────────────────────────────────────────────────────┐
│                       COMPLETE WORKFLOW DIAGRAM                        │
└───────────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼─────────────────────────────────────────┐
│ 1️⃣ INSTALLATION (One Time)                                             │
│   ┌─────────────┐     ┌───────────────┐     ┌───────────────────┐    │
│   │ Clone Repo  │────>│ Setup Venv &  │────>│ Install blpapi /  │    │
│   │ & Install   │     │ Activate Venv │     │ Optional Extras   │    │
│   │ (pip install .) │     │               │     │                   │    │
│   └─────────────┘     └───────────────┘     └──────────┬────────┘    │
│                                                          │             │
└──────────────────────────────────────────────────────────▼─────────────┘
                                                           │
┌──────────────────────────────────────────────────────────▼─────────────┐
│ 2️⃣ DATA EXTRACTION (Run Periodically, e.g., Monthly)                 │
│   ┌───────────────────────────────────┐                                │
│   │ renaissance-extract               │                                │
│   │ (Use --test-mode if no Bloomberg) │                                │
│   └─────────────────┬─────────────────┘                                │
│                     │ (Creates files in data/)                         │
└─────────────────────▼────────────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────────────┐
│ 3️⃣ RANKING CALCULATION                                                 │
│   ┌───────────────────────────────────┐                                │
│   │ renaissance-rank                  │                                │
│   └─────────────────┬─────────────────┘                                │
│                     │ (Creates rankings in output/)                    │
└─────────────────────▼────────────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────────────┐
│ 4️⃣ ANALYSIS & VISUALIZATION                                          │
│   ┌─────────────────────┐     ┌───────────────────────┐                │
│   │ renaissance-analyze │ ──> │ renaissance-visualize │                │
│   └─────────────────────┘     └─────────┬─────────────┘                │
│                                         │ (Creates reports & charts in output/)│
└─────────────────────────────────────────▼──────────────────────────────┘
                                          │
┌─────────────────────────────────────────▼──────────────────────────────┐
│ 5️⃣ REVIEW RESULTS & MAKE DECISIONS                                       │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Review Reports │────>│ Examine Charts│────>│ Inform Investment │    │
│   │ (Excel/CSVs)   │     │ (HTML/Images)│     │ Strategy          │    │
│   └────────────────┘     └──────────────┘     └───────────────────┘    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## Installation and Setup

### System Requirements
- **Python**: Version 3.8 or higher.
- **Git**: For cloning the repository.
- **Bloomberg Terminal**: Required only if extracting live data. Must be running and logged in.
- **Operating System**: Windows, macOS, or Linux.
- **RAM**: 4GB minimum (8GB recommended).
- **Disk Space**: ~100MB for installation, plus space for data and output files.

### Installation Steps (Recommended Method)

Follow these steps to set up the system using `pip`:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
    cd Renaissance_Stock_Ranking
    ```

2.  **Create and Activate Virtual Environment**:
    *(This isolates project dependencies)*
    ```bash
    # Windows
    python -m venv venv
    venv\\Scripts\\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
    *Remember to activate the environment each time you open a new terminal for this project.*

3.  **Install the Package**:
    *(Editable mode `-e` allows code changes without reinstalling)*
    ```bash
    pip install -e .
    ```
    This installs the core package and its required dependencies (pandas, numpy, etc.) as defined in `setup.py`.

4.  **Install Bloomberg API (If Using Live Data)**:
    *   **Ensure Bloomberg Terminal is running and logged in.**
    *   Run:
    ```bash
    pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
    ```
    *(See Troubleshooting if issues occur. You only need this step if you plan to run `renaissance-extract` without the `--test-mode` flag).*

5.  **Install Optional Dependencies (As Needed)**:
    Use the `extras_require` feature defined in `setup.py`:
    *   For visualization features (Plotly):
        ```bash
        pip install -e ".[viz]"
        ```
    *   For Jupyter notebook examples:
        ```bash
        pip install -e ".[notebook]"
        ```
    *   For running tests (Pytest):
        ```bash
        pip install -e ".[test]"
        ```
    *   To install *all* optional dependencies (excluding `blpapi`):
        ```bash
        pip install -e ".[viz,notebook,test]"
        ```

6.  **Verify Installation**:
    ```bash
    # Ensure your virtual environment is activated
    renaissance-rank --help
    ```
    This should display the help message for the ranking command.

*(Note: The previous installation methods using `requirements.txt` or the `install.sh`/`.bat` scripts are considered legacy. The `pip install -e .` method provides better dependency management based on `setup.py`).*

## Data Requirements

The system requires specific input data, typically placed in the `data/` directory (though paths can be customized via command-line options).

### 1. NIFTY 500 Constituent List (`nifty500_list.csv`)

Contains metadata about the stocks.

**Required columns:**
- `ISIN`: The International Securities Identification Number (primary key).
- `Name`: The company name.

**Optional but recommended columns:**
- `Ticker`: The Bloomberg ticker (useful for data extraction).
- `Sector`: The GICS sector classification (required for `renaissance-analyze`).

**Example format:**
```csv
ISIN,Name,Ticker,Sector
INE009A01021,Infosys Ltd,INFO:IN,Information Technology
INE062A01020,Tata Consultancy Services Ltd,TCS:IN,Information Technology
INE040A01034,HDFC Bank Ltd,HDFCB:IN,Financials
```

### 2. Historical Prices (`historical_prices.csv`)

Contains monthly closing prices.

**Required columns:**
- `ISIN`: Matches the ISIN in the constituent list.
- `Date`: The date of the price (Strictly **YYYY-MM-DD** format).
- `Price`: The adjusted closing price.

**Important notes:**
- Prices **must** be month-end closing prices.
- Prices **must** be adjusted for corporate actions (splits, dividends). Bloomberg data typically provides this.
- At least **13 months** of data is required to calculate the first 12-month return.
- All prices should be in the same currency (preferably INR).

**Example format:**
```csv
ISIN,Date,Price
INE009A01021,2022-01-31,1680.75
INE009A01021,2022-02-28,1722.30
INE062A01020,2022-01-31,3698.15
```

### 3. Financial Metrics (`financial_metrics.csv`) - Optional

Used by `renaissance-analyze` for enhanced sector analysis.

**Required column:**
- `ISIN`: Matches the ISIN in the constituent list.

**Optional metric columns (examples):**
- `PE_Ratio`: Price-to-earnings ratio
- `PB_Ratio`: Price-to-book ratio
- `ROE`: Return on equity
- `DebtToAsset`: Debt-to-asset ratio
- `DividendYield`: Dividend yield

**Example format:**
```csv
ISIN,PE_Ratio,PB_Ratio,ROE,DebtToAsset,DividendYield
INE009A01021,28.5,3.2,25.4,0.12,1.5
INE062A01020,30.2,12.5,42.8,0.05,1.2
```

### Data Source
- **Bloomberg**: The `renaissance-extract` command can automatically fetch this data if you have API access.
- **Manual**: You can prepare these files manually from other sources, ensuring the format matches the requirements.
- **Sample**: Sample files are provided in `data/sample/` for testing.

## Running the System

Ensure your virtual environment is activated before running any commands.

### Workflow Overview

The typical workflow involves running the commands in this order:

1.  **`renaissance-extract`**: Get the raw data (CSV files).
2.  **`renaissance-rank`**: Process the data and calculate rankings.
3.  **`renaissance-analyze`**: Perform sector analysis (optional).
4.  **`renaissance-visualize`**: Generate charts (optional).

### Step 1: Data Extraction (`renaissance-extract`)

This command prepares the necessary input CSV files (`nifty500_list.csv`, `historical_prices.csv`, `financial_metrics.csv`) in the specified output directory (default: `data/`).

*   **Using Live Bloomberg Data:**
    ```bash
    # Ensure Bloomberg Terminal is running and logged in
    renaissance-extract
    ```
    *Use `--output-dir <path>` to save files to a different location.*

*   **Using Test Mode (No Bloomberg Needed):**
    ```bash
    renaissance-extract --test-mode
    ```
    This generates sample data files, useful for development or testing the workflow without API access.

### Step 2: Core Ranking (`renaissance-rank`)

This command reads the CSV files from the data directory (default: `data/`), calculates returns and rankings, and saves the results (typically an Excel file like `NIFTY500_Rankings_YYYYMMDD.xlsx`) to the output directory (default: `output/`).

```bash
renaissance-rank
```

*   Use `--input-dir <path>` if your data CSVs are not in `data/`.
*   Use `--output-dir <path>` to save results to a different location.
*   Use `--generate-historical` to output historical rankings for backtesting (can be large).
*   Use `--help` for all options.

### Step 3: Sector Analysis (`renaissance-analyze`) - Optional

This command reads the ranking results and the input data (especially `nifty500_list.csv` for sector info and optionally `financial_metrics.csv`) to generate sector-level insights.

```bash
renaissance-analyze
```

*   Requires the NIFTY 500 list to contain a `Sector` column.
*   Optionally uses `financial_metrics.csv` if found.
*   Saves reports (e.g., `sector_performance.csv`, `sector_analysis_report.xlsx`) to `output/sector_analysis/` (by default).
*   Use `--rankings-file <path>`, `--nifty500-file <path>`, `--metrics-file <path>` to specify non-default input locations.
*   Use `--output-dir <path>` for results.
*   Use `--help` for all options.

### Step 4: Visualization (`renaissance-visualize`) - Optional

This command reads the ranking results and generates interactive HTML charts and potentially static images.

```bash
renaissance-visualize
```

*   Saves visualizations to `output/visualizations/` (by default).
*   Creates an `visualization_index_YYYYMMDD_HHMMSS.html` file linking to all generated charts.
*   Use `--rankings-file <path>` if rankings are not in the default location.
*   Use `--output-dir <path>` for results.
*   Use `--help` for all options.

### Alternative: Using Convenience Scripts

You can achieve the same workflow using the scripts in the `scripts/` directory:

```bash
# Activate virtual environment

# Step 1: Extract (Live Data)
python scripts/extract_bloomberg.py
# OR Extract (Test Mode)
python scripts/extract_bloomberg.py --test-mode

# Step 2: Rank
python scripts/run_ranking.py

# Step 3: Analyze Sectors
python scripts/analyze_sectors.py

# Step 4: Visualize
python scripts/visualize_results.py
```
*These scripts accept the same command-line arguments as their `renaissance-*` counterparts (e.g., `python scripts/run_ranking.py --output-dir results`).*

## Interpreting Results

The primary outputs are generated in the `output/` directory.

### 1. Ranking Results (e.g., `NIFTY500_Rankings_YYYYMMDD.xlsx`)

This Excel file typically contains multiple sheets:

*   **Latest Rankings**: Stocks ranked 1 (best) to N (worst) based on the most recent 12-month return. Includes ISIN, Name, Sector, Return, Rank.
*   **Rank Changes**: Shows the change in rank from the previous month. Includes Current Rank, Previous Rank, Rank Delta (negative delta means improvement).
*   **Monthly Returns**: Detailed monthly and calculated yearly returns for all stocks.

### 2. Sector Analysis Results (in `output/sector_analysis/`)

*   **`sector_performance.csv`**: Metrics like average return, volatility, number of stocks per sector.
*   **`sector_concentration.csv`**: Analysis of portfolio concentration within sectors.
*   **`top_stocks_by_sector.csv`**: Lists the highest-ranked stocks within each sector.
*   **`sector_analysis_report.xlsx`**: May contain a consolidated report with charts and tables.

### 3. Visualization Results (in `output/visualizations/`)

*   **`visualization_index_YYYYMMDD_HHMMSS.html`**: The main HTML file linking to all charts.
*   **Individual Chart Files (.html, .png)**: Interactive charts (usually Plotly HTML files) or static images showing:
    *   Return distributions.
    *   Top/Bottom performers.
    *   Rank change distributions.
    *   Sector performance comparisons.

### 4. Log Files (in `output/logs/`)

*   `ranking_system.log`, `bloomberg_extractor.log`, etc.: Contain detailed step-by-step information, warnings, and errors from each run. Essential for debugging.

## Extending the System

The system is designed to be modular. Key areas for extension:

*   **Analysis Modules (`renaissance/analysis/`)**: Add new analysis types (e.g., different risk metrics).
*   **Core Logic (`renaissance/core/`)**: Modify return calculations (`return_calculator.py`) or the ranking algorithm (`ranking_system.py`).
*   **Data Loaders (`renaissance/core/data_loader.py`)**: Adapt to load data from different formats or sources.
*   **Data Extraction (`renaissance/data_extraction/`)**: Add extractors for other data vendors.
*   **Visualization (`renaissance/visualization/`)**: Create new chart types.
*   **CLI (`renaissance/cli/`)**: Add new commands or options.

Remember to add corresponding tests in the `tests/` directory for any new functionality.

## Troubleshooting

### Installation Issues

*   **Problem**: `pip install -e .` fails (e.g., missing C++ compiler).
    *   **Solution**: Ensure build tools are installed. Upgrade pip (`python -m pip install --upgrade pip`). Check error logs for specifics.

*   **Problem**: `ModuleNotFoundError: No module named 'blpapi'`.
    *   **Solution 1**: Activate virtual environment (`venv\\Scripts\\activate` or `source venv/bin/activate`).
    *   **Solution 2**: Install `blpapi` correctly after activating venv:
        ```bash
        pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
        ```

*   **Problem**: `blpapi` installation fails or connection errors.
    *   **Solution 1**: **Ensure Bloomberg Terminal is running and logged in** before install/run.
    *   **Solution 2**: Check network/firewall.
    *   **Solution 3**: Consult Bloomberg API docs for OS-specific needs.

### Runtime Issues

*   **Problem**: Command `renaissance-rank` (or others) not found.
    *   **Solution 1**: Activate the correct virtual environment.
    *   **Solution 2**: Verify installation (`pip list`). Try reinstalling (`pip install --force-reinstall -e .`).

*   **Problem**: `FileNotFoundError` during `renaissance-rank` or `renaissance-analyze`.
    *   **Solution**: Ensure input CSVs exist in the correct directory (default: `data/`). Run `renaissance-extract` first. Check `--input-dir` / `--output-dir` consistency if used.

*   **Problem**: Date format errors (`ValueError: time data ... does not match format '%Y-%m-%d'`)
    *   **Solution**: Ensure all dates in `historical_prices.csv` strictly follow the **YYYY-MM-DD** format.

*   **Problem**: Insufficient data warning or errors during return calculation.
    *   **Solution**: Verify `historical_prices.csv` contains at least 13 consecutive months of data for stocks being analyzed.

*   **Problem**: Incorrect results or unexpected behavior.
    *   **Solution**: Examine log files in `output/logs/`. Verify input data format. Run `renaissance-extract --test-mode` and subsequent steps to test with known sample data.

### Getting Help

1.  Consult the detailed log files in `output/logs/`.
2.  Review the specific guides in the `docs/` directory.
3.  Ensure input data meets the format requirements.

## Quick Reference

### Command-Line Tools

| Tool                  | Description                                    | Key Options                                                                 |
| :-------------------- | :--------------------------------------------- | :-------------------------------------------------------------------------- |
| `renaissance-extract` | Fetches/generates input data CSVs            | `--output-dir`, `--test-mode`, `--start-date`, `--end-date`                 |
| `renaissance-rank`    | Calculates returns and rankings              | `--input-dir`, `--output-dir`, `--nifty500-file`, `--price-file`, `--generate-historical` |
| `renaissance-analyze` | Performs sector analysis                       | `--input-dir`, `--output-dir`, `--rankings-file`, `--nifty500-file`, `--metrics-file` |
| `renaissance-visualize` | Generates charts from ranking results        | `--output-dir`, `--rankings-file`                                           |

*Use `--help` with any command for a full list of options.*

### Script Interfaces

*   `scripts/extract_bloomberg.py` (Equivalent to `renaissance-extract`)
*   `scripts/run_ranking.py` (Equivalent to `renaissance-rank`)
*   `scripts/analyze_sectors.py` (Equivalent to `renaissance-analyze`)
*   `scripts/visualize_results.py` (Equivalent to `renaissance-visualize`)

*Scripts accept the same arguments as the CLI tools.*

### Required Data Columns

| File                    | Required Columns              | Recommended Columns |
| :---------------------- | :---------------------------- | :------------------ |
| `nifty500_list.csv`     | `ISIN`, `Name`                | `Ticker`, `Sector`  |
| `historical_prices.csv` | `ISIN`, `Date`, `Price`       |                     |
| `financial_metrics.csv` | `ISIN`                        | Metric columns      |

### Key Output Locations

| Output Type        | Default Location           |
| :----------------- | :------------------------- |
| Ranking Results    | `output/`                  |
| Sector Analysis    | `output/sector_analysis/`  |
| Visualizations     | `output/visualizations/`   |
| Logs               | `output/logs/`             | 