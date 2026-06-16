from pathlib import Path

import pandas as pd

from intraday_research_engine.analysis.metrics import compute_performance_metrics
from intraday_research_engine.backtest.vectorized import run_vectorized_backtest
from intraday_research_engine.data.load import load_price_data
from intraday_research_engine.features.returns import add_returns
from intraday_research_engine.features.rolling import add_rolling_features
from intraday_research_engine.features.signals import add_mean_reversion_signal


def main() -> None:
    input_file = Path("data/SPY_1d_2020-01-01_2024-01-01.csv")
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    windows = [10, 20, 50]
    thresholds = [0.5, 1.0, 1.5, 2.0]

    base_data = load_price_data(input_file)
    base_data = add_returns(base_data)

    results = []

    for window in windows:
        for threshold in thresholds:
            data = base_data.copy()

            data = add_rolling_features(data, window=window)
            zscore_col = f"zscore_{window}"

            data = add_mean_reversion_signal(
                data,
                zscore_col=zscore_col,
                threshold=threshold,
            )

            data = run_vectorized_backtest(
                data,
                signal_col="mean_reversion_signal",
                return_col="simple_return",
                transaction_cost=0.0005,
            )

            metrics = compute_performance_metrics(
                data,
                return_col="strategy_return",
                position_col="position",
                periods_per_year=252,
            )

            row = {
                "window": window,
                "threshold": threshold,
                **metrics,
            }

            results.append(row)

    results = pd.DataFrame(results)
    results = results.sort_values("sharpe_ratio", ascending=False)

    output_file = output_dir / "parameter_sweep.csv"
    results.to_csv(output_file, index=False)

    print(results)
    print()
    print(f"Parameter sweep saved to: {output_file}")


if __name__ == "__main__":
    main()