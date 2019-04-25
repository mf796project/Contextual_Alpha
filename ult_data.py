import os
import pandas as pd

path = os.path.abspath('.')
data_path = os.path.join(path, 'data')
res_path = os.path.join(path, 'result')

def get_matdata(factor_name):
    df = pd.read_csv(os.path.join(data_path, '_'.join(['S&P500', factor_name+'.csv'])))
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        return df.set_index('Date')
    except:
        return df.set_index(df.columns[0])