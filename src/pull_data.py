"""
Pull historical price data from Yahoo Finance for portfolio optimization.
Saves monthly adjusted close prices and computed returns to CSV.
"""

import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime

# --- Configuration ---
TICKERS = {
    "Technology": ["AAPL", "MSFT", "NVDA", "GOOG", "META"],
    "Healthcare": ["JNJ", "UNH", "LLY", "PFE", "ABBV"],
    "Financials": ["JPM", "BAC", "GS", "BRK-B", "V"],
    "Consumer Discretionary": ["AMZN", "TSLA", "HD"],
    "Consumer Staples": ["PG", "KO", "COST"],
    "Energy": ["XOM", "CVX"],
    "Industrials": ["CAT", "UNP", "HON"],
    "Utilities": ["NEE", "DUK"],
    "Real Estate": ["AMT"],
    "Materials": ["LIN"],
}

ALL_TICKERS = [t for sector in TICKERS.values() for t in sector]
START_DATE = "2016-05-01"
END_DATE = "2026-05-01"
DATA_DIR = Path(__file__).parent.parent / "data"


def pull_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """Download monthly adjusted close prices from Yahoo Finance."""
    print(f"Pulling data for {len(tickers)} tickers from {start} to {end}...")
    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        interval="1mo",
        auto_adjust=True,
    )
    # yf.download returns MultiIndex columns; extract Close prices
    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data[["Close"]]
        prices.columns = tickers
    # Drop rows with any missing values
    prices = prices.dropna()
    return prices


def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute simple monthly returns from price data."""
    returns = prices.pct_change().dropna()
    return returns


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Pull and save prices
    prices = pull_prices(ALL_TICKERS, START_DATE, END_DATE)
    prices_path = DATA_DIR / "monthly_prices.csv"
    prices.to_csv(prices_path)
    print(f"Saved prices to {prices_path} ({prices.shape[0]} months, {prices.shape[1]} assets)")

    # Compute and save returns
    returns = compute_returns(prices)
    returns_path = DATA_DIR / "monthly_returns.csv"
    returns.to_csv(returns_path)
    print(f"Saved returns to {returns_path} ({returns.shape[0]} months, {returns.shape[1]} assets)")

    # Summary stats
    print("\n--- Summary ---")
    print(f"Date range: {prices.index[0].strftime('%Y-%m')} to {prices.index[-1].strftime('%Y-%m')}")
    print(f"Mean monthly return by asset:\n{returns.mean().sort_values(ascending=False).to_string()}")

    # Save ticker metadata
    meta = []
    for sector, ticks in TICKERS.items():
        for t in ticks:
            meta.append({"ticker": t, "sector": sector})
    meta_df = pd.DataFrame(meta)
    meta_path = DATA_DIR / "ticker_metadata.csv"
    meta_df.to_csv(meta_path, index=False)
    print(f"\nSaved ticker metadata to {meta_path}")


if __name__ == "__main__":
    main()
