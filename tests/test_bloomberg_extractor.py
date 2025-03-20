"""
test_bloomberg_extractor.py

This script tests the Bloomberg data extraction functionality using mocks to avoid
requiring an actual Bloomberg Terminal connection.
"""

import os
import sys
import pandas as pd
import unittest
from unittest.mock import patch, MagicMock
import datetime
import tempfile
import shutil

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Check if Bloomberg API is available
try:
    import blpapi
    BLOOMBERG_API_AVAILABLE = True
except ImportError:
    BLOOMBERG_API_AVAILABLE = False

# Import modules from the project
# Use conditional imports to avoid errors when blpapi is not available
if BLOOMBERG_API_AVAILABLE:
    from renaissance.data_extraction.bloomberg_data_extractor import (
        get_nifty500_constituents, 
        get_historical_prices, 
        get_additional_metrics, 
        parse_arguments
    )


@unittest.skipIf(not BLOOMBERG_API_AVAILABLE, "Bloomberg API (blpapi) not available")
class TestBloombergExtractor(unittest.TestCase):
    """Test cases for the Bloomberg data extractor."""
    
    def setUp(self):
        """Set up test data."""
        # Create temporary directory for outputs
        self.test_dir = tempfile.mkdtemp()
        
        # Sample data for mocking
        self.sample_constituents = pd.DataFrame({
            'ISIN': ['INE009A01021', 'INE062A01020', 'INE001A01036', 'INE030A01027', 'INE040A01034'],
            'Name': ['Infosys Ltd', 'Tata Consultancy Services Ltd', 'Reliance Industries Ltd', 'Bharti Airtel Ltd', 'HDFC Bank Ltd'],
            'Ticker': ['INFO:IN', 'TCS:IN', 'RIL:IN', 'BHARTI:IN', 'HDFCB:IN'],
            'Sector': ['Information Technology', 'Information Technology', 'Energy', 'Communication Services', 'Financials']
        })
        
        self.sample_prices = pd.DataFrame({
            'ISIN': ['INE009A01021', 'INE009A01021', 'INE062A01020', 'INE062A01020'],
            'Date': [datetime.date(2023, 1, 31), datetime.date(2023, 2, 28), datetime.date(2023, 1, 31), datetime.date(2023, 2, 28)],
            'Price': [1500.50, 1550.25, 3200.75, 3150.30]
        })
        
        self.sample_metrics = pd.DataFrame({
            'ISIN': ['INE009A01021', 'INE062A01020', 'INE001A01036', 'INE030A01027', 'INE040A01034'],
            'PE_Ratio': [25.3, 28.4, 19.2, 22.5, 17.8],
            'PB_Ratio': [3.5, 12.2, 2.1, 3.3, 4.2],
            'ROE': [25.0, 40.5, 15.2, 18.3, 21.7],
            'DebtToAsset': [0.12, 0.05, 0.35, 0.28, 0.15],
            'DividendYield': [1.5, 1.2, 0.8, 2.1, 0.7]
        })
    
    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.test_dir)
    
    def test_parse_arguments(self):
        """Test command line argument parsing."""
        with patch('sys.argv', ['extract_bloomberg.py', '--test-mode', '--output-dir', self.test_dir]):
            args = parse_arguments()
            self.assertTrue(args.test_mode)
            self.assertEqual(args.output_dir, self.test_dir)
    
    @patch('renaissance.data_extraction.bloomberg_data_extractor.get_nifty500_constituents')
    def test_get_nifty500_constituents_test_mode(self, mock_get_constituents):
        """Test retrieving NIFTY 500 constituents in test mode."""
        # Set up the mock
        mock_get_constituents.return_value = self.sample_constituents
        
        # Call the function in test mode
        result = get_nifty500_constituents(test_mode=True)
        
        # Assert the function returns the expected sample data
        pd.testing.assert_frame_equal(result, self.sample_constituents)
    
    @patch('renaissance.data_extraction.bloomberg_data_extractor.get_historical_prices')
    def test_get_historical_prices_test_mode(self, mock_get_prices):
        """Test retrieving historical prices in test mode."""
        # Set up the mock
        mock_get_prices.return_value = self.sample_prices
        
        # Call the function in test mode
        result = get_historical_prices(
            isins=['INE009A01021', 'INE062A01020'],
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 3, 1),
            test_mode=True
        )
        
        # Assert the function returns the expected sample data
        pd.testing.assert_frame_equal(result, self.sample_prices)
    
    @patch('renaissance.data_extraction.bloomberg_data_extractor.get_additional_metrics')
    def test_get_additional_metrics_test_mode(self, mock_get_metrics):
        """Test retrieving additional financial metrics in test mode."""
        # Set up the mock
        mock_get_metrics.return_value = self.sample_metrics
        
        # Call the function in test mode
        result = get_additional_metrics(
            isins=['INE009A01021', 'INE062A01020', 'INE001A01036', 'INE030A01027', 'INE040A01034'],
            test_mode=True
        )
        
        # Assert the function returns the expected sample data
        pd.testing.assert_frame_equal(result, self.sample_metrics)


if __name__ == '__main__':
    unittest.main() 