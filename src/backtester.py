import pandas as pd

from src.momentum import (calculate_momentum, rank_stocks)


class Backtester:
    
    #Backtesting engine for the momentum strategy.
    def __init__(
        self,
        prices: pd.DataFrame,
        market_caps: pd.DataFrame,
        lookback: int = 63
    ):
        self.prices = prices
        self.market_caps = market_caps
        
         # Strategy Parameters
        self.lookback = lookback
        self.portfolio_size = 10
        self.weight_cap = 0.20

        
        # First trading day of every month
        self.rebalance_dates = self.get_rebalance_dates()

        # Strategy state
        self.current_portfolio = None
        self.current_weights = None

        # Results
        self.daily_returns = []
        self.portfolio_history = []
    
    def get_rebalance_dates(self) -> pd.DatetimeIndex:
        #Return the first trading day of every month starting from January 2006.
        # Keep only dates from 2006 onwards
        prices_2006 = self.prices[
            self.prices.index >= "2006-01-01"
        ]
        # First trading day of every month
        rebalance_dates = (
            prices_2006
            .groupby(
                [
                    prices_2006.index.year,
                    prices_2006.index.month
                ]
            )
            .apply(lambda x: x.index[0])
        )

        return pd.DatetimeIndex(rebalance_dates)
    
    def get_calculation_date(self, rebalance_date: pd.Timestamp) -> pd.Timestamp:

        #Return the trading day immediately before the rebalance date (Tcalc).
        idx = self.prices.index.get_loc(rebalance_date)

        if idx == 0:
            raise ValueError(
            "No previous trading day available."
            )

        return self.prices.index[idx - 1]

    def build_portfolio(
        self,
        previous_portfolio: list | None,
        ranks: pd.Series
    ) -> list[str]:
        # Build portfolio using the momentum buffer rule.
        if previous_portfolio is None:
            portfolio = (
                ranks
                .sort_values()
                .head(self.portfolio_size)
                .index
                .tolist()
            )

            assert len(portfolio) == self.portfolio_size
            return portfolio

        # Retain stocks ranked <= 12
        retained = [
            stock
            for stock in previous_portfolio
            if ranks.get(stock, float('inf')) <= 12
        ]

        portfolio = retained.copy()

        # Already have enough stocks
        if len(portfolio) >= self.portfolio_size:
            return portfolio[:self.portfolio_size]

        # Fill remaining slots from best-ranked stocks
        for stock in ranks.sort_values().index:
            if stock in portfolio:
                continue

            portfolio.append(stock)

            if len(portfolio) == self.portfolio_size:
                break

        assert len(portfolio) == self.portfolio_size, (
            f"Expected {self.portfolio_size} stocks,"
            f"got{len(portfolio)}."
        )

        return portfolio
    
    def calculate_weights(self, portfolio: list[str], calculation_date: pd.Timestamp, cap: float | None = None, debug: bool = False) -> pd.Series:
    
        # Calculate market-cap weights with an iterative maximum weight constraint.
        # Retrieve market capitalizations for the selected portfolio on Tcalc.
        caps = self.market_caps.loc[calculation_date, portfolio].copy()

        # Raw weights
        weights = caps / caps.sum()
        
        if debug:
            print("\nInitial Raw Weights")
            print(weights.sort_values(ascending=False))
            print("-" * 60)

        # Default weight cap
        if cap is None:
            cap = self.weight_cap

        # Iterative weight capping
        max_iterations = len(weights)

        iteration = 1
        for _ in range(max_iterations):

            # Identify overweight stocks
            overweight = weights > cap

            # Finished
            if not overweight.any():
                if debug:
                    print(f"\nConverged after {iteration-1} iteration(s).")
                break

            if debug:
                print(f"\nIteration {iteration}")
                print("Overweight Stocks:")
                print(weights[overweight])

            # Total excess
            excess = (weights[overweight] - cap).sum()

            # Cap overweight stocks
            weights[overweight] = cap

            # Remaining stocks
            underweight = weights < cap

            if not underweight.any():
                break

            remaining_caps = caps[underweight]

            redistribution = (remaining_caps / remaining_caps.sum())

            # Redistribute excess
            weights[underweight] += (redistribution * excess)

            if debug:
                print("\nWeights After Redistribution")
                print(weights.sort_values(ascending=False))
            iteration += 1
            
        # Final sanity checks
        if (weights > cap + 1e-10).any():
            raise RuntimeError("Weight capping algorithm failed to converge.")

        assert abs(weights.sum() - 1.0) < 1e-10, \
            "Weights do not sum to 1."

        return weights.sort_index()
    
    def calculate_portfolio_returns(self, portfolio: list, weights: pd.Series, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.Series:
        
        #Calculate daily portfolio returns between two dates.
        # Price data for portfolio
        portfolio_prices = self.prices.loc[
            start_date:end_date,
            portfolio
        ]

        # Daily stock returns
        daily_returns = portfolio_prices.pct_change().dropna()
        # Portfolio return
        portfolio_returns = daily_returns.dot(weights)

        return portfolio_returns
    
    def run(self)-> pd.Series:
        #Run the complete backtest.
        portfolio = None
        all_returns = []
        history = []

        for i, rebalance_date in enumerate(self.rebalance_dates):

            #print(f"Running {rebalance_date.date()}")

            # Tcalc
            calc_date = self.get_calculation_date(
                rebalance_date
            )

            # Compute momentum scores at Tcalc
            momentum = calculate_momentum(
                self.prices,
                calc_date,
                self.lookback
            )

            ranks = rank_stocks(momentum)
            
            # print(
                #f"{rebalance_date.date()} | "
                #f"Valid momentum values: {momentum.notna().sum()} / {len(momentum)}"
            #)
            
            # Construct portfolio using the buffer rule
            portfolio = self.build_portfolio(
                portfolio,
                ranks
            )

            # Compute market-cap weights with 20% cap
            weights = self.calculate_weights(
                portfolio,
                calc_date
            )

            history.append(
                {
                    "rebalance_date": rebalance_date,
                    "calculation_date": calc_date,
                    "portfolio": portfolio.copy(),
                    "weights": weights.copy()
                }
            )

           # No holding period after the final rebalance
            if i == len(self.rebalance_dates) - 1:
                break

            next_rebalance = self.rebalance_dates[i + 1]

            # First trading day AFTER we buy
            start_idx = self.prices.index.get_loc(rebalance_date) + 1
            start_date = self.prices.index[start_idx]

            # Last trading day BEFORE the next rebalance
            end_idx = self.prices.index.get_loc(next_rebalance) - 1
            end_date = self.prices.index[end_idx]

            returns = self.calculate_portfolio_returns(
                portfolio,
                weights,
                start_date,
                end_date
            )

            all_returns.append(returns)

        self.daily_returns = (
            pd.concat(all_returns)
            .sort_index()
        )

        self.portfolio_history = history

        return self.daily_returns