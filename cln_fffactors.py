import numpy as np
import pandas as pd
import datetime

startdate =  pd.to_datetime('1/1/1990')
enddate = pd.to_datetime('3/25/2019')
raw_df = pd.read_csv('FF_Factors.csv')
raw_df = raw_df.rename(columns = {'Unnamed: 0':'Date'})
raw_df[['Date']] = raw_df[['Date']].apply(
    lambda x:pd.to_datetime(x, format='%Y%m'))
raw_df_index = raw_df['Date']
loc = ((raw_df_index >= startdate)&(raw_df_index <= enddate)).values
cln_df = pd.Series(
    index = pd.date_range(start=startdate, end=enddate, freq=pd.offsets.BMonthEnd()),
    name = 'RF',
    data = raw_df[loc]['RF'].values,
)
cln_df = cln_df.reset_index().rename(columns={'index':'Date'})
file_name = 'rf'
cln_df.to_csv('_'.join(['S&P500', file_name+'.csv']), index=False)
