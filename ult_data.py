import os
import numpy as np
import pandas as pd

path = os.path.abspath('.')
data_path = os.path.join(path, 'mat_data')
res_path = os.path.join(path, 'result')
cont_path = os.path.join(path, 'context_data')

def get_matdata(factor_name):
    df = pd.read_csv(os.path.join(data_path, '_'.join(['S&P500', factor_name+'.csv'])))
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        return df.set_index('Date')
    except:
        return df.set_index(df.columns[0])