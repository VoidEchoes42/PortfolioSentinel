import yfinance as yf
import pandas as pd
import datetime
from pathlib import Path
from config.settings import MARKET_TICKERS, PROCESSED_DATA_DIR, DEFAULT_LOOKBACK_YEARS

def fetch_market_data(tickers=None, lookback_years=None, cache_file="market_prices.csv"):
    """
    Fetches daily adjusted close prices for given tickers.
    Uses caching to avoid repeated API calls.
    """
    if tickers is None:
        tickers = MARKET_TICKERS
    if lookback_years is None:
        lookback_years = DEFAULT_LOOKBACK_YEARS

    cache_path = PROCESSED_DATA_DIR / cache_file

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=lookback_years * 365)

    try:
        print(f"Fetching market data for {len(tickers)} tickers from {start_date} to {end_date}...")
        df = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
        
        # In case only one ticker is passed, yfinance returns a Series instead of a DataFrame
        if isinstance(df, pd.Series):
            df = df.to_frame(name=tickers[0])
            
        # Ensure we have all requested tickers in columns
        missing_tickers = [t for t in tickers if t not in df.columns]
        if missing_tickers:
            print(f"Warning: Data not found for {missing_tickers}")

        # Save to cache
        df.to_csv(cache_path)
        print("Market data successfully fetched and cached.")
        return df

    except Exception as e:
        print(f"Error fetching data from Yahoo Finance: {e}")
        print("Attempting to load from local cache...")
        if cache_path.exists():
            df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
            print("Successfully loaded market data from cache.")
            return df
        else:
            raise FileNotFoundError("No local cache found and API request failed. Check internet connection.")

def load_cached_market_data(cache_file="market_prices.csv"):
    """Loads market data strictly from cache."""
    cache_path = PROCESSED_DATA_DIR / cache_file
    if cache_path.exists():
        return pd.read_csv(cache_path, index_col=0, parse_dates=True)
    else:
        raise FileNotFoundError(f"Cache file {cache_path} not found.")

def fetch_fred_rates(series_id="DGS10", lookback_years=None):
    """
    Fetches macroeconomic data from FRED API (e.g., 10-Year Treasury Constant Maturity Rate).
    """
    import pandas_datareader.data as web
    if lookback_years is None:
        lookback_years = DEFAULT_LOOKBACK_YEARS
        
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=lookback_years * 365)
    
    try:
        df = web.DataReader(series_id, "fred", start_date, end_date)
        return df.dropna()
    except Exception as e:
        print(f"Error fetching from FRED: {e}")
        # Return a dummy series if offline
        dates = pd.date_range(start=start_date, end=end_date, freq='B')
        return pd.DataFrame({series_id: 4.5}, index=dates)

if __name__ == "__main__":
    # Quick test
    fetch_market_data()
    print(fetch_fred_rates().tail())
