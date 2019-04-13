import numpy as np
import pandas as pd

raw_df = pd.read_csv('S&P_sector_code.csv')
raw_df = raw_df.drop_duplicates(subset='tic', keep='first')
df = raw_df.set_index('tic')[['gsector', 'gind', 'gsubind']]
df = df.reset_index().rename(columns={
    'index':'Ticker',
    'gsector':'Gsector', # GIC Level1
    'gind':'Gind',       # GIC Level2
    'gsubind':'Gsubind', # GIC Level3
    })
file_name = 'GIC_sector_code'
df.to_csv('_'.join(['S&P500', file_name+'.csv']), index=False)

