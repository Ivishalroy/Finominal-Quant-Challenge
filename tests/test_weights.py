from src.data_loader import load_data
from src.validator import validate_data
from src.backtester import Backtester
from src.momentum import calculate_momentum, rank_stocks

prices, market_caps = load_data(
    "data/prices.csv",
    "data/market_caps.csv"
)

validate_data(prices, market_caps)

backtester = Backtester(
    prices,
    market_caps
)

rebalance_date = backtester.rebalance_dates[0]
calc_date = backtester.get_calculation_date(rebalance_date)

momentum = calculate_momentum(
    prices,
    calc_date,
    lookback=63
)

ranks = rank_stocks(momentum)

portfolio = backtester.build_portfolio(
    None,
    ranks
)

weights = backtester.calculate_weights(
    portfolio,
    calc_date
)

print("\nPortfolio")
print(portfolio)

print("\nWeights")
print(weights.sort_values(ascending=False))

assert abs(weights.sum() - 1.0) < 1e-10
assert weights.max() <= backtester.weight_cap + 1e-10
assert len(weights) == backtester.portfolio_size

print("\n✅ Weight Test Passed")