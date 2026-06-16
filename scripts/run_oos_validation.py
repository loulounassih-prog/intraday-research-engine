from pathlib import Path

import pandas as pd

from intraday_research_engine.analysis.metrics import compute_performance_metrics
from intraday_research_engine.backtest.vectorized import run_vectorized_backtest
from intraday_research_engine.data.load import load_price_data
from intraday_research_engine.features.returns import add_returns
from intraday_research_engine.features.rolling import add_rolling_features
from intraday_research_engine.features.signals import add_mean_reversion_signal


def prepare_backtest_data(
    data: pd.DataFrame,
    window: int,
    threshold: float,
    transaction_cost: float,
) -> pd.DataFrame:
    data = add_returns(data)
    data = add_rolling_features(data, window=window)

    data = add_mean_reversion_signal(
        data,
        zscore_col=f"zscore_{window}",
        threshold=threshold,
    )

    data = run_vectorized_backtest(
        data,
        signal_col="mean_reversion_signal",
        return_col="simple_return",
        transaction_cost=transaction_cost,
    )

    return data


def compute_metrics_table(data: pd.DataFrame) -> pd.DataFrame:
    strategy_metrics = compute_performance_metrics(
        data,
        return_col="strategy_return",
        position_col="position",
        periods_per_year=252,
    )

    buy_hold_metrics = compute_performance_metrics(
        data,
        return_col="simple_return",
        position_col=None,
        periods_per_year=252,
    )

    return pd.DataFrame(
        {
            "strategy": strategy_metrics,
            "buy_and_hold": buy_hold_metrics,
        }
    )


def main() -> None:
    input_file = Path("data/SPY_1d_2020-01-01_2024-01-01.csv")
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    window = 20
    threshold = 2.0
    transaction_cost = 0.0005

    data = load_price_data(input_file)

    data = prepare_backtest_data(
        data=data,
        window=window,
        threshold=threshold,
        transaction_cost=transaction_cost,
    )

    in_sample_data = data[data["Date"] < "2023-01-01"].copy()
    out_of_sample_data = data[data["Date"] >= "2023-01-01"].copy()

    in_sample_metrics = compute_metrics_table(in_sample_data)
    out_of_sample_metrics = compute_metrics_table(out_of_sample_data)

    in_sample_metrics.to_csv(output_dir / "in_sample_metrics.csv")
    out_of_sample_metrics.to_csv(output_dir / "out_of_sample_metrics.csv")

    print("In-sample metrics")
    print(in_sample_metrics)
    print()
    print("Out-of-sample metrics")
    print(out_of_sample_metrics)


if __name__ == "__main__":
    main()