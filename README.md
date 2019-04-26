# Contextual_Alpha

## Guide for loading Available data:
```
from ult_data import get_matdata

df = get_matdata('ALL_CAPITALIZED_FILE') # return T by K matrix data (T:date(pd.datetimeindex) K:tickers)

df = get_matdata('constituents') # return T by K logical data (T:date(pd.datetimeindex) K:tickers)

df = get_matdata('rf') # return T by 1 series of fama risk-free rate(T:date(pd.datetimeindex))
df = get_matdata('index') # return T by 1 series of S&P500 index price(T:date(pd.datetimeindex))

df = get_matdata('gic_sector_code') # return K by 3 data of Gic sector code(K:tickers)
```
## Available data:
```
{
    "index": "SPX index price",
    "constituents": "S&P500 constituents",
    "rf": "Fama French risk-free rate",
    "gic_sector_code": "GIC Sector Code(Global Industry Classification Standard)",
    
    "EXRET": "S&P500 constituents' excess return",
    "BETA_ADJ_OVERRIDABLE": "Overridable Adjusted Beta",
    "CLSPRC": "S&P500 constituents' daily close price",
    "CUR_MKT_CAP": "Current Market Capitalization",
    "ASSET_GROWTH": "Assets - 1 Year Growth",
    "5Y_GEO_GROWTH_DILUTED_EPS": "Diluted EPS - 5 Yr Geometric Growth",
    "CASH_FLOW_TO_NET_INC": "Cash Flow to Net Income",
    "ACCT_RCV_TURN": "Accounts Receivable Turnover",
    "BEST_ANALYST_RATING": "BEst Analyst Rating",
    "GOODWILL_ASSETS_%": "Goodwill to Assets %",
    "INVENT_TURN": "Inventory Turnover",
    "TOT_DEBT_TO_TOT_ASSET": "Total Debt to Total Assets",
    "GEO_GROW_SALES_PER_SH": "Sales per Share - 5 Yr Geometric Growth",
    "BEST_PE_NXT_YR": "BEst P/E Next Year",
    "TOT_ANALYST_REC": "Total Analyst Recommendations",
    "REL_SHR_PX_MOMENTUM": "Relative Share Price Momentum",
    "BEST_PX_BPS_RATIO": "BEst P/Bk",
    "PROF_MARGIN": "Profit Margin",
    "BEST_EST_LONG_TERM_GROWTH": "BEst Est Long Term Growth",
    "RETURN_ON_INV_CAPITAL": "Return on Invested Capital",
    "NET_INC_GROWTH": "Net Income - 1 Yr Growth",
    "AVERAGE_BID_ASK_SPREAD_%": "Average Bid Ask Spread Percentage",
    "GROSS_MARGIN_ADJUSTED": "Gross Margin Adjusted",
    "PE_RATIO": "Price Earnings Ratio (P/E)",
    "QUICK_RATIO": "Quick Ratio",
    "EQY_REC_CONS": "Recommendation Consensus",
    "GEO_GROW_CASH_OPER_ACT": "Cash from Operating Act - 5 Yr Geometric Growth",
    "ASSET_TURNOVER": "Asset Turnover",
    "PX_TO_BOOK_RATIO": "Price to Book Ratio",
    "CASH_FLOW_GROWTH": "Cash Flow - 1 Yr Growth",
    "SALES_GROWTH": "Revenue Growth Year over Year"
}
```
