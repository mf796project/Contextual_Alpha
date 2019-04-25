import os
import numpy as np
import pandas as pd

path = os.path.abspath('.')
rawdata_path = os.path.join(path, 'rawdata')
matdata_path = os.path.join(path, 'mat_data')
res_path = os.path.join(path, 'result')
cont_path = os.path.join(path, 'context_data')

def get_matdata(file_name):
    ''' read data from matdata_path or cont_path'''
    try:
        df = pd.read_csv(os.path.join(matdata_path, '_'.join(['S&P500', file_name+'.csv'])))
    except FileNotFoundError:
        df = pd.read_csv(os.path.join(cont_path, '_'.join([file_name+'.csv'])))

    try:
        df['Date'] = pd.to_datetime(df['Date'])
        return df.set_index('Date')
    except:
        return df.set_index(df.columns[0])

def to_context(matdata, n):
    '''transform matdata to n contexts'''
    q = np.linspace(0, 1, n+1) # quantile
    cont_list = []
    for i in range(n):
        q_head = matdata.quantile(q[i], axis=1)
        q_tail = matdata.quantile(q[i+1], axis=1)
        
        # left close & right open
        if i == n - 1:
            df = matdata.apply(lambda x: (x >= q_head) & (x <= q_tail))
        else:
            df = matdata.apply(lambda x: (x >= q_head) & (x < q_tail))
        
        cont_list.append(df)

    return cont_list