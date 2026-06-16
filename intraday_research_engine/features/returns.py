import numpy as np
import pandas as pd


def add_returns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple and log returns computed from the Close price.
    """

    data = data.copy()

    data["simple_return"] = data["Close"].pct_change()
    data["log_return"] = np.log(data["Close"] / data["Close"].shift(1))

    return data