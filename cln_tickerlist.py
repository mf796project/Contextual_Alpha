from ult_data import wrds_sp500_cons_path
import os
import pandas as pd

start_date = pd.to_datetime('1990/01/01')
# create ticker_list for S&P500 for data downloading
wrds_sp500_cons = pd.read_csv(wrds_sp500_cons_path)
inperiod_loc = -(pd.to_datetime(wrds_sp500_cons['thru']) < start_date)
wrds_sp500_cons = wrds_sp500_cons[inperiod_loc]
ticker_list = wrds_sp500_cons['co_tic'].dropna().values
ticker_list = list(set(ticker_list))
# csv for BB
with open('ticker_list.csv', 'w') as f:
    for ticker in ticker_list:
        f.write(ticker+' US Equity\n')

# txt for WRDS
with open('ticker_list.txt', 'w') as f:
    for ticker in ticker_list:
        f.write(ticker+'\n')  

