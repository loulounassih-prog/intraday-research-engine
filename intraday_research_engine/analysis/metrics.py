import numpy as np
import pandas as pd


def compute_performance_metrics(
    data: pd.DataFrame,
    return_col: str = "strategy_return",
    position_col: str | None = "position",
    periods_per_year: int = 252,
) -> dict:
    returns = data[return_col].dropna()

    total_return = (1 + returns).prod() - 1
    annualized_return = (1 + total_return) ** (periods_per_year / len(returns)) - 1
    annualized_volatility = returns.std() * np.sqrt(periods_per_year)

    if annualized_volatility == 0:
        sharpe_ratio = np.nan
    else:
        sharpe_ratio = annualized_return / annualized_volatility

    equity_curve = (1 + returns).cumprod()
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1
    max_drawdown = drawdown.min()

    hit_rate = (returns > 0).mean()

    metrics = {
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "hit_rate": hit_rate,
    }

    if position_col is not None and position_col in data.columns:
        positions = data[position_col].fillna(0)

        active_returns = data.loc[positions != 0, return_col].dropna()
        active_hit_rate = (active_returns > 0).mean()

        exposure = (positions != 0).mean()
        turnover = positions.diff().abs().sum()

        metrics["active_hit_rate"] = active_hit_rate
        metrics["exposure"] = exposure
        metrics["turnover"] = turnover

    return metrics