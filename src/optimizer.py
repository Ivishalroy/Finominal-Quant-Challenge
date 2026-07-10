import pandas as pd

from src.backtester import Backtester
from src.metrics import calculate_all_metrics


LOOKBACKS = [21, 63, 126, 189, 252]


def optimize_lookback(prices, market_caps):
    """
    Run the complete backtest for each lookback period and
    return a DataFrame of performance metrics.
    """

    results = []

    for lookback in LOOKBACKS:

        print(f"Running Lookback = {lookback}")

        backtester = Backtester(
            prices,
            market_caps,
            lookback=lookback
        )

        daily_returns = backtester.run()

        metrics = calculate_all_metrics(daily_returns)

        results.append({
            "Lookback": lookback,
            "Sharpe Ratio": metrics["Sharpe Ratio"],
            "Cumulative Return": metrics["Cumulative Return"],
            "CAGR": metrics["CAGR"]
        })

    results = pd.DataFrame(results)

    results = results.sort_values(
        by="Sharpe Ratio",
        ascending=False
    ).reset_index(drop=True)

    return results