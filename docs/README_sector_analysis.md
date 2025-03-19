# Sector Analysis Tool for Renaissance Stock Ranking System

## Overview

The sector analysis tool extends the Renaissance Stock Ranking System by providing sector-based insights from the ranking results. This tool enables portfolio managers and analysts to understand sector performance, identify sector trends, and make more informed investment decisions by considering both individual stock performance and sector dynamics.

## Features

The sector analysis tool provides the following capabilities:

1. **Sector Performance Analysis**
   - Average, median, min, and max returns by sector
   - Risk metrics (standard deviation of returns)
   - Sector ranking based on performance

2. **Top Stocks by Sector**
   - Identification of best performers in each sector
   - Detailed stock profiles with financial metrics
   - Comparison of top stocks across sectors

3. **Sector Concentration Analysis**
   - Distribution of stocks across sectors
   - Sector contribution to overall market returns
   - Identification of over/underrepresented sectors

4. **Financial Metrics by Sector**
   - Average PE ratios, PB ratios, ROE, debt metrics, and dividend yields by sector
   - Identification of value vs. growth sectors
   - Cross-sector comparisons of financial health

5. **Investment Strategy Recommendations**
   - Value opportunity identification
   - Growth sector highlighting
   - Diversification suggestions based on sector analysis

## Prerequisites

To use the sector analysis tool, you need:

1. A completed run of the Renaissance Stock Ranking System, which generates the ranking output files
2. NIFTY 500 constituent list with sector information (automatically provided if using the Bloomberg API extractor)
3. Financial metrics data (optional, enhances analysis if available)

## Usage

### Basic Usage

Run the sector analysis script after completing a ranking system run:

```bash
python docs/sector_analysis.py
```

This will automatically use:
- The latest rankings file from the `output` directory
- The latest NIFTY 500 list with sector information from the `data` directory
- The latest financial metrics file from the `output` directory (if available)
- Save results to `output/sector_analysis/`

### Advanced Usage

For more control over the inputs and outputs:

```bash
python docs/sector_analysis.py --rankings-file <path_to_rankings_file> --nifty500-file <path_to_nifty500_file> --metrics-file <path_to_metrics_file> --output-dir <output_directory>
```

Example with custom paths:
```bash
python docs/sector_analysis.py --rankings-file output/NIFTY500_Rankings_20230331.csv --nifty500-file data/custom_nifty500_list.csv --metrics-file output/custom_metrics.csv --output-dir analysis/sectors
```

### Command-line Arguments

- `--rankings-file`: Path to the rankings output file (default: latest in `output/`)
- `--nifty500-file`: Path to the NIFTY 500 list with sector info (default: `data/nifty500_list.csv`)
- `--metrics-file`: Path to the financial metrics file (default: latest in `output/`)
- `--output-dir`: Directory where analysis results will be saved (default: `output/sector_analysis/`)

## Output Files

The tool generates the following output files:

1. **sector_performance.csv**: Statistical performance metrics for each sector
2. **sector_returns.png**: Visualization of average returns by sector
3. **top_stocks_by_sector.txt**: Detailed report of top performers in each sector
4. **top_stocks_comparison.png**: Visual comparison of top stocks across sectors
5. **sector_concentration.csv**: Metrics on sector distribution and contribution
6. **sector_concentration.png**: Pie charts visualizing sector concentration
7. **sector_metrics.csv**: Financial metrics averaged by sector
8. **sector_metrics.png**: Visualizations of key financial metrics by sector
9. **sector_analysis_report.txt**: Comprehensive analysis report with investment implications

## Integration with Bloomberg API

When used with the Bloomberg API data extractor, the sector analysis tool automatically leverages:

1. **GICS Sector Classification**: The Bloomberg API extractor retrieves the GICS (Global Industry Classification Standard) sector for each stock, providing a standardized sector classification.

2. **Financial Metrics**: The Bloomberg API extractor can retrieve key financial metrics for each stock, enabling richer sector-based analysis.

To ensure proper integration:

1. Run the Bloomberg data extractor with sector information:
   ```bash
   python src/bloomberg_data_extractor.py
   ```

2. Run the standard ranking system:
   ```bash
   python src/main.py
   ```

3. Run the sector analysis tool:
   ```bash
   python docs/sector_analysis.py
   ```

## Sample Workflow

A complete workflow including sector analysis:

1. **Extract data** (monthly or as needed):
   ```bash
   python src/bloomberg_data_extractor.py --output-dir data
   ```

2. **Run ranking system**:
   ```bash
   python src/main.py
   ```

3. **Generate visualizations**:
   ```bash
   python docs/visualize_results.py
   ```

4. **Perform sector analysis**:
   ```bash
   python docs/sector_analysis.py
   ```

5. **Review results**:
   - Examine the sector analysis report in `output/sector_analysis/sector_analysis_report.txt`
   - Review visualizations for insights
   - Use findings to inform investment decisions

## Interpreting Results

### Sector Performance

- **High Average Returns**: Sectors with high average returns have outperformed others during the analysis period
- **High Standard Deviation**: Indicates higher volatility/risk in that sector
- **Rank Percentile**: Lower values indicate better overall sector performance

### Sector Concentration

- **Count/Percentage**: Shows how many stocks from each sector are in the dataset
- **Return Contribution**: Shows which sectors contribute most to overall market returns

### Financial Metrics by Sector

- **PE Ratio**: Lower values may indicate undervalued sectors
- **ROE**: Higher values suggest more efficient use of equity
- **Debt Metrics**: Lower values indicate less leveraged sectors
- **Dividend Yield**: Higher values may indicate income-focused sectors

### Investment Implications

The sector analysis report provides specific investment strategy suggestions based on:

1. **Value Opportunities**: Sectors with strong returns but relatively low valuations
2. **Growth Focus**: Highest performing sectors regardless of valuation
3. **Diversification Opportunities**: Balanced selection of sectors for portfolio diversification

## Customization

The sector analysis tool can be customized by modifying the script. Common customizations include:

- Adding additional financial metrics to the analysis
- Changing visualization styles or color schemes
- Adjusting reporting thresholds or categories
- Creating custom investment strategy rules

## Troubleshooting

### Common Issues

1. **Missing Sector Information**:
   - Ensure your NIFTY 500 list file includes a 'Sector' column
   - If using Bloomberg API, confirm sector extraction is working

2. **Financial Metrics Not Appearing**:
   - Verify the financial metrics file exists and contains the expected columns
   - Check that metrics are being properly merged based on ISIN

3. **No Output Generated**:
   - Ensure rankings file exists and contains the required columns
   - Check permissions for writing to the output directory

4. **Empty or Small Sectors**:
   - Some sectors may have few stocks in the NIFTY 500, leading to less reliable statistics
   - Consider using a broader classification or focusing on major sectors

## Future Enhancements

Planned future enhancements to the sector analysis tool:

1. **Historical Sector Rotation Analysis**: Track changing sector performance over time
2. **Correlation Analysis**: Identify correlations between sectors
3. **Economic Factor Sensitivity**: Analyze how different sectors respond to economic variables
4. **Scenario Testing**: Model sector performance under different market conditions
5. **Automated Investment Recommendations**: Generate specific allocation recommendations

## Conclusion

The sector analysis tool adds significant value to the Renaissance Stock Ranking System by providing deeper insights into market structure and sector dynamics. By understanding both individual stock performance and sector trends, portfolio managers can make more informed, comprehensive investment decisions. 