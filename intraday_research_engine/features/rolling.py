import pandas as pd


def add_rolling_features(
    data: pd.DataFrame,
    window: int = 20,
) -> pd.DataFrame:
    """
    Add rolling mean, rolling volatility and z-score based on the Close price.
    """

    data = data.copy()

    mean_col = f"rolling_mean_{window}"
    std_col = f"rolling_std_{window}"
    zscore_col = f"zscore_{window}"

    data[mean_col] = data["Close"].rolling(window=window).mean()
    data[std_col] = data["Close"].rolling(window=window).std()

    data[zscore_col] = (data["Close"] - data[mean_col]) / data[std_col]

    return data