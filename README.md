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

## Key Features

- **Monthly Rolling Year Returns**: Calculates yearly returns on a rolling monthly basis
- **Performance Ranking**: Ranks stocks based on yearly returns
- **Rank Tracking**: Monitors how stock rankings change over time
- **Sector Analysis**: Analyzes performance by sector and identifies sector-level trends
- **Visual Reports**: Generates insightful charts and graphs for better understanding
- **Trend Identification**: Spots emerging winners and declining stocks
- **Bloomberg API Integration**: Automatically extracts data from Bloomberg (optional)
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

## Installation Guide

This section provides instructions for installing the Renaissance Stock Ranking System on different platforms.

### Quick Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Renaissance_Stock_Ranking.git
   cd Renaissance_Stock_Ranking
   ```

2. **Run the installation script**:
   - Windows: `install.bat`
   - Mac/Linux: `./install.sh`

### Detailed Installation

#### Windows Installation
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

#### Mac/Linux Installation
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
└──────────────────────────────────────────────────────────┼─────────────┘
                                                           │
┌──────────────────────────────────────────────────────────▼─────────────┐
│ 2️⃣ DATA EXTRACTION (IF USING BLOOMBERG)                                │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Extract NIFTY  │────>│ Extract      │────>│ Extract Financial │    │
│   │ 500 List       │     │ Price Data   │     │ Metrics           │    │
│   └────────────────┘     └──────────────┘     └──────────┬────────┘    │
│                                                          │             │
└──────────────────────────────────────────────────────────┼─────────────┘
                                                           │
┌──────────────────────────────────────────────────────────▼─────────────┐
│ 3️⃣ CORE RANKING PROCESS                                                │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Run Ranking    │────>│ Generate     │────>│ Analyze Ranking   │    │
│   │ Algorithm      │     │ Outputs      │     │ Results           │    │
│   └────────────────┘     └──────────────┘     └──────────┬────────┘    │
│                                                          │             │
└──────────────────────────────────────────────────────────┼─────────────┘
                                                           │
┌──────────────────────────────────────────────────────────▼─────────────┐
│ 4️⃣ VISUALIZATION & ANALYSIS                                            │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Generate       │────>│ Analyze      │────>│ Create Reports    │    │
│   │ Visualizations │     │ Sectors      │     │ & Presentations   │    │
│   └────────────────┘     └──────────────┘     └──────────┬────────┘    │
│                                                          │             │
└──────────────────────────────────────────────────────────┼─────────────┘
                                                           │
┌──────────────────────────────────────────────────────────▼─────────────┐
│ 5️⃣ PORTFOLIO CONSTRUCTION                                              │
│   ┌────────────────┐     ┌──────────────┐     ┌───────────────────┐    │
│   │ Select Top     │────>│ Apply Other  │────>│ Finalize          │    │
│   │ Ranked Stocks  │     │ Criteria     │     │ Portfolio         │    │
│   └────────────────┘     └──────────────┘     └───────────────────┘    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Data Extraction

If you have Bloomberg Terminal access, use the data extraction module:
```bash
python scripts/extract_bloomberg.py
```

Or use the provided sample data for testing.

### Step 2: Running the Core Ranking System

Process the data to rank stocks:
```bash
python scripts/run_ranking.py
```

This generates:
- Ranking outputs in the `output/` directory
- Rank change analysis
- Summary statistics

### Step 3: Generating Visualizations

Create charts and graphs:
```bash
python scripts/visualize_results.py
```

This produces:
- Return distribution charts
- Top/bottom performer charts
- Rank change visualizations
- An HTML index with explanations

### Step 4: Analyzing Sectors

Analyze performance by sector:
```bash
python scripts/analyze_sectors.py
```

This creates:
- Sector performance statistics
- Concentration analysis
- Top stocks by sector

### Step 5: Portfolio Construction

Use the results to construct a portfolio:
1. Start with top-ranked stocks
2. Apply sector diversification
3. Consider other financial metrics
4. Apply risk management guidelines

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

## Input Data Requirements

The system requires specific CSV file formats for input data:

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

## Output Files and Visualizations

### Ranking Output Files

The system generates several output files:

1. **Stock Rankings (`NIFTY500_Rankings_YYYYMMDD.csv`)**
   - Stocks ranked by yearly returns for the most recent month.

2. **Rank Changes (`NIFTY500_RankDelta_YYYYMMDD.csv`)**
   - How each stock's rank has changed from the previous month.

3. **Summary Report (`NIFTY500_Ranking_Summary_YYYYMMDD_HHMMSS.txt`)**
   - Text summary of key statistics from the ranking process.

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

### Sector Analysis Files

The system also generates sector analysis files in the `output/sector_analysis/` directory:

4. **Sector Performance (`sector_performance.csv`)**
   - Performance metrics for each sector.

5. **Sector Concentration (`sector_concentration.csv`)**
   - Analysis of concentration within each sector.

6. **Top Stocks by Sector (`top_stocks_by_sector.txt`)**
   - Report showing the top-performing stocks in each sector.

## Common Tasks Guide

### Task: Running a Quick Analysis with Sample Data
```bash
# Run the ranking system with sample data
python scripts/run_ranking.py --nifty500-file data/sample/nifty500_list.csv --price-file data/sample/historical_prices.csv

# Generate visualizations
python scripts/visualize_results.py

# Analyze sectors
python scripts/analyze_sectors.py
```

### Task: Setting Up for Bloomberg Data
```bash
# Extract data from Bloomberg (requires Bloomberg Terminal)
python scripts/extract_bloomberg.py

# Verify the extracted data
ls -la data/
```

### Task: Customizing the Analysis
```bash
# Get help on command options
python scripts/run_ranking.py --help

# Run with custom parameters
python scripts/run_ranking.py --nifty500-file your_list.csv --price-file your_prices.csv --output-dir custom_output
```

### Task: Generating Monthly Reports
```bash
# Extract fresh data
python scripts/extract_bloomberg.py

# Run the complete analysis suite
python scripts/run_ranking.py
python scripts/visualize_results.py
python scripts/analyze_sectors.py

# The output files can now be used for monthly reporting
ls -la output/
```

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

