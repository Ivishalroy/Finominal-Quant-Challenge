from src.data_loader import load_data
from src.validator import validate_data

prices, market_caps = load_data(
    "data/prices.csv",
    "data/market_caps.csv"
)

validate_data(prices, market_caps)

print("✅ Validator Test Passed")