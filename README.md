# Automated Stock Ranking System for Renaissance Investment Managers

## Project Overview
This project implements an automated stock ranking system for Renaissance Investment Managers. The system is designed to replace a manual process of collecting and analyzing stock data with an efficient Python-based solution. It automates the calculation of yearly returns for NIFTY 500 stocks on a monthly rolling basis, ranks stocks based on these returns, and analyzes rank changes month-over-month.

```
┌───────────────────────────────────────────────────────────┐
│                                                             │
│                 Renaissance Stock Ranking System            │
│                                                             │
└─────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Bloomberg     │     │ CSV Files     │     │ Data          │
│ Terminal      │────>│ - NIFTY 500   │────>│ Loader        │
│ (Data Source) │     │ - Prices      │     │               │
└───────────────┘     └───────────────┘     └───────┬───────┘
                                                    │
                                                    ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Output        │     │ Rank Delta    │     │ Return        │
│ Generator     │<────│ Calculator    │<────│ Calculator    │
│               │     │               │     │               │
└───────┬───────┘     └───────┬───────┘     └───────────────┘
        │                     │
        │                     ▼
        │             ┌───────────────┐
        │             │ Ranking       │
        │             │ System        │
        │             │               │
        │             └───────┬───────┘
        │                     │
        ▼                     │
┌───────────────┐             │
│ Output Files  │<────────────┘
│ - Rankings    │
│ - Rank Delta  │
│ - Summary     │
└───────────────┘
```

## Problem Statement
Previously, Renaissance Investment Managers relied on a manual process for:
- Downloading historical month-end closing prices from various sources
- Maintaining this data in Excel spreadsheets
- Performing calculations manually
- Manually adjusting historical data for corporate actions (splits, dividends, etc.)

This manual approach had several drawbacks:
- **Time inefficiency**: Hours spent on data collection and manipulation
- **Data inaccuracy risks**: Manual entry and calculation errors
- **Scalability issues**: Difficult to expand analysis to more stocks or metrics
- **Complex corporate action handling**: Tedious, error-prone adjustments for stock splits, dividends, etc.

## Solution
This Python-based system addresses these issues by:
- Automating the loading and processing of data extracted from Bloomberg Terminal
- Handling calculations programmatically with high accuracy
- Using ISINs for robust security identification (immune to ticker changes)
- Supporting corporate action adjusted data (leveraging Bloomberg's automatic adjustments)
- Generating clear, structured outputs for easy interpretation

## Key Features
- **Historical Data Analysis**: Analyzes historical monthly price data to calculate yearly returns
- **Performance Ranking**: Ranks stocks from best to worst based on calculated yearly returns
- **Rank Change Tracking**: Tracks month-to-month rank changes to identify improving or declining stocks
- **Data Visualization**: Automatically generates insightful charts and graphs from ranked data without requiring Python knowledge
- **Sector Analysis**: Analyzes stock performance by sector, identifying top-performing sectors and sector concentration metrics
- **Financial Metrics Integration**: Incorporates key financial metrics (P/E, P/B, ROE, etc.) for deeper analysis
- **Comprehensive Output**: Produces detailed CSV files with ranking results and performance metrics
- **Flexible Configuration**: Easily customizable through command-line parameters
- **Bloomberg API Integration**: Optional automated data extraction including sector information and financial metrics
- **Modern Package Structure**: Organized as a proper Python package for easy installation and use

## Project Structure
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
│   ├── sector_analysis/   # Sector analysis outputs (created when run)
│   └── visualizations/    # Visualization outputs (created when run)
├── renaissance/           # Main package directory
│   ├── analysis/          # Analysis modules
│   │   └── sector_analysis.py    # Sector analysis functionality
│   ├── cli/               # Command-line interfaces
│   │   ├── main.py                # Main entry point
│   │   ├── analyze.py             # Sector analysis CLI
│   │   ├── visualize.py           # Visualization CLI
│   │   └── extract.py             # Bloomberg extraction CLI
│   ├── core/              # Core functionality
│   │   ├── data_loader.py          # Data loading functions
│   │   ├── return_calculator.py    # Return calculation functions
│   │   ├── ranking_system.py       # Ranking functions
│   │   ├── rank_delta_calculator.py # Rank change functions
│   │   └── output_generator.py     # Output generation functions
│   ├── data_extraction/   # Data extraction modules
│   │   └── bloomberg_data_extractor.py # Bloomberg API integration
│   └── visualization/     # Visualization modules
│       └── visualize.py           # Visualization functions
├── scripts/               # Convenience scripts for users
│   ├── run_ranking.py              # Run the ranking system
│   ├── analyze_sectors.py          # Run sector analysis
│   ├── visualize_results.py        # Generate visualizations
│   └── extract_bloomberg.py        # Extract Bloomberg data
├── tests/                 # Test scripts
│   ├── test_ranking_system.py    # Tests for core ranking functionality
│   └── test_sector_analysis.py   # Tests for sector analysis
├── install.sh             # Installation script for macOS/Linux
├── install.bat            # Installation script for Windows
├── README.md              # This file
├── setup.py               # Package installation configuration
├── pyproject.toml         # Modern Python packaging configuration
└── requirements.txt       # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Bloomberg Terminal access (for data extraction in office)
- Git (for deployment from GitHub)

### Installation

#### Option 1: Using the Installation Scripts (Recommended)
1. Clone this repository:
   ```bash
   git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
   cd Renaissance_Stock_Ranking
   ```

2. Run the appropriate installation script:
   ```bash
   # On macOS/Linux
   ./install.sh
   
   # On Windows
   install.bat
   ```

This will:
- Create a virtual environment
- Install all required packages
- Install the Renaissance package in development mode
- Make scripts executable (on Linux/macOS)

#### Option 2: Manual Installation
1. Clone this repository or download and extract the project ZIP file
2. Create a virtual environment:
   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Usage on Renaissance Investment Managers' System

### Data Workflow
This system follows a specific workflow due to restricted Bloomberg Terminal access:

1. **In-Office Data Extraction (Bloomberg Terminal Access Required)**:
   - Use Bloomberg Terminal to extract the NIFTY 500 constituent list with ISINs
   - Extract historical monthly closing prices for all NIFTY 500 stocks
   - Save data to structured CSV files
   - See [Data Extraction Guide](docs/data_extraction_guide.md) for detailed instructions
   - Or use the automated Bloomberg extractor: `python scripts/extract_bloomberg.py`

2. **Data Processing (Can be Done Anywhere)**:
   - Place the extracted data files in the `data/` directory:
     - `nifty500_list.csv`: List of NIFTY 500 constituents with ISINs
     - `historical_prices.csv`: Historical monthly closing prices
   - Run the Python system to process the data

### Running the System

#### Basic Usage
```bash
# Using the convenience script (recommended for most users)
python scripts/run_ranking.py

# OR using the package entry point (if installed)
renaissance-rank
```

#### Generating Visualizations
To create visual charts from the output data:
```bash
# Using the convenience script
python scripts/visualize_results.py

# OR using the package entry point
renaissance-visualize
```
This will generate charts showing return distributions, top performers, and rank changes in the `output/visualizations` directory.

#### Running Sector Analysis
To perform a detailed sector-based analysis:
```bash
# Using the convenience script
python scripts/analyze_sectors.py

# OR using the package entry point
renaissance-analyze
```
This will generate comprehensive sector reports and visualizations in the `output/sector_analysis` directory.

#### Bloomberg Data Extraction
For automated data extraction including sector information and financial metrics:
```bash
# Using the convenience script
python scripts/extract_bloomberg.py

# OR using the package entry point
renaissance-extract
```

#### Advanced Usage with Custom Paths
```bash
python scripts/run_ranking.py --nifty500-file data/custom_nifty500_list.csv --price-file data/custom_prices.csv --output-dir custom_output --generate-historical
```

Command-line arguments:
- `--nifty500-file`: Path to NIFTY 500 constituent list (default: `data/nifty500_list.csv`)
- `--price-file`: Path to historical prices file (default: `data/historical_prices.csv`)
- `--output-dir`: Directory for output files (default: `output/`)
- `--generate-historical`: Generate historical rankings output (optional)

### Python Package Usage

After installing the package with `pip install -e .`, you can use it in your own Python code:

```python
# Example of using the package in your own Python code
from renaissance.core.data_loader import load_and_prepare_all_data
from renaissance.core.return_calculator import calculate_yearly_returns
from renaissance.core.ranking_system import rank_stocks_by_return

# Load data
nifty500_df, prices_df = load_and_prepare_all_data('data/nifty500_list.csv', 'data/historical_prices.csv')

# Calculate returns
returns_df = calculate_yearly_returns(prices_df)

# Rank stocks
ranked_df = rank_stocks_by_return(returns_df)

# Do something with the rankings
print(ranked_df.head())
```

You can also run the tools using the provided entry points:

```bash
renaissance-rank     # Run the ranking system
renaissance-visualize  # Generate visualizations
renaissance-analyze    # Run sector analysis
renaissance-extract    # Extract Bloomberg data
```

### Testing

Run all tests:
```bash
python -m unittest discover tests
```

Run a specific test:
```bash
python -m unittest tests.test_ranking_system
```

## Input Data Requirements

The system processes two primary data files:

1. **NIFTY 500 constituent list** (`nifty500_list.csv`): A list of all stocks in the NIFTY 500 index, with their ISINs as the primary identifier.
2. **Historical monthly closing prices** (`historical_prices.csv`): Month-end closing prices for all NIFTY 500 stocks.

These files can be created either:
- Manually by extracting data from the Bloomberg Terminal as described in the [Data Extraction Guide](docs/data_extraction_guide.md)
- Automatically using the Bloomberg API integration (see the [Bloomberg API Guide](docs/bloomberg_api_guide.md))

## Output Files
- **Latest Rankings (`NIFTY500_Rankings_YYYYMMDD.csv`)**: Current month rankings
- **Rank Delta (`NIFTY500_RankDelta_YYYYMMDD.csv`)**: Rank changes from previous month
- **Summary Statistics (`NIFTY500_Ranking_Summary_YYYYMMDD_HHMMSS.txt`)**: Key statistics
- **Historical Rankings (Optional)**: All historical monthly rankings

## Troubleshooting

### Common Issues
- **File not found errors**: Ensure data files are in the correct location (`data/` directory)
- **Missing columns**: Check that your CSV files have the required columns
- **Date format issues**: Ensure dates are in YYYY-MM-DD format
- **Rank calculation issues**: Ensure price data spans at least 13 months to calculate yearly returns
- **Import errors**: If you get "module not found" errors, make sure you've installed the package with `pip install -e .`

For detailed troubleshooting guide, see [User Guide](docs/user_guide.md).

## Complete Workflow with Sector Analysis

The complete workflow incorporating all features is:

1. **Extract data** (monthly or as needed):
   ```bash
   python scripts/extract_bloomberg.py
   ```
   This extracts NIFTY 500 constituents with sectors, historical prices, and financial metrics.

2. **Run the core ranking system**:
   ```bash
   python scripts/run_ranking.py
   ```
   This generates the stock rankings based on yearly returns.

3. **Generate ranking visualizations**:
   ```bash
   python scripts/visualize_results.py
   ```
   This creates visual charts of the ranking results.

4. **Perform sector analysis**:
   ```bash
   python scripts/analyze_sectors.py
   ```
   This analyzes performance by sector and generates sector-based reports.

5. **Review all results for investment decisions**:
   - Individual stock rankings (`output/NIFTY500_Rankings_*.csv`)
   - Rank changes month-over-month (`output/NIFTY500_RankDelta_*.csv`)
   - Visual charts (`output/visualizations/`)
   - Sector analysis reports (`output/sector_analysis/`)
   - The consolidated sector analysis report (`output/sector_analysis/sector_analysis_report.txt`)

## Sector-Based Portfolio Construction

To construct a portfolio based on both individual stock performance and sector insights:

1. Identify top-performing sectors from the sector analysis report
2. Within those sectors, select the highest-ranked stocks from the main ranking system
3. Consider sector diversification based on the concentration analysis
4. Use financial metrics to ensure balanced exposure to value and growth characteristics

For advanced usage and customization options, see the [Sector Analysis Guide](docs/README_sector_analysis.md).

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
   git remote add origin https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
   git branch -M main
   git push -u origin main
   ```

## Author
Renaissance Investment Managers

## License
Proprietary - For use at Renaissance Investment Managers only
