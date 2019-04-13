import numpy as np
import pandas as pd
import json

raw_df = pd.read_csv('CUR_MKT_CAP.csv')

file_name = raw_df.iloc[4,1]
file_mean = raw_df.iloc[3,1]

# columns
ticker_list = [i.split(' ')[0] for i in raw_df.iloc[2,1:].values]
# index
date = pd.to_datetime(raw_df.iloc[5:,0].values)
# cleaned dataframe
df = pd.DataFrame(
    data=raw_df.iloc[5:,1:].values, 
    index=date, 
    columns=ticker_list)
if file_name == 'PX_CLOSE_1D':
    df = df.shift(-1) # price yesterday to today 
df = df[~pd.isnull(df.index)]
df = df.loc[:,~df.columns.duplicated()]
df = df.reindex(sorted(df.columns), axis=1)
df = df.reset_index().rename(columns={'index':'Date'})
df.to_csv('_'.join(['S&P500', file_name+'.csv']), index=False)


