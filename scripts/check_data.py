from pathlib import Path

from intraday_research_engine.data.load import load_price_data
from intraday_research_engine.features.returns import add_returns
from intraday_research_engine.features.rolling import add_rolling_features
from intraday_research_engine.features.signals import add_mean_reversion_signal


if __name__ == "__main__":
    file_path = Path("data/SPY_1d_2020-01-01_2024-01-01.csv")

    data = load_price_data(file_path)
    data = add_returns(data)
    data = add_rolling_features(data, window=20)
    data = add_mean_reversion_signal(data, zscore_col="zscore_20", threshold=1.0)

    columns = [
        "Date",
        "Close",
        "zscore_20",
        "mean_reversion_signal",
    ]

    print(data[columns].tail(30))
    print()
    print(data["mean_reversion_signal"].value_counts().sort_index())