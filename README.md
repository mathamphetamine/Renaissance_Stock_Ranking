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
- Automated calculation of yearly returns on a monthly rolling basis for NIFTY 500 stocks
- Ranking of stocks based on these returns
- Tracking of month-over-month rank changes
- Generation of output files for analysis
- Visualization tool for easy data interpretation without requiring Python knowledge
- Bloomberg API integration for automated data extraction (new!)
- **Historical Data Analysis**: Analyzes historical monthly price data to calculate yearly returns.
- **Performance Ranking**: Ranks stocks from best to worst based on calculated yearly returns.
- **Rank Change Tracking**: Tracks month-to-month rank changes to identify improving or declining stocks.
- **Data Visualization**: Automatically generates insightful charts and graphs from ranked data without requiring Python knowledge.
- **Sector Analysis**: Analyzes stock performance by sector, identifying top-performing sectors and sector concentration metrics.
- **Comprehensive Output**: Produces detailed CSV files with ranking results and performance metrics.
- **Flexible Configuration**: Easily customizable through configuration parameters.

## Project Structure
```
Renaissance_Stock_Ranking/
├── data/                  # Directory for storing input data files
│   └── sample/            # Sample data files for testing
├── docs/                  # Documentation
│   ├── data_extraction_guide.md  # Guide for Bloomberg data extraction
│   ├── example_usage.ipynb       # Jupyter notebook with example usage
│   ├── img/                      # Images for documentation
│   └── user_guide.md             # Detailed user guide
├── output/                # Generated output files (created when run)
├── src/                   # Source code
│   ├── __init__.py
│   ├── data_loader.py     # Functions for loading data from files
│   ├── return_calculator.py  # Functions for calculating yearly returns
│   ├── ranking_system.py  # Functions for ranking stocks
│   ├── rank_delta_calculator.py  # Functions for calculating rank changes
│   ├── output_generator.py  # Functions for generating output files
│   └── main.py            # Main script to run the system
├── tests/                 # Test scripts
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Bloomberg Terminal access (for data extraction in office)
- Git (for deployment from GitHub)

### Installation

#### Option 1: Clone from GitHub (Recommended)
1. Clone this repository:
   ```bash
   git clone https://github.com/mathamphetamine/Renaissance_Stock_Ranking.git
   cd Renaissance_Stock_Ranking
   ```

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

#### Option 2: Manual Installation
1. Download and extract the project ZIP file
2. Create a virtual environment (as above)
3. Install required packages (as above)

## Usage on Renaissance Investment Managers' System

### Data Workflow
This system follows a specific workflow due to restricted Bloomberg Terminal access:

1. **In-Office Data Extraction (Bloomberg Terminal Access Required)**:
   - Use Bloomberg Terminal to extract the NIFTY 500 constituent list with ISINs
   - Extract historical monthly closing prices for all NIFTY 500 stocks
   - Save data to structured CSV files
   - See [Data Extraction Guide](docs/data_extraction_guide.md) for detailed instructions

2. **Data Processing (Can be Done Anywhere)**:
   - Place the extracted data files in the `data/` directory:
     - `nifty500_list.csv`: List of NIFTY 500 constituents with ISINs
     - `historical_prices.csv`: Historical monthly closing prices
   - Run the Python system to process the data

### Running the System

#### Basic Usage
```bash
python src/main.py
```

#### Generating Visualizations
To create visual charts from the output data (requires matplotlib and seaborn):
```bash
python docs/visualize_results.py
```
This will generate charts showing return distributions, top performers, and rank changes in the `output/visualizations` directory.

#### Advanced Usage with Custom Paths
```bash
python src/main.py --nifty500-file data/custom_nifty500_list.csv --price-file data/custom_prices.csv --output-dir custom_output --generate-historical
```

Command-line arguments:
- `--nifty500-file`: Path to NIFTY 500 constituent list (default: `data/nifty500_list.csv`)
- `--price-file`: Path to historical prices file (default: `data/historical_prices.csv`)
- `--output-dir`: Directory for output files (default: `output/`)
- `--generate-historical`: Generate historical rankings output (optional)

### Testing

Run all tests:
```bash
python -m unittest discover tests
```

Run a specific test:
```bash
python -m unittest tests.test_ranking_system
```

### Sector-Based Analysis

To perform a detailed sector-based analysis of the ranking results:

1. Ensure your `nifty500_list.csv` file includes a 'Sector' column (automatically added if using the Bloomberg API extractor).
2. Run the sector analysis script:
   ```
   python docs/sector_analysis.py
   ```

This will generate comprehensive sector reports and visualizations in the `output/sector_analysis` directory, including:
- Sector performance statistics
- Top stocks by sector
- Sector concentration analysis
- Financial metrics by sector
- Investment strategy recommendations

For customization options, run:
```
python docs/sector_analysis.py --help
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

For detailed troubleshooting guide, see [User Guide](docs/user_guide.md).

## Glossary of Terms

Here's a quick reference:

- **CSV**: Comma-Separated Values file - a simple text file format that stores tabular data with commas between values
- **ISIN**: International Securities Identification Number - a 12-character alphanumeric code that uniquely identifies a specific security
- **Terminal Command/Command Line**: A text-based interface to control your computer by typing commands
- **Virtual Environment**: An isolated Python environment that allows packages to be installed for use by a particular project only
- **Repository**: A storage location for software packages, typically used with version control systems like Git
- **Dependencies**: External software packages that your project relies on to function
- **Script**: A file containing Python code that can be executed
- **Module**: A Python file containing definitions and statements that can be imported and used in other Python files

## Installation

Here's a simplified guide:

### Windows Installation
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
   - Run the system:
     ```
     python src\main.py
     ```
   - Check the "output" folder for results

### Mac/Linux Installation
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
   - Run the system:
     ```
     python src/main.py
     ```
   - Check the "output" folder for results

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
