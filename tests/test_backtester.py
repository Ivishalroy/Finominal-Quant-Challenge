from src.data_loader import load_data
from src.backtester import Backtester

prices, market_caps = load_data(
    "data/prices.csv",
    "data/market_caps.csv"
)

backtester = Backtester(prices, market_caps)

# First rebalance date
assert backtester.rebalance_dates[0].strftime("%Y-%m-%d") == "2006-01-02"

# Tcalc
calc = backtester.get_calculation_date(
    backtester.rebalance_dates[0]
)

assert calc.strftime("%Y-%m-%d") == "2005-12-30"

print("✅ Backtester Calendar Test Passed")