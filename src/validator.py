import pandas as pd
def validate_index(prices, market_caps):
        
    #Check whether both datasets have identical datetime indices.
    if not prices.index.equals(market_caps.index):
        raise ValueError("Price and Market Cap indices do not match.")
    print("✓ Date indices match.")
    
def validate_columns(prices, market_caps):
    
    #Ensure both datasets contain identical stocks.
    if not prices.columns.equals(market_caps.columns):
        raise ValueError("Stock columns do not match.")
    print("✓ Stock columns match.")

def validate_missing(prices, market_caps):
    
    #Check for missing values.
    if prices.isna().any().any():
        raise ValueError("Missing values found in prices.")
    if market_caps.isna().any().any():
        raise ValueError("Missing values found in market caps.")
    print("✓ No missing values.")
    
def validate_duplicates(prices, market_caps):
    
    #Check for duplicate dates.
    if prices.index.has_duplicates:
        raise ValueError("Duplicate dates found in prices.")
    if market_caps.index.has_duplicates:
        raise ValueError("Duplicate dates found in market caps.")
    print("✓ No duplicate dates.")

def validate_sorted(prices, market_caps):
    
    #Ensure dates are sorted.
    if not prices.index.is_monotonic_increasing:
        raise ValueError("Price dates are not sorted.")
    if not market_caps.index.is_monotonic_increasing:
        raise ValueError("Market cap dates are not sorted.")
    print("✓ Dates are sorted.")

def validate_prices(prices):
    
    #Ensure prices are positive.
    if (prices <= 0).any().any():
        raise ValueError("Non-positive prices detected.")
    print("✓ Prices are positive.")

def validate_market_caps(market_caps):
   
    #Ensure market caps are positive.
    if (market_caps <= 0).any().any():
        raise ValueError("Non-positive market caps detected.")
    print("✓ Market caps are positive.")

def validate_data(prices, market_caps):
    validate_index(prices, market_caps)
    validate_columns(prices, market_caps)
    validate_missing(prices, market_caps)
    validate_duplicates(prices, market_caps)
    validate_sorted(prices, market_caps)
    validate_prices(prices)
    validate_market_caps(market_caps)

    print("\nAll validation checks passed!")