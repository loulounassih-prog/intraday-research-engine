from pathlib import Path

import yfinance as yf
import pandas as pd



def download_price_data(
    ticker: str,
    start: str,
    end: str,
    interval: str = "1d",
    output_dir: str = "data",
) -> Path:
    """
    Download OHLCV market data from Yahoo Finance and save it as a CSV file.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    data = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=True,
        progress=False,
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    expected_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    data = data[expected_columns]

    file_path = output_path / f"{ticker}_{interval}_{start}_{end}.csv"
    data.to_csv(file_path, index=False)

    return file_path