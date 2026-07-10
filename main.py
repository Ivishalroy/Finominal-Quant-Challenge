from src.data_loader import load_data
from src.data_quality import DataQualityReport
from src.validator import validate_data
from src.optimizer import optimize_lookback


prices, market_caps = load_data(
    "data/prices.csv",
    "data/market_caps.csv"
)

validate_data(
    prices,
    market_caps
)

quality = DataQualityReport(
    prices,
    market_caps
)

quality.generate()

results = optimize_lookback(
    prices,
    market_caps
)

print("\n")
print("=" * 80)
print("LOOKBACK OPTIMIZATION RESULTS")
print("=" * 80)

print(results)

best = results.iloc[0]

print("\n")
print("=" * 80)
print("BEST STRATEGY")
print("=" * 80)

print(f"Optimal Lookback : {best['Lookback']} Days")
print(f"Sharpe Ratio     : {best['Sharpe Ratio']:.4f}")
print(f"Cumulative Return: {best['Cumulative Return']:.2%}")
print(f"CAGR             : {best['CAGR']:.2%}")