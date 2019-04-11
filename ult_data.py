import os
import pandas as pd

path = os.path.abspath('.')
data_path = os.path.join(path, 'data')

def get_matdata(factor_name):
    df = pd.read_csv(os.path.join(data_path, '_'.join(['S&P500', factor_name+'.csv'])))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    return df