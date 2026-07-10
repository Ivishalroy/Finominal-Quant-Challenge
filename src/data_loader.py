import pandas as pd


def load_data(price_path, marketcap_path):
    
    #Load price and market capitalization datasets.
   
    # Prices (DD-MM-YYYY)
    prices = pd.read_csv(price_path)

    prices["date"] = pd.to_datetime(prices["date"],format="%d-%m-%Y")
    prices.set_index("date", inplace=True)

    # Market Caps (YYYY-MM-DD)
    market_caps = pd.read_csv(marketcap_path)

    market_caps["date"] = pd.to_datetime(market_caps["date"],format="%Y-%m-%d")
    market_caps.set_index("date", inplace=True)

    return prices, market_caps