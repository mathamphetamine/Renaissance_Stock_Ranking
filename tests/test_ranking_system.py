"""
test_ranking_system.py

This script tests the functionality of the NIFTY 500 Stock Ranking System
using sample data files.
"""

import os
import sys
import pandas as pd
import unittest
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules from the project
from src.data_loader import load_and_prepare_all_data
from src.return_calculator import calculate_yearly_returns
from src.ranking_system import rank_stocks_by_return
from src.rank_delta_calculator import calculate_rank_delta


class TestRankingSystem(unittest.TestCase):
    """Test cases for the NIFTY 500 Stock Ranking System."""
    
    def setUp(self):
        """Set up test data paths."""
        # Determine the absolute path to the sample data files
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.nifty500_file = os.path.join(self.base_dir, 'data', 'sample', 'nifty500_list.csv')
        self.price_file = os.path.join(self.base_dir, 'data', 'sample', 'historical_prices.csv')
        
        # Ensure the test is run from a directory with access to the sample data
        if not os.path.exists(self.nifty500_file):
            self.skipTest(f"Sample data file not found: {self.nifty500_file}. Make sure sample data is in the correct location.")
        
        if not os.path.exists(self.price_file):
            self.skipTest(f"Sample data file not found: {self.price_file}. Make sure sample data is in the correct location.")
            
        # Print the directories for debugging
        print(f"Base directory: {self.base_dir}")
        print(f"NIFTY 500 file: {self.nifty500_file}")
        print(f"Price file: {self.price_file}")
    
    def test_data_loading(self):
        """Test that data can be loaded correctly."""
        nifty500_df, monthly_prices_df = load_and_prepare_all_data(
            self.nifty500_file, self.price_file
        )
        
        # Check that we have the expected number of stocks in the NIFTY 500 list
        self.assertGreaterEqual(len(nifty500_df), 5, "Should have at least 5 stocks in sample data")
        
        # Check that we have the required columns in the NIFTY 500 list
        self.assertIn('ISIN', nifty500_df.columns)
        self.assertIn('Name', nifty500_df.columns)
        
        # Check that we have the required columns in the price data
        self.assertIn('ISIN', monthly_prices_df.columns)
        self.assertIn('Date', monthly_prices_df.columns)
        self.assertIn('Price', monthly_prices_df.columns)
        
        # Check that Date column is datetime type
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(monthly_prices_df['Date']))
        
        # Print some summary information for debugging
        print(f"Loaded {len(nifty500_df)} stocks from NIFTY 500 list")
        print(f"Loaded {len(monthly_prices_df)} price records")
        print(f"Price data covers {monthly_prices_df['Date'].nunique()} months")
    
    def test_return_calculation(self):
        """Test that yearly returns can be calculated correctly."""
        _, monthly_prices_df = load_and_prepare_all_data(
            self.nifty500_file, self.price_file
        )
        
        returns_df = calculate_yearly_returns(monthly_prices_df)
        
        # Check that we have the required columns in the returns data
        self.assertIn('ISIN', returns_df.columns)
        self.assertIn('Date', returns_df.columns)
        self.assertIn('YearlyReturn', returns_df.columns)
        
        # Check that we actually calculated some returns
        self.assertGreater(len(returns_df), 0, "Should have calculated at least some returns")
        
        # Print some summary information for debugging
        print(f"Calculated {len(returns_df)} yearly returns")
        print(f"Return data covers {returns_df['Date'].nunique()} months")
        print(f"Returns calculated for {returns_df['ISIN'].nunique()} unique stocks")
        
        # Check a specific return calculation if we have sufficient data
        # This assumes our sample data has at least one stock with data in both 2022 and 2023
        dec_2022_stocks = monthly_prices_df[monthly_prices_df['Date'] == pd.Timestamp('2022-12-31')]['ISIN'].unique()
        dec_2023_stocks = monthly_prices_df[monthly_prices_df['Date'] == pd.Timestamp('2023-12-31')]['ISIN'].unique()
        
        # Find common stocks between the two periods
        common_stocks = set(dec_2022_stocks).intersection(set(dec_2023_stocks))
        
        if common_stocks:
            # Take the first common stock for verification
            test_isin = list(common_stocks)[0]
            
            # Get prices for December 2022 and December 2023
            price_dec2022 = monthly_prices_df[
                (monthly_prices_df['ISIN'] == test_isin) & 
                (monthly_prices_df['Date'] == pd.Timestamp('2022-12-31'))
            ]['Price'].values[0]
            
            price_dec2023 = monthly_prices_df[
                (monthly_prices_df['ISIN'] == test_isin) & 
                (monthly_prices_df['Date'] == pd.Timestamp('2023-12-31'))
            ]['Price'].values[0]
            
            # Calculate expected return
            expected_return = (price_dec2023 / price_dec2022) - 1
            
            # Find the calculated return for the same period
            calculated_return_rows = returns_df[
                (returns_df['ISIN'] == test_isin) & 
                (returns_df['Date'] == pd.Timestamp('2023-12-31'))
            ]
            
            if not calculated_return_rows.empty:
                calculated_return = calculated_return_rows['YearlyReturn'].values[0]
                
                # Compare with a small tolerance for floating-point errors
                self.assertAlmostEqual(calculated_return, expected_return, places=4)
                
                print(f"Verified return calculation for ISIN {test_isin}")
                print(f"Expected: {expected_return:.4f}, Calculated: {calculated_return:.4f}")
    
    def test_ranking(self):
        """Test that stocks can be ranked correctly based on returns."""
        _, monthly_prices_df = load_and_prepare_all_data(
            self.nifty500_file, self.price_file
        )
        
        returns_df = calculate_yearly_returns(monthly_prices_df)
        ranked_df = rank_stocks_by_return(returns_df)
        
        # Check that we have the Rank column
        self.assertIn('Rank', ranked_df.columns)
        
        # Check that ranks are integers
        self.assertTrue(all(isinstance(rank, int) for rank in ranked_df['Rank']))
        
        # Check that for each date, the stock with the highest return has Rank 1
        for date, group in ranked_df.groupby('Date'):
            # Only perform the check if we have at least one stock for this date
            if not group.empty:
                highest_return_idx = group['YearlyReturn'].idxmax()
                highest_return_rank = group.loc[highest_return_idx, 'Rank']
                self.assertEqual(highest_return_rank, 1, f"Highest return stock should have Rank 1 for date {date}")
        
        # Print some summary information for debugging
        print(f"Ranked {len(ranked_df)} stock records")
        print(f"Ranking covers {ranked_df['Date'].nunique()} months")
        print(f"Average number of ranked stocks per month: {ranked_df.groupby('Date')['ISIN'].count().mean():.1f}")
    
    def test_rank_delta(self):
        """Test that rank delta can be calculated correctly."""
        _, monthly_prices_df = load_and_prepare_all_data(
            self.nifty500_file, self.price_file
        )
        
        returns_df = calculate_yearly_returns(monthly_prices_df)
        ranked_df = rank_stocks_by_return(returns_df)
        delta_df = calculate_rank_delta(ranked_df)
        
        # Check that we have the RankDelta column
        self.assertIn('RankDelta', delta_df.columns)
        
        # Print some summary information for debugging
        print(f"Calculated rank delta for {len(delta_df)} stock records")
        print(f"Rank delta covers {delta_df['Date'].nunique()} months")
        
        # Count valid rank deltas (excluding first occurrence of each stock)
        valid_deltas = delta_df['RankDelta'].notna().sum()
        print(f"Valid rank deltas (excluding first occurrences): {valid_deltas}")
        
        # Check a specific rank delta calculation if we have sufficient data
        # Find stocks that appear in at least two consecutive months
        for isin in delta_df['ISIN'].unique():
            stock_data = delta_df[delta_df['ISIN'] == isin].sort_values('Date')
            
            # Need at least two rows for this stock to check rank delta
            if len(stock_data) >= 2:
                # Get two consecutive records
                for i in range(len(stock_data) - 1):
                    current_idx = stock_data.index[i]
                    next_idx = stock_data.index[i+1]
                    
                    # Only check if rank delta is not NaN for the second record
                    if not pd.isna(stock_data.loc[next_idx, 'RankDelta']):
                        rank1 = stock_data.loc[current_idx, 'Rank']
                        rank2 = stock_data.loc[next_idx, 'Rank']
                        expected_delta = rank2 - rank1
                        calculated_delta = stock_data.loc[next_idx, 'RankDelta']
                        
                        self.assertEqual(calculated_delta, expected_delta,
                                      f"Rank delta calculation incorrect for ISIN {isin}")
                        
                        print(f"Verified rank delta calculation for ISIN {isin}")
                        print(f"Previous rank: {rank1}, Current rank: {rank2}, Delta: {calculated_delta}")
                        return  # Exit after verifying one stock
    
    def test_end_to_end(self):
        """Test the complete analysis workflow."""
        # Load data
        nifty500_df, monthly_prices_df = load_and_prepare_all_data(
            self.nifty500_file, self.price_file
        )
        
        # Calculate returns
        returns_df = calculate_yearly_returns(monthly_prices_df)
        
        # Rank stocks
        ranked_df = rank_stocks_by_return(returns_df)
        
        # Calculate rank delta
        delta_df = calculate_rank_delta(ranked_df)
        
        # Check that we have data
        self.assertGreater(len(returns_df), 0, "Returns DataFrame should not be empty")
        self.assertGreater(len(ranked_df), 0, "Ranked DataFrame should not be empty")
        self.assertGreater(len(delta_df), 0, "Delta DataFrame should not be empty")
        
        # Check that the latest date has rankings
        latest_date = ranked_df['Date'].max()
        latest_rankings = ranked_df[ranked_df['Date'] == latest_date]
        self.assertGreater(len(latest_rankings), 0, 
                         f"No rankings found for latest date {latest_date}")
        
        # Print summary of the end-to-end test
        print("\nEnd-to-end test summary:")
        print(f"Processed {len(nifty500_df)} stocks with {len(monthly_prices_df)} price records")
        print(f"Calculated {len(returns_df)} yearly returns across {returns_df['Date'].nunique()} months")
        print(f"Generated rankings for {ranked_df['Date'].nunique()} months")
        print(f"Latest ranking date: {latest_date}, with {len(latest_rankings)} ranked stocks")


if __name__ == '__main__':
    unittest.main() 