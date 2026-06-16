from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def add_drawdown(data: pd.DataFrame, curve_col: str, output_col: str) -> pd.DataFrame:
    data = data.copy()

    running_max = data[curve_col].cummax()
    data[output_col] = data[curve_col] / running_max - 1

    return data


def main() -> None:
    input_file = Path("reports/backtest_results.csv")
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(input_file)
    data["Date"] = pd.to_datetime(data["Date"])

    data = add_drawdown(data, "equity_curve", "strategy_drawdown")
    data = add_drawdown(data, "buy_and_hold_curve", "buy_hold_drawdown")

    plt.figure(figsize=(10, 6))
    plt.plot(data["Date"], data["equity_curve"], label="Mean reversion strategy")
    plt.plot(data["Date"], data["buy_and_hold_curve"], label="Buy and hold")
    plt.title("Equity Curve: Strategy vs Buy and Hold")
    plt.xlabel("Date")
    plt.ylabel("Portfolio value")
    plt.legend()
    plt.grid(True)

    equity_file = output_dir / "equity_curve.png"
    plt.savefig(equity_file, dpi=150, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(data["Date"], data["strategy_drawdown"], label="Mean reversion strategy")
    plt.plot(data["Date"], data["buy_hold_drawdown"], label="Buy and hold")
    plt.title("Drawdown: Strategy vs Buy and Hold")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.grid(True)

    drawdown_file = output_dir / "drawdown.png"
    plt.savefig(drawdown_file, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Figure saved to: {equity_file}")
    print(f"Figure saved to: {drawdown_file}")


if __name__ == "__main__":
    main()