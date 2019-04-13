from ult_data import get_matdata

df = get_matdata('CLSPRC') # return T by K matrix data (T:date(pd.datetimeindex) K:tickers)

df = get_matdata('constituents') # return T by K logical data (T:date(pd.datetimeindex) K:tickers)

df = get_matdata('rf') # return T by 1 series of fama risk-free rate(T:date(pd.datetimeindex))
df = get_matdata('index') # return T by 1 series of S&P500 index price(T:date(pd.datetimeindex))

df = get_matdata('gic_sector_code') # return K by 3 data of Gic sector code(K:tickers)