import numpy as np
import pandas as pd
import json

raw_df = pd.read_csv('Raw_S&P500_histdata.csv')
ticker_list = [x[0].split(' ')[0] for x in 
    pd.read_csv('ticker_list.csv', header=None).values]
df = raw_df.pivot(index='datadate', columns='tic', values='prccd')
# for x in df.columns:
#     if x in ticker_list:
#         continue
#     else:
#         print(x)
df = df.loc[:,[x in ticker_list for x in df.columns]]
df = df.reset_index().rename(columns={'index':'Date'})
df.to_csv('_'.join(['S&P500', 'clsprc.csv']), index=False)

