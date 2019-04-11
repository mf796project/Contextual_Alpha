import os
import pandas as pd

# path
path = os.path.abspath('.')
data_path = os.path.join(path, 'data')
rawdata_path = os.path.join(path, 'rawdata')

wrds_sp500_cons_name = 'RaW_S&P500_constituents.csv'
wrds_sp500_cons_path = os.path.join(data_path, wrds_sp500_cons_name)

wrds_sp500_hist_name = 'Raw_S&P500_histdata.csv'
wrds_sp500_hist_path = os.path.join(data_path, wrds_sp500_hist_name)

wrds_sp500_ticker_name = 'ticker_list.txt'
wrds_sp500_ticker_list_path = os.path.join(data_path, wrds_sp500_ticker_name)

bb_sp500_ticker_name = 'ticker_list.csv'
bb_sp500_ticker_list_path = os.path.join(data_path, bb_sp500_ticker_name)

sp500_cons_name = 'S&P500_constituents.csv'
sp500_cons_path = os.path.join(data_path, sp500_cons_name)

factor_paths = [os.path.join(rawdata_path, i) for i in os.listdir(rawdata_path) if i.endswith('.csv')]
mat_paths = [os.path.join(data_path, i) for i in os.listdir(data_path) if i.startswith('S&P500')]



