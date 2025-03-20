"""
test_visualization.py

This script tests the visualization functionality of the Renaissance Stock Ranking System.
"""

import os
import sys
import pandas as pd
import unittest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import patch

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules from the project
from renaissance.visualization.visualize import create_visualizations

class TestVisualization(unittest.TestCase):
    """Test cases for the Renaissance visualization module."""
    
    def setUp(self):
        """Set up test data."""
        # Create temporary directory for visualization outputs
        self.test_dir = tempfile.mkdtemp()
        
        # Create sample rankings dataframe
        self.rankings_data = {
            'ISIN': ['IN0001', 'IN0002', 'IN0003', 'IN0004', 'IN0005'],
            'Name': ['Company A', 'Company B', 'Company C', 'Company D', 'Company E'],
            'Date': ['2023-12-31', '2023-12-31', '2023-12-31', '2023-12-31', '2023-12-31'],
            'YearlyReturn': [0.25, 0.15, 0.05, -0.05, -0.15],
            'Rank': [1, 2, 3, 4, 5]
        }
        self.rankings = pd.DataFrame(self.rankings_data)
        self.rankings['Date'] = pd.to_datetime(self.rankings['Date'])
        
        # Create sample rank delta dataframe
        self.rank_delta_data = {
            'ISIN': ['IN0001', 'IN0002', 'IN0003', 'IN0004', 'IN0005'],
            'Name': ['Company A', 'Company B', 'Company C', 'Company D', 'Company E'],
            'Date': ['2023-12-31', '2023-12-31', '2023-12-31', '2023-12-31', '2023-12-31'],
            'YearlyReturn': [0.25, 0.15, 0.05, -0.05, -0.15],
            'Rank': [1, 2, 3, 4, 5],
            'PreviousRank': [3, 1, 4, 2, 5],
            'RankDelta': [-2, 1, -1, 2, 0]
        }
        self.rank_delta = pd.DataFrame(self.rank_delta_data)
        self.rank_delta['Date'] = pd.to_datetime(self.rank_delta['Date'])
    
    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.test_dir)
    
    def test_create_visualizations(self):
        """Test creating visualizations."""
        # Mock the get_latest_file function to return our test data paths
        with patch('renaissance.visualization.visualize.get_latest_file') as mock_get_latest_file, \
             patch('renaissance.visualization.visualize.pd.read_csv') as mock_read_csv:
            
            # Set up the mocks to return our test data
            mock_read_csv.side_effect = [self.rankings, self.rank_delta]
            
            # Call the function
            create_visualizations()
            
            # Since we can't easily verify the saved files (due to the mocks),
            # we just verify that the function runs without errors and the mocks were called
            mock_get_latest_file.assert_called()
            self.assertEqual(mock_read_csv.call_count, 2)


if __name__ == '__main__':
    unittest.main() 