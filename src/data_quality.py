import pandas as pd


class DataQualityReport:
    """
    Analyze the quality of the input dataset without modifying it.
    """

    def __init__(
        self,
        prices: pd.DataFrame,
        market_caps: pd.DataFrame
    ):
        self.prices = prices
        self.market_caps = market_caps

    # ---------------------------------------------------
    # Dataset Summary
    # ---------------------------------------------------
    def dataset_summary(self):

        print("\n")
        print("=" * 80)
        print("DATASET SUMMARY")
        print("=" * 80)

        print(f"Trading Days        : {len(self.prices)}")
        print(f"Stocks              : {len(self.prices.columns)}")
        print(f"Start Date          : {self.prices.index.min().date()}")
        print(f"End Date            : {self.prices.index.max().date()}")

        print()

        print(f"Missing Prices      : {self.prices.isna().sum().sum()}")
        print(f"Missing Market Caps : {self.market_caps.isna().sum().sum()}")

        print(f"Duplicate Dates     : {self.prices.index.duplicated().sum()}")

        print(
            f"Negative Prices     : {(self.prices <= 0).sum().sum()}"
        )

        print(
            f"Negative MarketCaps : {(self.market_caps <= 0).sum().sum()}"
        )

    # ---------------------------------------------------
    # Stock Quality
    # ---------------------------------------------------
    def stock_quality_report(self):

        daily_returns = self.prices.pct_change().dropna()

        report = []

        for stock in daily_returns.columns:

            r = daily_returns[stock]

            report.append(
                {
                    "Stock": stock,
                    "Mean Return": r.mean(),
                    "Std Dev": r.std(),
                    "Maximum Return": r.max(),
                    "Minimum Return": r.min(),
                    "Returns >20%": (r > 0.20).sum(),
                    "Returns >50%": (r > 0.50).sum(),
                    "Returns >100%": (r > 1.00).sum(),
                    "Returns <-20%": (r < -0.20).sum(),
                    "Returns <-50%": (r < -0.50).sum(),
                }
            )

        report = pd.DataFrame(report)

        report = report.sort_values(
            "Returns >100%",
            ascending=False
        )

        report.to_csv(
            "stock_quality_report.csv",
            index=False
        )

        print("\n")
        print("=" * 80)
        print("TOP 10 MOST VOLATILE STOCKS")
        print("=" * 80)

        print(report.head(10))

        print("\nSaved -> stock_quality_report.csv")

        return report

    # ---------------------------------------------------
    # Extreme Return Report
    # ---------------------------------------------------
    def extreme_return_report(
        self,
        threshold=1.0
    ):

        returns = self.prices.pct_change()

        rows = []

        for stock in returns.columns:

            extreme = returns[stock].abs() > threshold

            for date in returns.index[extreme]:

                idx = self.prices.index.get_loc(date)

                if idx == 0:
                    continue

                rows.append(
                    {
                        "Date": date,
                        "Stock": stock,
                        "Return": returns.loc[date, stock],
                        "Price Before": self.prices.iloc[idx-1][stock],
                        "Price After": self.prices.iloc[idx][stock]
                    }
                )

        report = pd.DataFrame(rows)

        report.sort_values(
            "Return",
            key=lambda x: x.abs(),
            ascending=False,
            inplace=True
        )

        report.to_csv(
            "extreme_returns.csv",
            index=False
        )

        print("\n")
        print("=" * 80)
        print("LARGEST EXTREME RETURNS")
        print("=" * 80)

        print(report.head(20))

        print()

        print(f"Extreme Events : {len(report)}")

        print("Saved -> extreme_returns.csv")

        return report

    # ---------------------------------------------------
    # Run Everything
    # ---------------------------------------------------
    def generate(self):

        self.dataset_summary()

        self.stock_quality_report()

        self.extreme_return_report()