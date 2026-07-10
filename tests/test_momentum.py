from src.data_loader import load_data
from src.validator import validate_data
from src.momentum import calculate_momentum, rank_stocks

prices, market_caps = load_data(
    "data/prices.csv",
    "data/market_caps.csv"
)

validate_data(prices, market_caps)

calc_date = prices.index[300]

momentum = calculate_momentum(
    prices,
    calc_date,
    lookback=63
)

ranks = rank_stocks(momentum)

print("\nTop 10 Momentum Stocks")
print(momentum.sort_values(ascending=False).head(10))

print("\nTop 10 Ranks")
print(ranks.sort_values().head(10))

assert len(momentum) == prices.shape[1]
assert ranks.min() == 1
assert ranks.max() == len(prices.columns)

print("\n✅ Momentum Test Passed")