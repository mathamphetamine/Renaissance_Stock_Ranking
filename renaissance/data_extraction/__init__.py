"""
Data extraction modules for the Renaissance Stock Ranking System.

This package contains tools for automating the extraction of data needed by the system:
    - bloomberg_data_extractor: Functions for extracting NIFTY 500 constituents,
                              historical prices, sector information, and financial metrics
                              from the Bloomberg Terminal using the Bloomberg API

These modules reduce the manual effort required to collect data and ensure data quality
by using the Bloomberg API for direct data extraction. They include error handling,
retries, and validation to ensure robust data collection even in challenging network
conditions.
"""
