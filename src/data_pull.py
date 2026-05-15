"""
Pull 10 years of monthly adjusted-close prices for 30 S&P 500 large-cap equities.
Saves raw prices and computed monthly returns to data/.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# 30 tickers across 10 S&P 500 sectors
TICKERS = {
    "Tech": ["AAPL", "MSFT", "NVDA", "GOOG", "META"],
    "Healthcare": ["JNJ", "UNH", "LLY", "PFE", "ABBV"],
    "Financials": ["JPM", "BAC", "GS", "BRK-B", "V"],
    "Consumer_Disc": ["AMZN", "TSLA", "HD"],
    "Consumer_Staples": ["PG", "KO", "COST"],
    "Energy": ["XOM", "CVX"],
    "Industrials": ["CAT", "UNP", "HON"],
    "Utilities": ["NEE", "DUK"],
    "Real_Estate": ["AMT"],
    "Materials": ["LIN"],
}

ALL_TICKERS = [t for sector in TICKERS.values() for t in sector]

END_DATE = datetime.today().strftime("%Y-%m-%d")
START_DATE = (datetime.today() - timedelta(days=365 * 10)).strftime("%Y-%m-%d")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def pull_prices():
    """Download monthly adjusted-close prices."""
    print(f"Pulling data for {len(ALL_TICKERS)} tickers: {START_DATE} to {END_DATE}")
    df = yf.download(ALL_TICKERS, start=START_DATE, end=END_DATE, interval="1mo")

    if isinstance(df.columns, pd.MultiIndex):
        prices = df["Adj Close"]
    else:
        prices = df

    prices = prices.dropna(how="all")
    return prices


def compute_returns(prices):
    """Compute simple monthly returns from adjusted-close prices."""
    returns = prices.pct_change().dropna()
    return returns


def main():
    prices = pull_prices()
    print(f"Price data shape: {prices.shape}")

    prices_path = DATA_DIR / "monthly_prices.csv"
    prices.to_csv(prices_path)
    print(f"Saved prices to {prices_path}")

    returns = compute_returns(prices)
    returns_path = DATA_DIR / "monthly_returns.csv"
    returns.to_csv(returns_path)
    print(f"Saved returns to {returns_path}")

    print(f"\nDate range: {prices.index[0].date()} to {prices.index[-1].date()}")
    print(f"Tickers: {prices.shape[1]}")
    print(f"Monthly observations: {returns.shape[0]}")


if __name__ == "__main__":
    main()
