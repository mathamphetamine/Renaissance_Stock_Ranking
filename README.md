# Renaissance Stock Ranking System

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
├── install.sh             # Installation script for macOS/Linux
├── install.bat            # Installation script for Windows
├── README.md              # This file
├── setup.py               # Package installation configuration
├── pyproject.toml         # Modern Python packaging configuration
└── requirements.txt       # Python dependencies
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

### Quick Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Renaissance_Stock_Ranking.git
   cd Renaissance_Stock_Ranking
   ```

2. **Run the installation script**:
   - Windows: `install.bat`
   - Mac/Linux: `./install.sh`

### Detailed Installation for Different User Types

#### For Users Familiar with Python and Command-Line:

**Windows:**
```bash
git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
cd Renaissance_Stock_Ranking
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Optional: Install as editable package
pip install -e .
```

**Mac/Linux:**
```bash
git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
cd Renaissance_Stock_Ranking
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Optional: Install as editable package
pip install -e .
```

#### For Users Less Familiar with Python (Simplified):

**Windows Installation:**
1. **Install Python**:
   - Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Click "Install Now"

2. **Get the Stock Ranking System**:
   - Download the ZIP file of this project from GitHub
   - Extract the ZIP file to a folder on your computer

3. **Open Command Prompt**:
   - Press Windows+R, type "cmd" and press Enter
   - Navigate to the project folder:
     ```
     cd path\to\Renaissance_Stock_Ranking
     ```

4. **Set Up the System**:
   - Create a virtual environment (one-time setup):
     ```
     python -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     ```

5. **Use the System**:
   - Place your data files in the "data" folder
   - Run the system using the scripts in the "scripts" folder

**Mac/Linux Installation:**
1. **Install Python** (if not already installed):
   - Mac: Install Homebrew, then run `brew install python3`
   - Linux: Use package manager, e.g., `sudo apt install python3`

2. **Get the Stock Ranking System**:
   - Download the ZIP file from GitHub
   - Extract to your preferred location

3. **Open Terminal**:
   - Navigate to the project folder:
     ```
     cd path/to/Renaissance_Stock_Ranking
     ```

4. **Set Up the System**:
   - Create a virtual environment (one-time setup):
     ```
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

5. **Use the System**:
   - Place your data files in the "data" folder
   - Run the system using the scripts in the "scripts" folder

## Ways to Use the System

The system is designed to be flexible and can be used in multiple ways:

### 1. For Investment Analysts: Easy Scripts
Simple scripts in the `scripts/` directory can be run with minimal technical knowledge:
```bash
python scripts/run_ranking.py
python scripts/visualize_results.py
python scripts/analyze_sectors.py
python scripts/extract_bloomberg.py  # If you have Bloomberg access
```

### 2. For Technical Users: Command-Line Tools
After installation, use these commands from anywhere:
```bash
renaissance-rank
renaissance-visualize
renaissance-analyze
renaissance-extract
```

### 3. For Developers: Python Package API
Import and use in your own Python code:
```python
from renaissance.core.data_loader import load_and_prepare_all_data
from renaissance.core.return_calculator import calculate_yearly_returns
from renaissance.core.ranking_system import rank_stocks_by_return

# Load data and rank stocks
nifty500_df, prices_df = load_and_prepare_all_data('data/nifty500_list.csv', 'data/historical_prices.csv')
returns_df = calculate_yearly_returns(prices_df)
ranked_df = rank_stocks_by_return(returns_df)
```

## Complete Workflow Guide

This section walks you through the entire process from installation to portfolio construction.

```
┌───────────────────────────────────────────────────────────────────────┐
│                       COMPLETE WORKFLOW DIAGRAM                        │
└───────────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼─────────────────────────────────────────┐
│ 1️⃣ INSTALLATION                                                        │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Clone Repo     │────>│ Run Install  │────>│ Verify            │    │
│   │ from GitHub    │     │ Script       │     │ Installation      │    │
│   └────────────────┘     └──────────────┘     └──────────┬────────┘    │
│                                                          │             │
└──────────────────────────────────────────────────────────▼─────────────┘
                                                           │
┌──────────────────────────────────────────────────────────▼─────────────┐
│ 2️⃣ DATA COLLECTION                                                     │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Extract NIFTY  │────>│ Extract Stock│────>│ (Optional)        │    │
│   │ 500 List       │     │ Price History│     │ Financial Metrics │    │
│   └────────────────┘     └──────────────┘     └──────────┬────────┘    │
│                                                          │             │
└──────────────────────────────────────────────────────────▼─────────────┘
                                                           │
┌──────────────────────────────────────────────────────────▼─────────────┐
│ 3️⃣ CORE RANKING PROCESS                                                │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Calculate      │────>│ Rank Stocks  │────>│ Calculate Rank    │    │
│   │ Yearly Returns │     │ by Returns   │     │ Changes           │    │
│   └────────────────┘     └──────────────┘     └──────────┬────────┘    │
│                                                          │             │
└──────────────────────────────────────────────────────────▼─────────────┘
                                                           │
┌──────────────────────────────────────────────────────────▼─────────────┐
│ 4️⃣ ADVANCED ANALYSIS                                                   │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Generate       │     │ Analyze      │     │ Create            │    │
│   │ Visualizations │     │ Sectors      │     │ Summary Reports   │    │
│   └───────┬────────┘     └──────┬───────┘     └──────────┬────────┘    │
│           │                     │                        │             │
│           └─────────────────────┼────────────────────────┘             │
│                                 │                                      │
└─────────────────────────────────▼──────────────────────────────────────┘
                                  │
┌─────────────────────────────────▼──────────────────────────────────────┐
│ 5️⃣ PORTFOLIO CONSTRUCTION                                              │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Identify Top   │────>│ Select Best  │────>│ Balance with      │    │
│   │ Sectors        │     │ Stocks       │     │ Financial Metrics │    │
│   └────────────────┘     └──────────────┘     └───────────────────┘    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Installation

Choose the method that works best for you:

#### Using the Installation Scripts (Recommended)

On Windows:
```bash
git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
cd Renaissance_Stock_Ranking
install.bat
```

On macOS/Linux:
```bash
git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
cd Renaissance_Stock_Ranking
./install.sh
```

Verify your installation:
```bash
renaissance-rank --test-mode
```

### Step 2: Data Collection

You have three options for data collection:

#### Option A: Use the Bloomberg API (Automated, Requires Bloomberg Terminal)
```bash
# Extract all necessary data using the Bloomberg API
python scripts/extract_bloomberg.py
```

This option:
- Automatically extracts NIFTY 500 constituents with sector information
- Retrieves historical monthly prices with corporate action adjustments
- Collects key financial metrics for deeper analysis
- Saves all data in the required format

For detailed instructions on setting up and using the Bloomberg API, see the [Bloomberg API Guide](docs/bloomberg_api_guide.md).

#### Option B: Manual Extraction (Requires Bloomberg Terminal)
Follow the detailed steps in [Data Extraction Guide](docs/data_extraction_guide.md) to:
1. Extract NIFTY 500 constituent list with ISINs
2. Extract historical monthly prices
3. (Optional) Extract financial metrics
4. Save them as CSV files in the data directory

#### Option C: Use Sample Data (For Testing)
```bash
# Copy sample data to the data directory
cp data/sample/* data/
```

### Step 3: Run the Core Ranking Process

```bash
# Run the main ranking system
python scripts/run_ranking.py
```

This will:
- Load the NIFTY 500 list and historical prices
- Calculate 12-month returns for each stock
- Rank stocks based on these returns
- Calculate rank changes from the previous month
- Generate output files in the `output/` directory

### Step 4: Advanced Analysis

#### Generate Visualizations
```bash
# Create charts and graphs from the ranking results
python scripts/visualize_results.py
```

This creates several visualizations in `output/visualizations/`:
- Return distribution charts
- Top and bottom performers
- Rank change distribution
- And more

#### Perform Sector Analysis
```bash
# Analyze performance by sector
python scripts/analyze_sectors.py
```

This generates sector-level insights in `output/sector_analysis/`:
- Sector performance rankings
- Sector concentration analysis
- Top stocks by sector
- Investment recommendations based on sector performance

### Step 5: Portfolio Construction

Using the outputs from the previous steps, you can construct a portfolio:

1. **Identify top-performing sectors** from `sector_performance.csv`
2. **Select the highest-ranked stocks** from these sectors using `NIFTY500_Rankings_*.csv`
3. **Consider sector concentration** to ensure diversification
4. **Use financial metrics** to fine-tune stock selection (if available)

Example portfolio construction approach:
```python
# Example Python code (you can run this in a Jupyter notebook)
import pandas as pd

# Load sector performance data
sector_perf = pd.read_csv('output/sector_analysis/sector_performance.csv')

# Identify top 3 sectors
top_sectors = sector_perf.sort_values('Avg_Return', ascending=False).head(3)['Sector'].tolist()

# Load stock rankings
rankings = pd.read_csv('output/NIFTY500_Rankings_YYYYMMDD.csv')  # Replace with actual filename

# Get top 5 stocks from each top sector
portfolio = []
for sector in top_sectors:
    sector_stocks = rankings[rankings['Sector'] == sector].sort_values('Rank').head(5)
    portfolio.append(sector_stocks)

# Combine into final portfolio
final_portfolio = pd.concat(portfolio)
print("Portfolio of top 15 stocks from top 3 sectors:")
print(final_portfolio[['Name', 'Sector', 'Yearly_Return', 'Rank']])
```

## Common Tasks Guide

This section provides quick reference instructions for common tasks that analysts might want to perform with the system.

### Task 1: Find the Best Performing Stocks

To identify the top-performing stocks for a given month:

```bash
# Ensure you have the latest rankings
python scripts/run_ranking.py

# View the top 10 stocks (stocks are ranked from 1 to 500)
head -n 11 output/NIFTY500_Rankings_*.csv
```

### Task 2: Identify Stocks with Improving Performance

To find stocks that have shown the biggest improvement in rankings:

```bash
# Run the ranking system to calculate rank changes
python scripts/run_ranking.py

# Sort by rank delta (negative values mean improvement)
sort -t, -k6n output/NIFTY500_RankDelta_*.csv | head -n 10
```

### Task 3: Analyze Sector Performance Trends

To understand which sectors are performing well:

```bash
# Run the sector analysis
python scripts/analyze_sectors.py

# View the sector performance report
cat output/sector_analysis/sector_analysis_report.txt

# Or open the sector performance CSV for more detailed metrics
cat output/sector_analysis/sector_performance.csv
```

### Task 4: Create a Monthly Report with Visualizations

To generate a full set of visualizations for monthly reports:

```bash
# Run the core ranking
python scripts/run_ranking.py

# Generate visualizations
python scripts/visualize_results.py

# Create a directory for this month's report
mkdir -p reports/$(date +%Y-%m)

# Copy all the output files and visualizations to the report directory
cp output/NIFTY500_Rankings_*.csv reports/$(date +%Y-%m)/
cp output/NIFTY500_RankDelta_*.csv reports/$(date +%Y-%m)/
cp -r output/visualizations/* reports/$(date +%Y-%m)/
```

### Task 5: Perform a Custom Analysis on Specific Sectors

For a targeted analysis of specific sectors (e.g., Technology and Financials):

```python
# Python code example
from renaissance.core.data_loader import load_and_prepare_all_data
from renaissance.core.return_calculator import calculate_yearly_returns
import pandas as pd

# Load data
nifty500_df, prices_df = load_and_prepare_all_data('data/nifty500_list.csv', 'data/historical_prices.csv')

# Calculate returns for all stocks
returns_df = calculate_yearly_returns(prices_df)

# Merge with sector information
merged_df = pd.merge(returns_df, nifty500_df[['ISIN', 'Sector']], on='ISIN')

# Filter for specific sectors
target_sectors = ['Information Technology', 'Financials']
filtered_df = merged_df[merged_df['Sector'].isin(target_sectors)]

# Calculate average returns by sector and date
sector_returns = filtered_df.groupby(['Date', 'Sector'])['YearlyReturn'].mean().reset_index()

# Compare sector performance over time
pivot_df = sector_returns.pivot(index='Date', columns='Sector', values='YearlyReturn')
print(pivot_df.tail(12))  # Last 12 months of data
```

### Task 6: Update Data for a New Month

To update your data at the start of a new month:

```bash
# If you have Bloomberg access, use the Bloomberg extractor
python scripts/extract_bloomberg.py

# Otherwise, follow the manual extraction process
# 1. Use Bloomberg Terminal to export new data following docs/data_extraction_guide.md
# 2. Place updated files in the data directory
# 3. Run the ranking process with the new data
python scripts/run_ranking.py
```

### Task 7: Generate a Comprehensive Sector Allocation Strategy

To develop a complete sector allocation strategy based on performance:

```bash
# Run all the necessary analyses
python scripts/run_ranking.py
python scripts/analyze_sectors.py

# Run the sector allocation strategy generator
python scripts/generate_sector_strategy.py --output-file strategies/sector_allocation_$(date +%Y%m).pdf
```

## Output Files and Visualizations

### Output Files

The system generates several output files:

1. **Stock Rankings (`NIFTY500_Rankings_YYYYMMDD.csv`)**
   - Stocks ranked by yearly returns for the most recent month.

2. **Rank Changes (`NIFTY500_RankDelta_YYYYMMDD.csv`)**
   - How each stock's rank has changed from the previous month.

3. **Summary Report (`NIFTY500_Ranking_Summary_YYYYMMDD_HHMMSS.txt`)**
   - Text summary of key statistics from the ranking process.

4. **Sector Analysis Files (in `output/sector_analysis/`)**
   - Sector performance rankings
   - Sector concentration analysis
   - Top stocks by sector
   - Investment recommendations based on sector performance

### Visualization Outputs

The system generates several types of visualization outputs to help analyze the stock rankings and performance:

#### HTML Index File

The main entry point for visualizations is an HTML index file located at `output/visualizations/visualization_index_YYYYMMDD_HHMMSS.html`. This file provides:

- An organized overview of all generated visualizations
- Detailed explanations for interpreting each chart
- Navigation to individual visualization files

#### Types of Visualizations

1. **Distribution Charts**
   - **Return Distribution**: Shows how stock returns are distributed across the NIFTY 500
   - **Rank Delta Distribution**: Displays how ranking changes are distributed

2. **Performance Charts**
   - **Top Performers**: Highlights the top 10-20 stocks with highest returns
   - **Bottom Performers**: Shows the worst-performing stocks
   - **Return by Quartile**: Compares returns across different performance quartiles

3. **Change Analysis Charts**
   - **Top Improvers**: Stocks with the biggest positive rank changes
   - **Top Decliners**: Stocks with the biggest negative rank changes
   - **Return vs. Rank Scatter**: Visualizes the relationship between returns and rankings

#### Data Export Files

Along with the visualizations, the system exports CSV files with the underlying data:
- `top_performers_YYYYMMDD_HHMMSS.csv`: Detailed data on top-performing stocks
- `top_improvers_YYYYMMDD_HHMMSS.csv`: Stocks with the biggest ranking improvements
- `top_decliners_YYYYMMDD_HHMMSS.csv`: Stocks with the biggest ranking declines

#### Interpreting Visualizations

Each chart in the visualization suite is designed to provide insights:

- **Return Distribution**: Look for whether returns are normally distributed or skewed
- **Top/Bottom Performers**: Identify outliers and extreme performers
- **Rank Changes**: Spot momentum shifts and trending stocks
- **Sector Analysis Charts**: Understand sector rotation and relative performance

For detailed examples of how to interpret these visualizations, refer to the HTML index file or the [User Guide](docs/user_guide.md).

## Troubleshooting Guide

### Installation Issues

#### Problem: Package installation fails
**Solution**: Try using a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Problem: "Module not found" errors
**Solution**: Make sure you've installed in development mode:
```bash
pip install -e .
```

### Data Issues

#### Problem: "File not found" errors
**Solution**: Ensure data files are in the correct location:
```bash
# Check if files exist
ls -la data/
```

#### Problem: Missing columns in CSV files
**Solution**: Verify your files have the required columns:
```bash
# View the first few lines of your files
head -n 5 data/nifty500_list.csv
head -n 5 data/historical_prices.csv
```

#### Problem: Empty or incomplete results
**Solution**: Ensure you have at least 13 months of price data to calculate yearly returns.

### Code Issues

#### Problem: "Logger is not defined" error
```
renaissance.cli.main - ERROR - Input data validation failed: name 'logger' is not defined
```

**Solution**: This occurs when the logger isn't properly initialized in the validate_input_data function. The system has been updated to handle this, but if you encounter this issue:

1. Make sure you're using the latest version from GitHub
2. Check that the `validate_input_data` function in `renaissance/cli/main.py` includes the logger parameter and proper initialization:
   ```python
   def validate_input_data(nifty500_file: str, price_file: str, logger=None) -> bool:
       # Initialize logger if not provided
       if logger is None:
           logger = logging.getLogger(__name__)
   ```
3. Update the call to validate_input_data in the main function to pass the logger parameter

#### Problem: Missing output directories
**Solution**: The system should create output directories automatically, but you can manually create them:
```bash
mkdir -p output/visualizations output/sector_analysis output/logs
```

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
   git remote add origin https://github.com/your-username/Renaissance_Stock_Ranking.git
   git branch -M main
   git push -u origin main
   ```

## Author
Renaissance Investment Managers

## License
Proprietary - For use at Renaissance Investment Managers only

