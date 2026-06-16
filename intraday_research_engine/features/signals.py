import numpy as np
import pandas as pd


def add_mean_reversion_signal(
    data: pd.DataFrame,
    zscore_col: str = "zscore_20",
    threshold: float = 1.0,
) -> pd.DataFrame:
    data = data.copy()

    data["mean_reversion_signal"] = np.where(
        data[zscore_col] < -threshold,
        1,
        np.where(data[zscore_col] > threshold, -1, 0),
    )

    return data