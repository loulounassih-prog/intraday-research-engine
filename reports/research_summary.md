# Research Summary

## Objective

The objective of this project is to build a reproducible research pipeline for testing simple quantitative trading signals. The focus is not to optimize a profitable strategy, but to implement a clean workflow including data loading, feature engineering, signal generation, backtesting, transaction costs, parameter comparison, and out-of-sample validation.

## Dataset

The experiment uses daily SPY data from 2020-01-01 to 2024-01-01.

The dataset contains OHLCV data with adjusted prices downloaded from Yahoo Finance.

## Signal

The tested signal is a simple mean reversion signal based on the z-score of the closing price relative to its rolling mean.

A long position is taken when the price is significantly below its rolling mean.

A short position is taken when the price is significantly above its rolling mean.

The selected configuration is:

- rolling window: 20 days
- z-score threshold: 2.0
- transaction cost: 0.05% per unit of position change

## Methodology

The signal is evaluated with a vectorized backtest.

To avoid look-ahead bias, the signal computed at time t is shifted by one period before being applied to returns.

The project also includes a parameter sweep over several rolling windows and z-score thresholds. The best configuration from the exploratory period is then evaluated on a separate test period.

Train/test split:

- Train period: 2020-2022
- Test period: 2023

## Results

### Train period

The strategy performs well on the train period.

It achieves a total return of approximately 30.5%, with an annualized Sharpe ratio of approximately 1.08 and a maximum drawdown of around -5.3%.

The exposure is low, around 8.3%, meaning the strategy is only active during a small fraction of the period.

### Test period

The strategy does not generalize well to the test period.

On 2023, the strategy has a slightly negative total return of approximately -0.9%, while buy and hold returns approximately 26.2%.

The out-of-sample Sharpe ratio is negative.

## Interpretation

The train results suggest that extreme mean reversion signals may look attractive in some market regimes, especially when the strategy is very selective.

However, the test results show that this simple z-score mean reversion signal is not robust enough to be considered reliable.

The strategy appears regime-dependent and does not capture the strong upward trend observed in 2023.

## Conclusion

This experiment does not provide evidence of a robust standalone trading strategy.

However, the research pipeline is functional and includes important components of a serious quantitative research workflow:

- clean data loading
- feature engineering
- signal generation
- vectorized backtesting
- transaction costs
- performance metrics
- parameter sweep
- train/test validation

The main conclusion is that the tested mean reversion signal is fragile out-of-sample. Further research should focus on robustness checks, additional assets, different market regimes, and more realistic execution assumptions.