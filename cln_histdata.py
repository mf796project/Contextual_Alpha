from cln_ult import wrds_sp500_hist_path, bb_sp500_ticker_list_path
import numpy as np
import pandas as pd
import json
import os

raw_df = pd.read_csv(wrds_sp500_hist_path)
ticker_list = [x[0].split(' ')[0] for x in 
    pd.read_csv(bb_sp500_ticker_list_path, header=None).values]
df = raw_df.pivot(index='datadate', columns='tic', values='prccd')
df = df.loc[:,[x in ticker_list for x in df.columns]]
df = df.reset_index().rename(columns={'index':'Date'})
df.to_csv('_'.join(['S&P500', 'clsprc.csv']), index=False)

