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

    data = load_price_data(input_file)
    data = add_returns(data)

    window = 20
    threshold = 2.0

    data = add_rolling_features(data, window=window)
    data = add_mean_reversion_signal(
        data,
        zscore_col="zscore_20",
        threshold=threshold,
    )
    data = run_vectorized_backtest(
        data,
        signal_col="mean_reversion_signal",
        return_col="simple_return",
        transaction_cost=0.0005,
    )

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

    metrics = pd.DataFrame(
        {
            "strategy": strategy_metrics,
            "buy_and_hold": buy_hold_metrics,
        }
    )

    data.to_csv(output_dir / "backtest_results.csv", index=False)
    metrics.to_csv(output_dir / "metrics.csv")

    print("Research run completed.")
    print(f"Backtest results saved to: {output_dir / 'backtest_results.csv'}")
    print(f"Metrics saved to: {output_dir / 'metrics.csv'}")
    print()
    print(metrics)


if __name__ == "__main__":
    main()