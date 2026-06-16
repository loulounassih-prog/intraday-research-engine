import pandas as pd


def run_vectorized_backtest(
    data: pd.DataFrame,
    signal_col: str = "mean_reversion_signal",
    return_col: str = "simple_return",
    transaction_cost: float = 0.0005,
) -> pd.DataFrame:
    data = data.copy()

    data["position"] = data[signal_col].shift(1).fillna(0)

    data["gross_strategy_return"] = data["position"] * data[return_col]

    data["trade_size"] = data["position"].diff().abs().fillna(0)
    data["transaction_cost"] = data["trade_size"] * transaction_cost

    data["strategy_return"] = (
        data["gross_strategy_return"] - data["transaction_cost"]
    )

    data["equity_curve"] = (1 + data["strategy_return"].fillna(0)).cumprod()
    data["buy_and_hold_curve"] = (1 + data[return_col].fillna(0)).cumprod()

    return data