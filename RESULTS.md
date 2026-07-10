# Results

## Data Validation

All validation checks passed.

- Matching trading dates
- Matching stock universe
- No missing values
- No duplicate dates
- Positive prices
- Positive market capitalizations

---

## Data Quality Summary

Trading Days           : 5337

Stocks                 : 30

Period                 : 2005-01-03 to 2026-06-24

Missing Prices         : 0

Missing Market Caps    : 0

Duplicate Dates        : 0

Negative Prices        : 0

Negative Market Caps   : 0

The data quality assessment identified a substantial number of extreme one-day price movements.

These events are consistent with unadjusted corporate actions or vendor-specific anomalies and should be considered when interpreting strategy performance.

---

## Lookback Optimization

| Lookback | Sharpe Ratio | Cumulative Return | CAGR |
|-----------|-------------:|------------------:|-------:|
| 21 | 4.2407 | 1.0524e67 | 4907.03% |
| 63 | 4.3783 | 3.8081e71 | 8747.73% |
| 126 | **4.4748** | **4.0792e72** | **9968.18%** |
| 189 | 4.3642 | 2.3293e72 | 9665.25% |
| 252 | 4.3669 | 7.7899e71 | 9099.42% |

---

## Best Strategy

Optimal Lookback

126 Trading Days

Annualized Sharpe Ratio

4.4748

---

## Discussion

The 126-day lookback achieved the highest Sharpe Ratio among the evaluated momentum windows.

However, the absolute performance metrics (particularly cumulative return and CAGR) should be interpreted with caution.

The accompanying data quality analysis identified numerous extreme price discontinuities within the supplied dataset that are consistent with unadjusted corporate actions.

Because the challenge dataset does not provide adjusted prices or corporate action metadata, the strategy was implemented exactly on the supplied data without modification.

Accordingly, while the relative comparison between lookback windows remains informative, the absolute performance metrics are likely overstated.

---

## Conclusion

Among the evaluated lookback periods, the 126-day momentum strategy achieved the highest Annualized Sharpe Ratio and is therefore selected as the optimal configuration under the challenge specification.

The implementation is modular, fully tested, reproducible, and follows the prescribed portfolio construction and weighting methodology.