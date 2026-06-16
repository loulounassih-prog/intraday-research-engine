from pathlib import Path

from intraday_research_engine.data.load import load_price_data
from intraday_research_engine.features.returns import add_returns
from intraday_research_engine.features.rolling import add_rolling_features
from intraday_research_engine.features.signals import add_mean_reversion_signal
from intraday_research_engine.backtest.vectorized import run_vectorized_backtest
from intraday_research_engine.analysis.metrics import compute_performance_metrics


if __name__ == "__main__":
    file_path = Path("data/SPY_1d_2020-01-01_2024-01-01.csv")

    data = load_price_data(file_path)
    data = add_returns(data)
    data = add_rolling_features(data, window=20)
    data = add_mean_reversion_signal(data, zscore_col="zscore_20", threshold=1.0)
    data = run_vectorized_backtest(data)

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

    print("Strategy metrics")
    for key, value in strategy_metrics.items():
        print(f"{key}: {value:.4f}")

    print()
    print("Buy and hold metrics")
    for key, value in buy_hold_metrics.items():
        print(f"{key}: {value:.4f}")