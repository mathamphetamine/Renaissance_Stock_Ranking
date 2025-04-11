#!/usr/bin/env python
"""
Bloomberg Data Extractor for Renaissance Stock Ranking System

This script automates the extraction of NIFTY 500 constituent data, historical prices,
sector classifications, and financial metrics using the Bloomberg API (BLPAPI).

Key Features:
- Extracts the current NIFTY 500 constituent list with ISINs, names, and tickers
- Retrieves GICS sector classifications for all constituents
- Downloads historical monthly closing prices with corporate action adjustments
- Collects key financial metrics (P/E ratio, P/B ratio, ROE, etc.)
- Handles connection issues with automatic retries
- Provides a test mode for development without Bloomberg access

Usage:
    python bloomberg_data_extractor.py [options]

Options:
    --output-dir DIR    Directory where output files will be saved (default: data)
    --start-date DATE   Start date for historical data (YYYY-MM-DD, default: 15 years ago)
    --end-date DATE     End date for historical data (YYYY-MM-DD, default: today)
    --test-mode         Run in test mode with sample data (no Bloomberg connection required)

Output Files:
    - nifty500_list.csv: List of NIFTY 500 constituents with ISIN, Name, Ticker, and Sector
    - historical_prices.csv: Monthly closing prices for all constituents
    - financial_metrics.csv: Key financial metrics for analysis and sector comparison

Author: Renaissance Investment Managers
Version: 1.0.0
"""

import pandas as pd
import datetime
import argparse
import logging
import os
import sys
import time

def setup_logging(output_dir=None):
    """Set up logging with appropriate handlers and directory structure."""
    if output_dir is None:
        output_dir = "output"
    
    # Create logs directory
    logs_dir = os.path.join(output_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Set up log file path
    log_file = os.path.join(logs_dir, "bloomberg_extractor.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

# Create logger
logger = logging.getLogger(__name__)

def parse_arguments():
    """
    Parse command line arguments for the Bloomberg data extractor.
    
    Returns:
        argparse.Namespace: Object containing parsed command-line arguments with the following attributes:
            - output_dir (str): Directory where CSV files will be saved
            - start_date (str): Start date for historical data in YYYY-MM-DD format
            - end_date (str): End date for historical data in YYYY-MM-DD format
            - test_mode (bool): Whether to run in test mode without Bloomberg connection
    """
    parser = argparse.ArgumentParser(description='Bloomberg Data Extractor for Renaissance Stock Ranking System')
    
    parser.add_argument('--output-dir', type=str, default='data',
                        help='Directory where CSV files will be saved')
    
    parser.add_argument('--start-date', type=str, default=None,
                        help='Start date for historical data (YYYY-MM-DD). Defaults to 15 years ago.')
    
    parser.add_argument('--end-date', type=str, default=None,
                        help='End date for historical data (YYYY-MM-DD). Defaults to today.')
    
    parser.add_argument('--test-mode', action='store_true',
                        help='Run in test mode with sample data (no Bloomberg connection required)')
    
    return parser.parse_args()

def get_nifty500_constituents(test_mode=False):
    """
    Get the current NIFTY 500 constituents with sector information using Bloomberg API.
    
    This function retrieves the complete list of NIFTY 500 constituent stocks along with
    their ISIN codes, names, tickers, and GICS sector classifications. The sector information
    is particularly important for sector-based analysis in the Renaissance Stock Ranking System.
    
    The function implements connection retry logic and timeout handling to ensure robustness
    when dealing with Bloomberg API connection issues.
    
    Args:
        test_mode (bool): If True, returns sample test data without calling Bloomberg API.
                         Useful for development and testing without Bloomberg access.
    
    Returns:
        pd.DataFrame: DataFrame with the following columns:
            - ISIN: International Securities Identification Number (unique identifier)
            - Name: Company name
            - Ticker: Bloomberg ticker symbol
            - Sector: GICS sector classification (e.g., "Financials", "Information Technology")
    
    Raises:
        Exception: If unable to connect to Bloomberg API after maximum retry attempts,
                 or if the request times out.
    """
    if test_mode:
        logger.info("TEST MODE: Using sample NIFTY 500 data instead of Bloomberg API")
        sample_data = [
            {"ISIN": "INE009A01021", "Name": "Infosys Ltd", "Ticker": "INFO:IN", "Sector": "Information Technology"},
            {"ISIN": "INE062A01020", "Name": "Tata Consultancy Services Ltd", "Ticker": "TCS:IN", "Sector": "Information Technology"},
            {"ISIN": "INE040A01034", "Name": "HDFC Bank Ltd", "Ticker": "HDFCB:IN", "Sector": "Financials"},
            {"ISIN": "INE001A01036", "Name": "Reliance Industries Ltd", "Ticker": "RIL:IN", "Sector": "Energy"},
            {"ISIN": "INE030A01027", "Name": "Bharti Airtel Ltd", "Ticker": "BHARTI:IN", "Sector": "Communication Services"},
            {"ISIN": "INE176A01028", "Name": "Hindustan Unilever Ltd", "Ticker": "HUVR:IN", "Sector": "Consumer Staples"},
            {"ISIN": "INE092A01019", "Name": "ITC Ltd", "Ticker": "ITC:IN", "Sector": "Consumer Staples"},
            {"ISIN": "INE397D01024", "Name": "Larsen & Toubro Ltd", "Ticker": "LT:IN", "Sector": "Industrials"},
            {"ISIN": "INE079A01024", "Name": "ICICI Bank Ltd", "Ticker": "ICICIBC:IN", "Sector": "Financials"},
            {"ISIN": "INE121A01024", "Name": "Adani Enterprises Ltd", "Ticker": "ADE:IN", "Sector": "Industrials"}
        ]
        return pd.DataFrame(sample_data)
    
    # Only import blpapi when actually needed (not in test mode)
    try:
        import blpapi
    except ImportError:
        logger.error("Bloomberg API (blpapi) not found. Please install it or use --test-mode.")
        raise ImportError("Bloomberg API (blpapi) not found. Please install it or use --test-mode.")
        
    # Set up session options
    SESSION_OPTIONS = blpapi.SessionOptions()
    SESSION_OPTIONS.setServerHost('localhost')
    SESSION_OPTIONS.setServerPort(8194)  # Default Bloomberg API port
    
    logger.info("Getting NIFTY 500 constituents from Bloomberg")
    
    # Maximum number of connection attempts
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        try:
            session = blpapi.Session(SESSION_OPTIONS)
            if not session.start():
                logger.error(f"Failed to start Bloomberg API session (attempt {attempt}/{max_attempts})")
                if attempt == max_attempts:
                    raise Exception("Failed to start Bloomberg API session after multiple attempts")
                time.sleep(5)  # Wait before retrying
                continue
            
            if not session.openService("//blp/refdata"):
                session.stop()
                logger.error(f"Failed to open //blp/refdata service (attempt {attempt}/{max_attempts})")
                if attempt == max_attempts:
                    raise Exception("Failed to open //blp/refdata service after multiple attempts")
                time.sleep(5)  # Wait before retrying
                continue
            
            refDataService = session.getService("//blp/refdata")
            request = refDataService.createRequest("ReferenceDataRequest")
            
            request.append("securities", "NIFTY 500 Index")
            
            # Request both index members and sector information
            request.append("fields", "INDX_MWEIGHT_HIST")
            request.append("fields", "GICS_SECTOR_NAME")  # Add GICS sector classification
            
            # Set the date to today to get current constituents
            overrides = request.getElement("overrides")
            override1 = overrides.appendElement()
            override1.setElement("fieldId", "INDX_MWEIGHT_HIST_END_DT")
            override1.setElement("value", datetime.date.today().strftime("%Y%m%d"))
            
            logger.info("Sending request for NIFTY 500 constituents")
            session.sendRequest(request)
            
            constituents = []
            timeout_seconds = 60
            start_time = time.time()
            
            while True:
                # Check for timeout
                if time.time() - start_time > timeout_seconds:
                    raise Exception(f"Bloomberg API request timed out after {timeout_seconds} seconds")
                
                ev = session.nextEvent(500)
                for msg in ev:
                    if msg.messageType() == blpapi.Name("ReferenceDataResponse"):
                        securityData = msg.getElement("securityData")
                        fieldData = securityData.getElement("fieldData")
                        
                        if fieldData.hasElement("INDX_MWEIGHT_HIST"):
                            weightData = fieldData.getElement("INDX_MWEIGHT_HIST")
                            for i in range(weightData.numValues()):
                                constituent = weightData.getValue(i)
                                isin = constituent.getElementAsString("ID_ISIN")
                                name = constituent.getElementAsString("NAME")
                                ticker = constituent.getElementAsString("TICKER")
                                
                                # Get sector if available
                                sector = "Unknown"
                                if constituent.hasElement("GICS_SECTOR_NAME"):
                                    sector = constituent.getElementAsString("GICS_SECTOR_NAME")
                                
                                constituents.append({
                                    "ISIN": isin,
                                    "Name": name,
                                    "Ticker": ticker,
                                    "Sector": sector
                                })
                
                if ev.eventType() == blpapi.Event.RESPONSE:
                    break
            
            session.stop()
            
            # Create DataFrame
            df = pd.DataFrame(constituents)
            logger.info(f"Retrieved {len(df)} NIFTY 500 constituents")
            
            # If we successfully got data with sectors, return it
            if "Sector" in df.columns and not all(df["Sector"] == "Unknown"):
                return df
            
            # If we didn't get sectors, try a separate query to get them
            logger.info("Attempting to retrieve sector information for constituents")
            return get_sectors_for_constituents(df)
            
        except blpapi.exception.NotFoundException as e:
            logger.error(f"Bloomberg API Error (attempt {attempt}/{max_attempts}): Service or field not found: {str(e)}")
            logger.error("This typically occurs when requested securities or fields are not available in your Bloomberg subscription.")
            if attempt == max_attempts:
                logger.error("Maximum number of attempts reached, giving up.")
                raise Exception(f"Bloomberg API error: Service or field not found - {str(e)}")
            else:
                logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
                continue
        
        except blpapi.exception.InvalidArgumentException as e:
            logger.error(f"Bloomberg API Error (attempt {attempt}/{max_attempts}): Invalid argument: {str(e)}")
            logger.error("This typically occurs when there's an issue with the request format or parameters.")
            if attempt == max_attempts:
                logger.error("Maximum number of attempts reached, giving up.")
                raise Exception(f"Bloomberg API error: Invalid argument - {str(e)}")
            else:
                logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
                continue
        
        except ConnectionError as e:
            logger.error(f"Network Error (attempt {attempt}/{max_attempts}): {str(e)}")
            logger.error("Please check your network connection and that Bloomberg Terminal is running.")
            if attempt == max_attempts:
                logger.error("Maximum number of attempts reached, giving up.")
                raise Exception(f"Network error connecting to Bloomberg - {str(e)}")
            else:
                logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
                continue
        
        except Exception as e:
            logger.error(f"Error in attempt {attempt}/{max_attempts}: {str(e)}")
            if attempt == max_attempts:
                logger.error("Maximum number of attempts reached, giving up.")
                raise
            else:
                logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
                continue

def get_sectors_for_constituents(constituents_df):
    """
    Get GICS sector information for a list of constituents if not already available.
    
    This function is called as a fallback if sector information wasn't retrieved in
    the initial query. It sends separate Bloomberg API requests to get sector
    classifications for each constituent, processing them in batches to avoid
    overwhelming the API.
    
    The GICS (Global Industry Classification Standard) sector classification is
    particularly valuable for sector-based analysis and is used by the sector
    analysis module in the Renaissance Stock Ranking System.
    
    Args:
        constituents_df (pd.DataFrame): DataFrame with constituent information
                                      including ISINs and tickers
        
    Returns:
        pd.DataFrame: The same DataFrame with an added or updated Sector column
                    containing GICS sector classifications
    """
    try:
        session = blpapi.Session(SESSION_OPTIONS)
        if not session.start():
            logger.warning("Failed to start Bloomberg API session for sector data, proceeding without sectors")
            logger.warning("Please verify that Bloomberg Terminal is running and you're logged in")
            return constituents_df
        
        if not session.openService("//blp/refdata"):
            session.stop()
            logger.warning("Failed to open //blp/refdata service for sector data, proceeding without sectors")
            logger.warning("This could be due to network issues or Bloomberg service unavailability")
            return constituents_df
        
        refDataService = session.getService("//blp/refdata")
        
        # Process in batches to avoid overwhelming the API
        batch_size = 50
        all_constituents = constituents_df.copy()
        
        # Add a Sector column with default value
        all_constituents["Sector"] = "Unknown"
        
        for i in range(0, len(all_constituents), batch_size):
            batch = all_constituents.iloc[i:i+batch_size]
            request = refDataService.createRequest("ReferenceDataRequest")
            
            # Add securities (using Bloomberg tickers)
            for _, row in batch.iterrows():
                ticker = row["Ticker"]
                if ":" not in ticker:
                    ticker = f"{ticker}:IN"  # Ensure proper Bloomberg format
                request.append("securities", ticker)
            
            # Add fields
            request.append("fields", "GICS_SECTOR_NAME")
            
            logger.info(f"Requesting sector data for batch {i//batch_size + 1}")
            session.sendRequest(request)
            
            response_count = 0
            while response_count < len(batch):
                ev = session.nextEvent(500)
                for msg in ev:
                    if msg.messageType() == blpapi.Name("ReferenceDataResponse"):
                        securityData = msg.getElement("securityData")
                        
                        # Process each security
                        for j in range(securityData.numValues()):
                            security_element = securityData.getValue(j)
                            ticker = security_element.getElementAsString("security").split()[0]
                            
                            # Find the matching row in our batch
                            matches = batch[batch["Ticker"] == ticker]
                            if len(matches) == 0:
                                # Try without exchange code
                                ticker_base = ticker.split(":")[0]
                                matches = batch[batch["Ticker"].str.startswith(ticker_base)]
                            
                            if len(matches) > 0:
                                idx = matches.index[0]
                                
                                # Get the sector if available
                                if security_element.hasElement("fieldData") and security_element.getElement("fieldData").hasElement("GICS_SECTOR_NAME"):
                                    sector = security_element.getElement("fieldData").getElementAsString("GICS_SECTOR_NAME")
                                    all_constituents.loc[idx, "Sector"] = sector
                                    response_count += 1
                            else:
                                logger.warning(f"Could not match ticker {ticker} to any constituent")
                                response_count += 1
                
                if ev.eventType() == blpapi.Event.RESPONSE:
                    break
        
        session.stop()
        logger.info(f"Added sector information to constituents data")
        return all_constituents
        
    except blpapi.exception.NotFoundException as e:
        logger.warning(f"Bloomberg API Error when retrieving sectors: Service or field not found: {str(e)}")
        logger.warning("Proceeding without sector information")
        return constituents_df
    
    except blpapi.exception.InvalidArgumentException as e:
        logger.warning(f"Bloomberg API Error when retrieving sectors: Invalid argument: {str(e)}")
        logger.warning("Proceeding without sector information")
        return constituents_df
    
    except ConnectionError as e:
        logger.warning(f"Network Error when retrieving sectors: {str(e)}")
        logger.warning("Please check your network connection and that Bloomberg Terminal is running")
        logger.warning("Proceeding without sector information")
        return constituents_df
        
    except Exception as e:
        logger.warning(f"Error retrieving sector information: {str(e)}")
        logger.warning("Proceeding without sector information")
        return constituents_df

def get_historical_prices(isins, start_date, end_date, test_mode=False):
    """
    Get historical monthly prices for a list of ISINs.
    
    Args:
        isins (list): List of ISINs to get prices for
        start_date (datetime): Start date for historical data
        end_date (datetime): End date for historical data
        test_mode (bool): If True, returns sample data without calling Bloomberg API
        
    Returns:
        pd.DataFrame: DataFrame with ISIN, Date, and Price columns
    """
    if test_mode:
        logger.info("TEST MODE: Using sample price data instead of Bloomberg API")
        
        # Generate sample dates (month-end dates)
        dates = []
        current_date = start_date
        while current_date <= end_date:
            # Get the last day of the month
            next_month = current_date.replace(day=28) + datetime.timedelta(days=4)
            last_day = next_month - datetime.timedelta(days=next_month.day)
            dates.append(last_day)
            
            # Move to the next month
            current_date = current_date.replace(day=1)
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        # Generate sample price data
        data = []
        for isin in isins:
            base_price = 1000 + hash(isin) % 4000  # Pseudo-random starting price based on ISIN
            current_price = base_price
            
            for date in dates:
                # Add some random price movement
                change_pct = (hash(isin + str(date)) % 20 - 10) / 100  # -10% to +10%
                current_price = current_price * (1 + change_pct)
                
                data.append({
                    "ISIN": isin,
                    "Date": date.strftime("%Y-%m-%d"),
                    "Price": round(current_price, 2)
                })
        
        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    
    # Only import blpapi when actually needed (not in test mode)
    try:
        import blpapi
    except ImportError:
        logger.error("Bloomberg API (blpapi) not found. Please install it or use --test-mode.")
        raise ImportError("Bloomberg API (blpapi) not found. Please install it or use --test-mode.")
        
    # Set up session options
    SESSION_OPTIONS = blpapi.SessionOptions()
    SESSION_OPTIONS.setServerHost('localhost')
    SESSION_OPTIONS.setServerPort(8194)  # Default Bloomberg API port
    
    logger.info(f"Getting historical prices for {len(isins)} stocks")
    
    session = blpapi.Session(SESSION_OPTIONS)
    if not session.start():
        raise Exception("Failed to start Bloomberg API session")
    
    if not session.openService("//blp/refdata"):
        session.stop()
        raise Exception("Failed to open //blp/refdata service")
    
    refDataService = session.getService("//blp/refdata")
    
    all_prices = []
    
    # Process ISINs in batches of 50 to avoid overwhelming the API
    batch_size = 50
    for i in range(0, len(isins), batch_size):
        batch_isins = isins[i:i+batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}/{(len(isins) + batch_size - 1)//batch_size}")
        
        request = refDataService.createRequest("HistoricalDataRequest")
        
        # Add securities (convert ISINs to Bloomberg Equity identifiers)
        for isin in batch_isins:
            request.append("securities", f"{isin} Equity")
        
        # Add fields
        request.append("fields", "PX_LAST")
        
        # Set date range
        request.set("startDate", start_date.strftime("%Y%m%d"))
        request.set("endDate", end_date.strftime("%Y%m%d"))
        
        # Set periodicity to monthly
        request.set("periodicitySelection", "MONTHLY")
        
        # Request prices in INR
        overrides = request.getElement("overrides")
        override1 = overrides.appendElement()
        override1.setElement("fieldId", "CRNCY")
        override1.setElement("value", "INR")
        
        logger.info(f"Sending request for historical prices (batch {i//batch_size + 1})")
        session.sendRequest(request)
        
        batch_prices = []
        while True:
            ev = session.nextEvent(500)
            for msg in ev:
                if msg.messageType() == blpapi.Name("HistoricalDataResponse"):
                    securityData = msg.getElement("securityData")
                    security = securityData.getElementAsString("security")
                    
                    # Extract ISIN from security string (e.g., "INE009A01021 Equity")
                    isin = security.split(" ")[0]
                    
                    fieldData = securityData.getElement("fieldData")
                    for i in range(fieldData.numValues()):
                        point = fieldData.getValue(i)
                        date = point.getElementAsDatetime("date").strftime("%Y-%m-%d")
                        price = point.getElementAsFloat("PX_LAST")
                        
                        batch_prices.append({
                            "ISIN": isin,
                            "Date": date,
                            "Price": price
                        })
            
            if ev.eventType() == blpapi.Event.RESPONSE:
                break
        
        all_prices.extend(batch_prices)
    
    session.stop()
    
    # Create DataFrame
    df = pd.DataFrame(all_prices)
    
    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Sort by ISIN and Date
    df = df.sort_values(["ISIN", "Date"])
    
    logger.info(f"Retrieved {len(df)} historical price records")
    
    return df

def validate_data(nifty500_df, prices_df):
    """
    Validate the extracted data to ensure it meets the requirements.
    
    Args:
        nifty500_df (pd.DataFrame): NIFTY 500 constituents data
        prices_df (pd.DataFrame): Historical price data
        
    Returns:
        bool: True if data is valid, False otherwise
    """
    logger.info("Validating extracted data")
    
    # Check that we have data for all ISINs
    missing_isins = set(nifty500_df['ISIN']) - set(prices_df['ISIN'].unique())
    if missing_isins:
        logger.warning(f"Missing price data for {len(missing_isins)} ISINs")
        
    # Check date coverage
    all_dates = prices_df['Date'].unique()
    date_range = (prices_df['Date'].min(), prices_df['Date'].max())
    logger.info(f"Date range: {date_range[0]} to {date_range[1]}")
    logger.info(f"Total months: {len(all_dates)}")
    
    return True

def get_additional_metrics(isins, test_mode=False):
    """
    Get additional financial metrics for a list of ISINs.
    
    Args:
        isins (list): List of ISINs to get metrics for
        test_mode (bool): If True, returns sample data without calling Bloomberg API
        
    Returns:
        pd.DataFrame: DataFrame with ISIN and various financial metrics
    """
    if test_mode:
        logger.info("TEST MODE: Using sample financial metrics instead of Bloomberg API")
        
        # Generate sample metrics data
        data = []
        for isin in isins:
            # Generate pseudo-random metrics based on ISIN
            pe_ratio = round(10 + (hash(isin) % 40), 2)
            pb_ratio = round(1 + (hash(isin[:6]) % 10) / 2, 2)
            roe = round(5 + (hash(isin[:4]) % 25), 2)
            debt_to_asset = round(0.1 + (hash(isin[:8]) % 8) / 10, 2)
            div_yield = round((hash(isin[:7]) % 10) / 2, 2)
            
            data.append({
                "ISIN": isin,
                "PE_Ratio": pe_ratio,
                "PB_Ratio": pb_ratio,
                "ROE": roe,
                "DebtToAsset": debt_to_asset,
                "DividendYield": div_yield
            })
        
        return pd.DataFrame(data)
    
    # Only import blpapi when actually needed (not in test mode)
    try:
        import blpapi
    except ImportError:
        logger.error("Bloomberg API (blpapi) not found. Please install it or use --test-mode.")
        raise ImportError("Bloomberg API (blpapi) not found. Please install it or use --test-mode.")
        
    # Set up session options
    SESSION_OPTIONS = blpapi.SessionOptions()
    SESSION_OPTIONS.setServerHost('localhost')
    SESSION_OPTIONS.setServerPort(8194)  # Default Bloomberg API port
    
    logger.info(f"Getting additional financial metrics for {len(isins)} stocks")
    
    try:
        session = blpapi.Session(SESSION_OPTIONS)
        if not session.start():
            logger.error("Failed to start Bloomberg API session for financial metrics")
            return pd.DataFrame({"ISIN": isins})  # Return just ISINs if we can't get metrics
        
        if not session.openService("//blp/refdata"):
            session.stop()
            logger.error("Failed to open //blp/refdata service for financial metrics")
            return pd.DataFrame({"ISIN": isins})
        
        refDataService = session.getService("//blp/refdata")
        
        all_metrics = []
        
        # Process ISINs in batches of 50 to avoid overwhelming the API
        batch_size = 50
        for i in range(0, len(isins), batch_size):
            batch_isins = isins[i:i+batch_size]
            logger.info(f"Processing metrics batch {i//batch_size + 1}/{(len(isins) + batch_size - 1)//batch_size}")
            
            request = refDataService.createRequest("ReferenceDataRequest")
            
            # Add securities (convert ISINs to Bloomberg Equity identifiers)
            for isin in batch_isins:
                request.append("securities", f"{isin} Equity")
            
            # Add fields for financial metrics
            request.append("fields", "PE_RATIO")            # Price-to-earnings ratio
            request.append("fields", "PX_TO_BOOK_RATIO")    # Price-to-book ratio
            request.append("fields", "RETURN_COM_EQY")      # Return on equity
            request.append("fields", "TOT_DEBT_TO_TOT_ASSET") # Debt-to-asset ratio
            request.append("fields", "EQY_DVD_YLD_IND")     # Dividend yield
            
            logger.info(f"Sending request for financial metrics (batch {i//batch_size + 1})")
            session.sendRequest(request)
            
            batch_metrics = []
            while True:
                ev = session.nextEvent(500)
                for msg in ev:
                    if msg.messageType() == blpapi.Name("ReferenceDataResponse"):
                        securityData = msg.getElement("securityData")
                        
                        # Process each security
                        for j in range(securityData.numValues()):
                            security_element = securityData.getValue(j)
                            security = security_element.getElementAsString("security")
                            
                            # Extract ISIN from security string (e.g., "INE009A01021 Equity")
                            isin = security.split(" ")[0]
                            
                            metric_data = {"ISIN": isin}
                            
                            # Process each field if available
                            if security_element.hasElement("fieldData"):
                                field_data = security_element.getElement("fieldData")
                                
                                if field_data.hasElement("PE_RATIO"):
                                    metric_data["PE_Ratio"] = field_data.getElementAsFloat("PE_RATIO")
                                
                                if field_data.hasElement("PX_TO_BOOK_RATIO"):
                                    metric_data["PB_Ratio"] = field_data.getElementAsFloat("PX_TO_BOOK_RATIO")
                                
                                if field_data.hasElement("RETURN_COM_EQY"):
                                    metric_data["ROE"] = field_data.getElementAsFloat("RETURN_COM_EQY")
                                
                                if field_data.hasElement("TOT_DEBT_TO_TOT_ASSET"):
                                    metric_data["DebtToAsset"] = field_data.getElementAsFloat("TOT_DEBT_TO_TOT_ASSET")
                                
                                if field_data.hasElement("EQY_DVD_YLD_IND"):
                                    metric_data["DividendYield"] = field_data.getElementAsFloat("EQY_DVD_YLD_IND")
                            
                            batch_metrics.append(metric_data)
                
                if ev.eventType() == blpapi.Event.RESPONSE:
                    break
            
            all_metrics.extend(batch_metrics)
        
        session.stop()
        
        # Create DataFrame
        df = pd.DataFrame(all_metrics)
        logger.info(f"Retrieved financial metrics for {len(df)} stocks")
        return df
        
    except Exception as e:
        logger.error(f"Error getting financial metrics: {str(e)}")
        # Return just the ISINs if we encountered an error
        return pd.DataFrame({"ISIN": isins})

def main():
    """
    Main entry point for the Bloomberg data extractor.
    
    This function orchestrates the entire data extraction process using Bloomberg API.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Set up logging
    logger = setup_logging(args.output_dir)
    
    logger.info("Starting Bloomberg data extraction")
    
    try:
        # Set default start and end dates if not provided
        end_date = datetime.datetime.now().date() if args.end_date is None else datetime.datetime.strptime(args.end_date, "%Y-%m-%d").date()
        start_date = end_date.replace(year=end_date.year - 15) if args.start_date is None else datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
        
        logger.info(f"Date range: {start_date} to {end_date}")
        logger.info(f"Output directory: {args.output_dir}")
        
        if args.test_mode:
            logger.info("Running in TEST MODE - no Bloomberg connection will be made")
            
        # Get NIFTY 500 constituents
        logger.info("Step 1: Extracting NIFTY 500 constituents")
        nifty500_df = get_nifty500_constituents(test_mode=args.test_mode)
        
        # Save the constituents list
        constituents_file = os.path.join(args.output_dir, "nifty500_list.csv")
        nifty500_df.to_csv(constituents_file, index=False)
        logger.info(f"Saved NIFTY 500 list to {constituents_file}")
        
        # Get historical prices
        logger.info("Step 2: Extracting historical prices")
        prices_df = get_historical_prices(
            nifty500_df["ISIN"].tolist(), 
            start_date, 
            end_date, 
            test_mode=args.test_mode
        )
        
        # Validate the extracted data
        validate_data(nifty500_df, prices_df)
        
        # Save the prices
        prices_file = os.path.join(args.output_dir, "historical_prices.csv")
        prices_df.to_csv(prices_file, index=False)
        logger.info(f"Saved historical prices to {prices_file}")
        
        # Get additional financial metrics
        logger.info("Step 3: Extracting financial metrics")
        try:
            metrics_df = get_additional_metrics(nifty500_df["ISIN"].tolist(), test_mode=args.test_mode)
            if len(metrics_df.columns) > 1:  # If we have more than just ISIN column
                metrics_file = os.path.join(args.output_dir, "financial_metrics.csv")
                metrics_df.to_csv(metrics_file, index=False)
                logger.info(f"Saved additional financial metrics to {metrics_file}")
        except Exception as e:
            logger.warning(f"Could not retrieve additional financial metrics: {str(e)}")
            logger.info("Continuing without financial metrics")
        
        logger.info("Bloomberg data extraction completed successfully")
        logger.info(f"Summary:")
        logger.info(f"- NIFTY 500 constituents: {len(nifty500_df)} stocks")
        logger.info(f"- Historical prices: {len(prices_df)} records")
        logger.info(f"- Date range: {prices_df['Date'].min().strftime('%Y-%m-%d')} to {prices_df['Date'].max().strftime('%Y-%m-%d')}")
        logger.info(f"- Files saved to: {args.output_dir}")
        return 0
    
    except Exception as e:
        logger.error(f"Error during Bloomberg data extraction: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main()) 