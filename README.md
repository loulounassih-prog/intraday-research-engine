# Intraday Research Engine

A small quantitative research pipeline for testing simple market signals on historical price data.

The goal of this project is not to claim a profitable trading strategy. The goal is to build a clean and reproducible research workflow: data loading, feature engineering, signal generation, backtesting, transaction costs, performance metrics, parameter comparison, and out-of-sample validation.

## Research Question

Can a simple mean reversion signal based on the z-score of SPY prices produce robust results after transaction costs?

## Dataset

The current experiment uses daily SPY OHLCV data downloaded from Yahoo Finance.

* Asset: SPY
* Frequency: daily
* Period: 2020-01-01 to 2024-01-01
* Prices: adjusted prices from Yahoo Finance

## Signal

The tested signal is a simple mean reversion rule based on the z-score of the closing price relative to its rolling mean.

```text
zscore = (Close - rolling_mean) / rolling_std
```

Trading rule:

```text
zscore < -threshold  -> long
zscore >  threshold  -> short
otherwise            -> flat
```

The intuition is that when the price is far below its recent average, the strategy expects a short-term rebound. When the price is far above its recent average, the strategy expects a short-term reversal.

## Backtest Methodology

The backtest is vectorized and includes transaction costs.

To avoid look-ahead bias, the signal computed at time `t` is shifted by one period before being applied to returns.

```text
signal at time t
        ↓
position at time t+1
        ↓
strategy return at time t+1
```

Transaction costs are applied when the position changes.

The current transaction cost assumption is:

```text
0.05% per unit of position change
```

For example:

```text
0  ->  1     cost = 0.05%
1  ->  0     cost = 0.05%
1  -> -1     cost = 0.10%
```

## Metrics

The project computes the following metrics:

* total return
* annualized return
* annualized volatility
* Sharpe ratio
* maximum drawdown
* hit rate
* active hit rate
* exposure
* turnover

The `active_hit_rate` only considers periods where the strategy has an active position. This is more informative than the raw hit rate for a strategy that is often flat.

## Parameter Comparison

A small parameter sweep is included to check whether the signal behaves consistently across reasonable parameter choices.

Tested parameters:

```text
rolling window ∈ {10, 20, 50}
threshold      ∈ {0.5, 1.0, 1.5, 2.0}
```

This is not meant to aggressively optimize the strategy. It is used as a basic robustness check.

The best in-sample configuration found in the current experiment is:

```text
rolling window = 20
threshold      = 2.0
```

## In-Sample / Out-of-Sample Validation

The experiment uses a simple in-sample / out-of-sample split.

```text
2020-2022  -> in-sample period
2023       -> out-of-sample period
```

The in-sample period is used for exploration and parameter comparison.

The out-of-sample period is used to check whether the selected configuration generalizes to unseen market data.

## Results

### In-Sample Period: 2020-2022

The selected strategy performs well in-sample.

Approximate results:

```text
Strategy total return:        +30.5%
Strategy Sharpe ratio:         1.08
Strategy max drawdown:        -5.3%
Strategy exposure:             8.3%
```

### Out-of-Sample Period: 2023

The selected strategy does not generalize well out-of-sample.

Approximate results:

```text
Strategy total return:         -0.9%
Strategy Sharpe ratio:         -0.30
Buy and hold total return:    +26.2%
```

The strategy is almost flat to slightly negative, while buy and hold performs strongly.

## Interpretation

The in-sample results suggest that extreme mean reversion signals may look attractive in some market regimes, especially when the strategy is highly selective.

However, the out-of-sample results show that this simple z-score mean reversion signal is not robust enough to be considered reliable as a standalone trading strategy.

The strategy appears regime-dependent and fails to capture the strong upward trend observed in 2023.

## Conclusion

This project does not claim to find a robust profitable strategy.

The main result is methodological: the project demonstrates a reproducible quantitative research workflow and shows that a simple SPY mean reversion signal can look attractive in-sample but fail to generalize out-of-sample.

The tested signal is fragile and should not be considered reliable without further robustness checks.

## Project Structure

```text
intraday-research-engine/
│
├── data/
├── reports/
├── scripts/
├── tests/
│
├── intraday_research_engine/
│   ├── data/
│   ├── features/
│   ├── backtest/
│   └── analysis/
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Usage

Install dependencies:

```powershell
python -m pip install -r requirements.txt
python -m pip install -e .
```

Download the data:

```powershell
python scripts/download_data.py
```

Run the main research pipeline:

```powershell
python scripts/run_research.py
```

Run the parameter sweep:

```powershell
python scripts/run_parameter_sweep.py
```

Run the out-of-sample validation:

```powershell
python scripts/run_oos_validation.py
```

Generate plots:

```powershell
python scripts/plot_results.py
```

## Outputs

The scripts generate result files in the `reports/` directory.

```text
reports/
├── backtest_results.csv
├── metrics.csv
├── parameter_sweep.csv
├── in_sample_metrics.csv
├── out_of_sample_metrics.csv
├── equity_curve.png
└── drawdown.png
```

## Possible Extensions

Possible extensions include:

* testing more assets
* testing other market regimes
* using intraday data
* adding walk-forward validation
* improving transaction cost assumptions
* comparing several signal families
* adding volatility targeting
* adding risk-adjusted position sizing
* writing unit tests for the backtest engine
