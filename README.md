# Renaissance Stock Ranking System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)]()
[![Bloomberg API](https://img.shields.io/badge/Bloomberg-API-yellow.svg)](https://www.bloomberg.com/professional/support/api-library/)

A comprehensive system for analyzing, ranking, and visualizing NIFTY 500 stocks based on performance metrics and sector analysis.

## Table of Contents

- [At a Glance](#at-a-glance)
- [What Problems Does It Solve?](#what-problems-does-it-solve)
- [System Workflow](#system-workflow)
- [Key Features](#key-features)
- [Project Structure](#project-structure-and-organization)
- [Input Data Requirements](#input-data-requirements)
- [Installation Guide](#installation-guide)
- [Ways to Use the System](#ways-to-use-the-system)
- [Complete Workflow Guide](#complete-workflow-guide)
- [Common Tasks Guide](#common-tasks-guide)
- [Output Files and Visualizations](#output-files-and-visualizations)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Need More Help?](#need-more-help)
- [Glossary of Terms](#glossary-of-terms)
- [GitHub Deployment](#github-deployment-instructions)
- [Author](#author)
- [License](#license)

## At a Glance

The Renaissance Stock Ranking System automates the analysis of NIFTY 500 stocks, transforming what was once a time-consuming manual process into an efficient, accurate workflow. The system calculates yearly returns on a monthly rolling basis, ranks stocks by performance, tracks rank changes, analyzes sector performance, and visualizes results through easy-to-understand charts.

```
┌────────────────────────────────────────────────┐
│                                                │
│         Renaissance Stock Ranking System       │
│                                                │
└────────────────────────┬───────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────┐   ┌────────────┐   ┌────────────┐   ┌──────────┐  │
│  │          │   │            │   │            │   │          │  │
│  │  Extract ├──►│  Calculate ├──►│    Rank    ├──►│  Analyze │  │
│  │   Data   │   │   Returns  │   │   Stocks   │   │  Results │  │
│  │          │   │            │   │            │   │          │  │
│  └──────────┘   └────────────┘   └────────────┘   └────┬─────┘  │
│                                                        │         │
│                                                        ▼         │
│  ┌──────────┐   ┌────────────┐   ┌────────────┐   ┌──────────┐  │
│  │          │   │            │   │            │   │          │  │
│  │  Make    │◄──┤  Visualize │◄──┤   Analyze  │◄──┤  Track   │  │
│  │Decisions │   │   Results  │   │   Sectors  │   │  Changes │  │
│  │          │   │            │   │            │   │          │  │
│  └──────────┘   └────────────┘   └────────────┘   └──────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## What Problems Does It Solve?

### Before: Manual Process Challenges
- ⏱️ **Time-Consuming**: Hours spent manually downloading and manipulating data
- ❌ **Error-Prone**: Manual calculations and data entry led to mistakes
- 📈 **Limited Analysis**: Difficult to expand beyond basic calculations
- 🔄 **Corporate Actions**: Tedious manual adjustments for stock splits and dividends

### After: Automated Solution Benefits
- ⚡ **Efficiency**: Processes hundreds of stocks in seconds
- ✓ **Accuracy**: Consistent, error-free calculations
- 📊 **Rich Analysis**: Advanced metrics and sector-level insights
- 🛠️ **Adjustments Handled**: Uses Bloomberg's pre-adjusted data
- 🔄 **Bloomberg Integration**: Direct API access for streamlined data extraction
- 📈 **Financial Metrics**: Automated collection of key valuation and performance metrics

## System Workflow

### Monthly Workflow Process

```
┌───────────────────────────────────────────────────────────────────────┐
│                       MONTHLY WORKFLOW DIAGRAM                         │
└───────────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼─────────────────────────────────────────┐
│ 1️⃣ EXTRACT DATA                                                        │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ NIFTY 500 List │     │ Stock Prices │     │ Financial Metrics │    │
│   │ (with sectors) │     │ (monthly)    │     │ (optional)        │    │
│   └────────┬───────┘     └───────┬──────┘     └──────────┬────────┘    │
│            │                     │                       │             │
│            └─────────────────────┼───────────────────────┘             │
│                                  │                                     │
└──────────────────────────────────▼─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 2️⃣ RUN CORE RANKING                                                    │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Calculate      │     │ Rank Stocks  │     │ Track Rank        │    │
│   │ Yearly Returns │────►│ by Returns   │────►│ Changes           │    │
│   └────────────────┘     └──────────────┘     └───────────────────┘    │
│                                                                        │
└──────────────────────────────────▼─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 3️⃣ RUN ADVANCED ANALYSIS                                               │
│   ┌────────────────────┐     ┌──────────────────┐                      │
│   │ Sector Performance │     │ Generate         │                      │
│   │ Analysis           │────►│ Visualizations   │                      │
│   └────────────────────┘     └──────────────────┘                      │
│                                                                        │
└──────────────────────────────────▼─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 4️⃣ REVIEW RESULTS                                                      │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Stock Rankings │     │ Sector Trends│     │ Performance       │    │
│   │ & Changes      │     │ & Analysis   │     │ Visualizations    │    │
│   └────────────────┘     └──────────────┘     └───────────────────┘    │
│                                                                        │
└──────────────────────────────────────────────────────────────────────────┘
```

## Key Features

- **Historical Data Analysis**: Analyzes historical monthly price data to calculate yearly returns
- **Performance Ranking**: Ranks stocks from best to worst based on calculated yearly returns
- **Rank Change Tracking**: Tracks month-to-month rank changes to identify improving or declining stocks
- **Data Visualization**: Automatically generates insightful charts and graphs from ranked data without requiring Python knowledge
- **Sector Analysis**: Analyzes stock performance by sector, identifying top-performing sectors and sector concentration metrics
- **Financial Metrics Integration**: Incorporates key financial metrics (P/E, P/B, ROE, etc.) for deeper analysis
- **Comprehensive Output**: Produces detailed CSV files with ranking results and performance metrics
- **Flexible Configuration**: Easily customizable through command-line parameters
- **Bloomberg API Integration**: Automated data extraction including sector information and financial metrics
- **Modern Package Structure**: Organized as a proper Python package for easy installation and use
- **Convenient Scripts**: Simple script interfaces for users without Python expertise
- **Test Mode**: Development and testing without requiring Bloomberg access

## Project Structure and Organization

### Package Structure Diagram
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

### Detailed File Structure
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
│   ├── logs/              # Log files from each run
│   ├── sector_analysis/   # Sector analysis outputs
│   └── visualizations/    # Visualization outputs
├── renaissance/           # Main package directory
│   ├── analysis/          # Analysis modules
│   ├── cli/               # Command-line interfaces
│   ├── core/              # Core functionality
│   ├── data_extraction/   # Data extraction modules
│   └── visualization/     # Visualization modules
├── scripts/               # Convenience scripts for users
├── tests/                 # Test scripts
├── README.md              # This file
├── setup.py               # Package installation configuration
├── pyproject.toml         # Modern Python packaging configuration
```

## Input Data Requirements

### NIFTY 500 List (`nifty500_list.csv`)
This file contains information about each stock in the NIFTY 500 index.

**Example**:
```
ISIN,Name,Ticker,Sector
INE040A01034,HDFC Bank Ltd,HDFCB,Financials
INE009A01021,Infosys Ltd,INFO,Information Technology
INE030A01027,Reliance Industries Ltd,RIL,Energy
```

**Required Columns**:
- `ISIN`: International Securities Identification Number (unique identifier)
- `Name`: Company name
- `Ticker`: Stock ticker symbol (optional)
- `Sector`: Industry sector (optional, required for sector analysis)

### Historical Prices (`historical_prices.csv`)
This file contains the monthly closing prices for each stock.

**Example**:
```
ISIN,Date,Price
INE040A01034,2023-01-31,1450.75
INE040A01034,2023-02-28,1487.25
INE009A01021,2023-01-31,1486.70
```

**Required Columns**:
- `ISIN`: International Securities Identification Number (matching the list file)
- `Date`: Date in YYYY-MM-DD format (should be month-end dates)
- `Price`: Adjusted closing price

### Financial Metrics (`financial_metrics.csv`) - Optional
This file contains additional financial metrics for each stock.

**Example**:
```
ISIN,PE_Ratio,PB_Ratio,ROE,DebtToAsset,DividendYield
INE040A01034,18.5,3.2,17.8,0.12,1.2
INE009A01021,22.1,3.8,25.4,0.03,2.5
```

The system is designed to work seamlessly with data extracted from Bloomberg, but any data source that provides the required format can be used. For detailed format specifications, see the [Data Extraction Guide](docs/data_extraction_guide.md).

## Installation Guide

Follow these steps to set up the Renaissance Stock Ranking System on your machine using the recommended `pip` installation method.

**Prerequisites:**
- **Python**: Version 3.8 or higher. Ensure Python is added to your system's PATH during installation.
- **Git**: Required to clone the repository.
- **Bloomberg Terminal**: (Required for live data extraction) Must be installed, running, and logged in *before* installing `blpapi` or running the data extraction step.

**Steps:**

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
    cd Renaissance_Stock_Ranking
    ```

2.  **Create and Activate Virtual Environment**:
    *(Recommended to isolate dependencies)*
    ```bash
    # Windows
    python -m venv venv
    venv\\Scripts\\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(Remember to activate the environment (`venv\\Scripts\\activate` or `source venv/bin/activate`) each time you open a new terminal to work on the project).*

3.  **Install the Package and Core Dependencies**:
    *(Using editable mode `-e` allows code changes without reinstalling)*
    ```bash
    pip install -e .
    ```

4.  **Install Bloomberg API (If Using Live Data)**:
    *   **Ensure Bloomberg Terminal is running and logged in.**
    *   Run the following command:
    ```bash
    pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
    ```
    *(See Troubleshooting section if issues occur).*

5.  **Install Optional Dependencies (As Needed)**:
    *   For visualization features:
        ```bash
        pip install -e ".[viz]"
        ```
    *   For Jupyter notebook examples:
        ```bash
        pip install -e ".[notebook]"
        ```
    *   For running tests:
        ```bash
        pip install -e ".[test]"
        ```
    *   For all development dependencies (includes viz, notebook, test):
        ```bash
        pip install -e ".[dev]"
        ```
    *   To install a specific combination (excluding `blpapi`):
        ```bash
        pip install -e ".[viz,notebook,test]" # Example combination
        ```

*(Note: This `pip install .` approach uses `setup.py` for robust dependency management and is preferred over using the legacy `requirements.txt` or `install.sh`/`.bat` scripts).*

## Ways to Use the System

The system offers flexibility for different users:

### 1. Using Command-Line Tools (Recommended for Regular Use)

Once installed (using `pip install -e .`), use these commands in your activated virtual environment:

*   **Extract Data**:
    *   Live Bloomberg Data: `renaissance-extract`
    *   Test/Sample Data: `renaissance-extract --test-mode`
*   **Calculate Rankings**: `renaissance-rank`
*   **Analyze Sectors**: `renaissance-analyze`
*   **Generate Visualizations**: `renaissance-visualize`

Add `--help` to any command for more options (e.g., `renaissance-rank --help`).

### 2. Using Convenience Scripts (Alternative)

If you prefer not to install the package using `pip install -e .`, you can run Python scripts directly from the `scripts/` directory (ensure the package and its dependencies, including any needed extras, have been installed first using the steps above):

*   **Extract Data**:
    *   Live Bloomberg Data: `python scripts/extract_bloomberg.py`
    *   Test/Sample Data: `python scripts/extract_bloomberg.py --test-mode`
*   **Calculate Rankings**: `python scripts/run_ranking.py`
*   **Analyze Sectors**: `python scripts/analyze_sectors.py`
*   **Generate Visualizations**: `python scripts/visualize_results.py`

*(Note: These scripts simply call the underlying command-line tools if the package is installed. The CLI tool approach is generally recommended for consistency).*

### 3. Using the Python Package API (For Developers)

Import and integrate the core modules into your own Python applications (requires package installation):
```python
# Example: Basic Ranking
from renaissance.core.data_loader import load_and_prepare_all_data
from renaissance.core.return_calculator import calculate_yearly_returns
from renaissance.core.ranking_system import rank_stocks_by_return, calculate_rank_changes

# Load sample data (adjust paths if necessary)
nifty500_df, prices_df, _ = load_and_prepare_all_data(
    nifty_file='data/sample/nifty500_list.csv',
    prices_file='data/sample/historical_prices.csv'
)

returns_df = calculate_yearly_returns(prices_df)
ranked_df = rank_stocks_by_return(returns_df)
final_df = calculate_rank_changes(ranked_df)

print(final_df.head())
```

## Complete Workflow Guide

Follow this workflow for a typical analysis cycle using the recommended command-line tools.

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

### Step 1: Installation
Follow the [Installation Guide](#installation-guide) above using the `pip install -e .` method.

### Step 2: Data Extraction
Choose the command appropriate for your setup:

*   **With Bloomberg Access:**
    ```bash
    # Activate your virtual environment first
    renaissance-extract
    ```
    This connects to the Bloomberg API and saves live data to the `data/` directory (or the directory specified with `--output-dir`).

*   **Without Bloomberg Access (Testing/Development):**
    ```bash
    # Activate your virtual environment first
    renaissance-extract --test-mode
    ```
    This generates sample data files in the `data/` directory (or specified `--output-dir`) without needing Bloomberg.

### Step 3: Run Core Ranking
Process the extracted data to calculate returns and rankings:
```bash
# Activate your virtual environment first
renaissance-rank
```
This reads data from `data/` (by default) and saves ranking results (e.g., `stock_rankings.xlsx`) to the `output/` directory (by default).

### Step 4: Advanced Analysis & Visualization

*   **Analyze Sectors:**
    ```bash
    # Activate your virtual environment first
    renaissance-analyze
    ```
    Reads rankings and generates sector analysis reports in `output/sector_analysis/`.

*   **Generate Visualizations:**
    ```bash
    # Activate your virtual environment first
    renaissance-visualize
    ```
    Reads rankings and generates charts/HTML reports in `output/visualizations/`.

### Step 5: Review Results
Examine the generated Excel files, CSVs, and visualizations in the `output/` directory to inform investment decisions.

## Common Tasks Guide

This section provides quick reference instructions for common tasks that analysts might want to perform with the system.

### Task 1: Find the Best Performing Stocks

To identify the top-performing stocks for a given month:

```bash
# Ensure you have the latest rankings by running the workflow up to step 3
renaissance-rank

# Check the latest output file in the output/ directory
# e.g., open NIFTY500_Rankings_*.xlsx in Excel and sort by 'Rank'
```

### Task 2: Identify Stocks with Improving Performance

To find stocks that have shown the biggest improvement in rankings:

```bash
# Ensure you have the latest rankings
renaissance-rank

# Check the latest output file in the output/ directory
# e.g., open NIFTY500_Rankings_*.xlsx and sort by 'Rank_Change' (ascending)
```

### Task 3: Analyze Sector Performance Trends

To understand which sectors are performing well:

```bash
# Run the sector analysis
renaissance-analyze

# View the sector performance report in output/sector_analysis/
# e.g., open sector_analysis_report.xlsx or sector_performance.csv
```

### Task 4: Create a Monthly Report with Visualizations

To generate a full set of visualizations for monthly reports:

```bash
# Ensure rankings are up-to-date
renaissance-rank

# Generate visualizations
renaissance-visualize

# The visualizations will be saved in output/visualizations/
# including an index HTML file for easy navigation.
```

### Task 5: Perform a Custom Analysis on Specific Sectors

For a targeted analysis, use the Python API as shown in the [Ways to Use the System](#3-using-the-python-package-api-for-developers) section, modifying the filtering logic as needed.

### Task 6: Update Data for a New Month

To update your data at the start of a new month:

```bash
# Activate your virtual environment
# If you have Bloomberg access:
renaissance-extract

# If you don't have Bloomberg access (for testing):
renaissance-extract --test-mode

# After extraction, re-run the ranking and analysis steps:
renaissance-rank
renaissance-analyze
renaissance-visualize
```

### Task 7: Generate a Comprehensive Sector Allocation Strategy

*(Note: A dedicated script `generate_sector_strategy.py` was mentioned previously but may not exist. This task involves manual interpretation of the analysis results)*

1.  Run the full workflow (`extract`, `rank`, `analyze`).
2.  Review the outputs in `output/` and `output/sector_analysis/`.
3.  Use the sector performance data (`sector_performance.csv`) and stock rankings (`NIFTY500_Rankings_*.xlsx`) to inform your allocation decisions based on your investment criteria (e.g., top stocks from top sectors, diversification rules).

## Output Files and Visualizations

### Output Files

The system generates several output files, typically within the `output/` directory:

1.  **Stock Rankings (`NIFTY500_Rankings_YYYYMMDD.xlsx` or similar)**:
    *   Contains sheets for detailed rankings, returns, and rank changes.
    *   Stocks ranked by yearly returns for the most recent month.
    *   Includes rank changes from the previous month.

2.  **Sector Analysis Files (in `output/sector_analysis/`)**:
    *   `sector_performance.csv`: Average returns, volatility, etc., per sector.
    *   `sector_concentration.csv`: Metrics on portfolio concentration within sectors.
    *   `sector_analysis_report.xlsx` (Optional): Consolidated report.

3.  **Log Files (in `output/logs/`)**:
    *   Detailed logs from each run (`ranking_system.log`, `bloomberg_extractor.log`, etc.). Useful for debugging.

### Visualization Outputs

Visualizations are saved in `output/visualizations/`:

#### HTML Index File
The main entry point is `visualization_index_YYYYMMDD_HHMMSS.html`. This file provides:
- An organized overview of all generated visualizations.
- Explanations for interpreting each chart.
- Links to individual visualization files (HTML or image formats).

#### Types of Visualizations (Examples)
1.  **Distribution Charts**: Return Distribution, Rank Delta Distribution.
2.  **Performance Charts**: Top/Bottom Performers, Return by Quartile.
3.  **Change Analysis Charts**: Top Improvers/Decliners, Return vs. Rank Scatter.
4.  **Sector Charts**: Sector Average Returns, Sector vs. Index Performance.

> **Note**: Example visualization outputs can be found in the `docs/img/` directory after running the system once. These provide a preview of the actual charts and reports you'll generate.

#### Data Export Files
CSV files containing the data used for specific charts might also be exported here (e.g., `top_performers_data.csv`).

#### Interpreting Visualizations
Refer to the HTML index file or the [User Guide](docs/user_guide.md) for guidance on interpreting the generated charts.

## Troubleshooting Guide

### Installation Issues

*   **Problem**: `pip install -e .` fails with errors related to building wheels (e.g., missing C++ compiler).
    *   **Solution**: Ensure you have the necessary build tools for your OS. For some packages (like `numpy`, `pandas`), installing pre-built wheels is usually preferred. Check error messages for specific package issues. Using a recent version of `pip` might help (`python -m pip install --upgrade pip`).

*   **Problem**: `ModuleNotFoundError: No module named 'blpapi'` when running commands.
    *   **Solution 1**: Ensure you have activated your virtual environment (`venv\\Scripts\\activate` or `source venv/bin/activate`).
    *   **Solution 2**: Verify `blpapi` was installed correctly using the Bloomberg index URL *after* activating the venv:
        ```bash
        pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
        ```
        *Note: If the above URL doesn't work, try `https://bloomberg.bintray.com/pip/simple/` as an alternative.*

*   **Problem**: `blpapi` installation fails or connection errors occur during `renaissance-extract`.
    *   **Solution 1**: **Crucially, ensure the Bloomberg Terminal application is running and you are logged in** *before* running the `pip install blpapi` command or the `renaissance-extract` command.
    *   **Solution 2**: Check network connectivity to Bloomberg services. Firewalls might block the connection.
    *   **Solution 3**: Refer to the official Bloomberg API documentation for platform-specific troubleshooting (e.g., environment variables like `BLPAPI_ROOT`, required C++ redistributables on Windows).

### Runtime Issues

*   **Problem**: Command `renaissance-rank` (or other `renaissance-*` commands) not found.
    *   **Solution 1**: Ensure you have activated your virtual environment where the package was installed.
    *   **Solution 2**: Verify the package was installed correctly using `pip install -e .`. Check `pip list` for `renaissance-stock-ranking`. If installed, try reinstalling with `pip install --force-reinstall -e .`.

*   **Problem**: `FileNotFoundError` when running `renaissance-rank` or `renaissance-analyze`.
    *   **Solution**: Make sure the required input files (e.g., `historical_prices.csv`, `nifty500_list.csv`) exist in the expected input directory (default: `data/`). Run `renaissance-extract` first. If you used `--output-dir` during extraction, you might need to specify the same directory using `--input-dir` (or equivalent options, check `--help`) for the ranking/analysis commands.

*   **Problem**: Incorrect results or unexpected behavior.
    *   **Solution**: Check the log files in `output/logs/` for detailed error messages or warnings. Ensure input data format matches the requirements documented. Use `--test-mode` with `renaissance-extract` to run with known sample data for comparison.

## Need More Help?

- **Detailed User Guide**: See [User Guide](docs/user_guide.md)
- **Bloomberg Data Extraction**: See [Data Extraction Guide](docs/data_extraction_guide.md)
- **Bloomberg API Integration**: See [Bloomberg API Guide](docs/bloomberg_api_guide.md) for automated data collection
- **Sector Analysis**: See [Sector Analysis Guide](docs/README_sector_analysis.md)
- **Code Examples**: See [Example Notebook](examples/example_usage.ipynb)

## Glossary of Terms

Here's a quick reference for technical terms used in this documentation:

- **CSV**: Comma-Separated Values file - a simple text format that stores tabular data with commas between values
- **ISIN**: International Securities Identification Number - a 12-character alphanumeric code that uniquely identifies a specific security
- **Terminal Command/Command Line**: A text-based interface to control your computer by typing commands
- **Virtual Environment**: An isolated Python environment that allows packages to be installed for use by a particular project only
- **Repository**: A storage location for software packages, typically used with version control systems like Git
- **Dependencies**: External software packages that your project relies on to function
- **Script**: A file containing Python code that can be executed
- **Module**: A Python file containing definitions and statements that can be imported and used in other Python files
- **Package**: A collection of Python modules. This project is structured as an installable package.
- **CLI (Command-Line Interface)**: Refers to the `renaissance-*` commands accessible after installation.
- **Entry Point**: A way for an installed package to expose commands directly in the terminal (e.g., `renaissance-rank`).
- **Extras**: Optional sets of dependencies that can be installed for specific features (e.g., `[viz]`, `[notebook]`).

## GitHub Deployment Instructions

If you need to deploy this project to your own GitHub repository:

1. Create a new repository on GitHub.
2. Initialize the local repository (if not already done):
   ```bash
   # Only run git init if you haven't already
   # git init
   git add .
   git commit -m "Initial commit"
   ```
3. Add your GitHub repository as remote and push:
   ```bash
   # Replace with your actual repo URL
   git remote add origin https://github.com/your-username/your-repo-name.git
   # Ensure your default branch is named 'main' or adjust as needed
   git branch -M main
   git push -u origin main
   ```

## Author
mathamphetamine

## License
Proprietary - For use at Renaissance Investment Managers only

