from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume"]


def load_price_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load OHLCV price data from a CSV file and return a clean DataFrame.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    data = pd.read_csv(file_path)

    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    data = data[REQUIRED_COLUMNS].copy()

    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date")
    data = data.drop_duplicates(subset="Date")
    data = data.reset_index(drop=True)

    return data