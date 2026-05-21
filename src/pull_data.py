"""
Pull historical price data from Yahoo Finance for portfolio optimization.
Saves monthly adjusted close prices and computed returns to CSV.
"""

import yfinance as yf
import pandas as pd
from pathlib import Path

# 30 large-cap US equities across 11 S&P 500 sectors
UNIVERSE = {
    "Information Technology": ["AAPL", "MSFT", "NVDA"],
    "Financials":              ["JPM", "BAC", "GS"],
    "Health Care":             ["JNJ", "UNH", "PFE"],
    "Consumer Discretionary":  ["AMZN", "TSLA", "HD"],
    "Communication Services":  ["GOOGL", "META", "VZ"],
    "Industrials":             ["CAT", "HON", "UPS"],
    "Consumer Staples":        ["PG", "KO", "WMT"],
    "Energy":                  ["XOM", "CVX", "SLB"],
    "Utilities":               ["NEE", "DUK"],
    "Real Estate":             ["PLD", "AMT"],
    "Materials":               ["LIN", "SHW"],
}

ALL_TICKERS = [t for sector in UNIVERSE.values() for t in sector]
START_DATE = "2016-05-01"
END_DATE = "2026-05-01"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def pull_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """Download monthly adjusted close prices from Yahoo Finance."""
    print(f"Pulling data for {len(tickers)} tickers from {start} to {end}...")
    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        interval="1mo",
        auto_adjust=True,
        progress=False,
    )
    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data[["Close"]]
        prices.columns = tickers
    return prices.dropna()


def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute simple monthly returns from price data."""
    return prices.pct_change().dropna()


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    prices = pull_prices(ALL_TICKERS, START_DATE, END_DATE)
    prices_path = DATA_DIR / "monthly_prices.csv"
    prices.to_csv(prices_path)
    print(
        f"Saved prices to {prices_path} "
        f"({prices.shape[0]} months, {prices.shape[1]} assets)"
    )

    returns = compute_returns(prices)
    returns_path = DATA_DIR / "monthly_returns.csv"
    returns.to_csv(returns_path)
    print(
        f"Saved returns to {returns_path} "
        f"({returns.shape[0]} months, {returns.shape[1]} assets)"
    )

    meta = [
        {"ticker": t, "sector": s}
        for s, ticks in UNIVERSE.items()
        for t in ticks
    ]
    meta_path = DATA_DIR / "ticker_metadata.csv"
    pd.DataFrame(meta).to_csv(meta_path, index=False)
    print(f"Saved ticker metadata to {meta_path}")

    start = prices.index[0].strftime("%Y-%m")
    end = prices.index[-1].strftime("%Y-%m")
    print("\n--- Summary ---")
    print(f"Date range: {start} to {end}")
    mean_returns = returns.mean().sort_values(ascending=False)
    print(f"Mean monthly return by asset:\n{mean_returns.to_string()}")


if __name__ == "__main__":
    main()
