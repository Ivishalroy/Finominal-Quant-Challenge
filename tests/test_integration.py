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

portfolio = None

print("=" * 80)
print("SYSTEM INTEGRATION TEST")
print("=" * 80)

for month, rebalance_date in enumerate(backtester.rebalance_dates[:3], start=1):

    calc_date = backtester.get_calculation_date(rebalance_date)

    momentum = calculate_momentum(
        prices,
        calc_date,
        lookback=backtester.lookback
    )

    ranks = rank_stocks(momentum)

    portfolio = backtester.build_portfolio(
        portfolio,
        ranks
    )

    weights = backtester.calculate_weights(
        portfolio,
        calc_date
    )

    print(f"\nMonth {month}")
    print(f"Rebalance Date : {rebalance_date.date()}")
    print(f"Calculation Date : {calc_date.date()}")

    print("\nPortfolio")
    for stock in portfolio:
        print(f"{stock:<10} Rank: {ranks[stock]:2d}")

    print("\nWeights")
    print(weights.sort_values(ascending=False))

    assert len(portfolio) == backtester.portfolio_size
    assert abs(weights.sum() - 1.0) < 1e-10
    assert weights.max() <= backtester.weight_cap + 1e-10

print("\n✅ Integration Test Passed")