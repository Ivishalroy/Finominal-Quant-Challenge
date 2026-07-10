## Submission Contents

- README.md – Project overview and execution instructions
- RESEARCH_NOTE.pdf – Methodology, implementation details, assumptions, and discussion
- RESULTS.md – Lookback optimization results
- Source code – Implementation of the momentum strategy

# Finominal Quant Challenge
## Junior Quantitative Analyst
Author: Vishal Roy

# Objective

The objective of this project is to optimize a monthly rebalanced, market-capitalization weighted momentum strategy by selecting the optimal momentum lookback period that maximizes the Annualized Sharpe Ratio.

The implementation follows the challenge specification exactly.

---

# Strategy Specification

## Universe

- 30 Stocks
- Daily closing prices
- Daily market capitalization
- Backtest Period:
    - January 2006
    - May 2026

---

## Momentum Score

Momentum is calculated as

Momentum = Price(Tcalc) / Price(Tcalc − Lookback) − 1

where

- Tcalc = Trading day immediately before the rebalance date.

---

## Portfolio Construction

At every monthly rebalance:

1. Rank all stocks by descending momentum.
2. Select the Top 10 stocks.
3. Apply the buffer rule:

- Existing holdings are retained while their rank remains ≤ 12.
- Remaining positions are filled using the highest-ranked new stocks.

---

## Portfolio Weighting

The portfolio is weighted using market capitalization.

Raw weights are computed as

weight_i = MarketCap_i / Total MarketCap

A maximum position size of 20% is enforced using iterative weight redistribution until

- No stock exceeds 20%
- Portfolio weights sum to 100%

---

## Optimization

The following lookback windows were evaluated independently:

- 21 Trading Days
- 63 Trading Days
- 126 Trading Days
- 189 Trading Days
- 252 Trading Days

The optimal lookback is selected using the highest Annualized Sharpe Ratio.

---

# Project Structure

src/

- data_loader.py
- validator.py
- momentum.py
- backtester.py
- metrics.py
- optimizer.py
- data_quality.py

tests/

- test_validator.py
- test_momentum.py
- test_weights.py
- test_integration.py

data/

- prices.csv
- market_caps.csv

main.py

---

# Validation

Before backtesting, the following checks are performed.

✓ Matching dates

✓ Matching stock universe

✓ Missing values

✓ Duplicate dates

✓ Chronological ordering

✓ Positive prices

✓ Positive market capitalizations

All validation checks passed successfully.

---

# Data Quality Assessment

A separate data quality module was implemented to inspect the supplied dataset.

The report includes

- Dataset summary
- Per-stock volatility statistics
- Extreme daily returns
- Quality reports exported as CSV

The analysis identified numerous extreme one-day price changes (many exceeding 100%), which are inconsistent with normal equity market behaviour and are likely associated with unadjusted corporate actions or vendor-specific data anomalies.

Since the challenge dataset does not include adjustment factors or corporate action metadata, the supplied data was intentionally left unchanged to preserve reproducibility and adherence to the challenge specification.

---

# Performance Metrics

The following metrics are reported

- Annualized Sharpe Ratio
- Cumulative Return
- CAGR

using daily portfolio returns.

---

# Testing

The implementation includes unit tests covering

✓ Data validation

✓ Momentum calculation

✓ Portfolio construction

✓ Weight capping

✓ System integration

---

# Limitations

The supplied dataset contains numerous discontinuous price jumps that are consistent with unadjusted corporate actions or other data quality issues.

Consequently,

- momentum rankings,
- cumulative returns,
- and CAGR

may be materially inflated.

The strategy implementation itself follows the challenge specification exactly and no manual modification of the supplied dataset was performed.

In a production quantitative research environment, adjusted price series and corporate action data would be incorporated before strategy evaluation.

---

# Technologies

Python

Pandas

NumPy

VS Code