import numpy as np
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def calculate_sharpe_ratio(
    daily_returns: pd.Series,
    risk_free_rate: float = 0.0,
) -> float:
    """
    Calculate the annualized Sharpe Ratio.

    Parameters
    ----------
    daily_returns : pd.Series
        Daily portfolio returns.
    risk_free_rate : float
        Annual risk-free rate (default = 0).

    Returns
    -------
    float
        Annualized Sharpe Ratio.
    """

    daily_returns = daily_returns.dropna()

    if len(daily_returns) < 2:
        return np.nan

    daily_rf = risk_free_rate / TRADING_DAYS_PER_YEAR
    excess_returns = daily_returns - daily_rf

    mean_daily = excess_returns.mean()
    std_daily = excess_returns.std(ddof=1)

    if np.isclose(std_daily, 0):
        return np.nan

    return (mean_daily / std_daily) * np.sqrt(TRADING_DAYS_PER_YEAR)


def calculate_cumulative_return(
    daily_returns: pd.Series,
) -> float:
    """
    Calculate cumulative portfolio return.

    CR = Π(1 + Rt) - 1
    """

    daily_returns = daily_returns.dropna()

    if daily_returns.empty:
        return np.nan

    return (1.0 + daily_returns).prod() - 1.0


def calculate_cagr(
    daily_returns: pd.Series,
) -> float:
    """
    Calculate Compound Annual Growth Rate (CAGR).
    """

    daily_returns = daily_returns.dropna()

    if daily_returns.empty:
        return np.nan

    cumulative_return = calculate_cumulative_return(
        daily_returns
    )

    years = len(daily_returns) / TRADING_DAYS_PER_YEAR

    if years <= 0:
        return np.nan

    # Prevent invalid power operation
    if cumulative_return <= -1:
        return np.nan

    return (1 + cumulative_return) ** (1 / years) - 1


def calculate_all_metrics(
    daily_returns: pd.Series,
) -> dict:
    """
    Compute all required performance metrics.
    """

    sharpe = calculate_sharpe_ratio(daily_returns)
    cumulative = calculate_cumulative_return(daily_returns)
    cagr = calculate_cagr(daily_returns)

    return {
        "Sharpe Ratio": sharpe,
        "Cumulative Return": cumulative,
        "CAGR": cagr,
        "Trading Days": len(daily_returns),
    }