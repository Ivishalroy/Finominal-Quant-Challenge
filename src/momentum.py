import pandas as pd

def calculate_momentum(prices: pd.DataFrame,
                       calculation_date: pd.Timestamp,
                       lookback: int) -> pd.Series:
    """
    Calculate momentum scores for all stocks.
    Momentum = (Current Price / Lookback Price) - 1
    
    Parameters:-
    prices : DataFrame
        Daily closing prices.
    calculation_date : Timestamp
        Tcalc (previous trading day).
    lookback : int
        Lookback window in trading days.

    Returns:-
    pandas.Series
        Momentum score for every stock.
    """

    # Locate calculation date
    current_idx = prices.index.get_loc(calculation_date)

    # Locate lookback date
    lookback_idx = current_idx - lookback

    if lookback_idx < 0:
        raise ValueError(
            f"Not enough history for {lookback}-day lookback."
        )

    current_prices = prices.iloc[current_idx]
    past_prices = prices.iloc[lookback_idx]

    momentum = (current_prices / past_prices) - 1

    return momentum

def rank_stocks(momentum_scores: pd.Series) -> pd.Series:
    
    #Rank stocks by descending momentum.
    #Rank 1 = Highest Momentum

    return (momentum_scores.rank(ascending=False,method="first").astype(int))


def top_n_stocks(momentum_scores: pd.Series,
                 n: int = 10) -> pd.Series:
    
    #Return top N momentum stocks.
     return momentum_scores.sort_values(
        ascending=False
    ).head(n)