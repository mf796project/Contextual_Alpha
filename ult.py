import os
import numpy as np
import pandas as pd

path = os.path.abspath('.')
rawdata_path = os.path.join(path, 'rawdata')
matdata_path = os.path.join(path, 'mat_data')
res_path = os.path.join(path, 'result')
cont_path = os.path.join(path, 'context_data')

def get_matdata(file_name, freq=None):
    ''' 
        read data from matdata_path or cont_path,
        adjust freq by asfreq(freq, method="ffill")
    '''
    try:
        df = pd.read_csv(os.path.join(matdata_path, '_'.join(['S&P500', file_name+'.csv'])))
    except FileNotFoundError:
        df = pd.read_csv(os.path.join(cont_path, '_'.join([file_name+'.csv'])))

    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
    except:
        df = df.set_index(df.columns[0])
    
    if freq == None:
        return df
    else:
        return df.asfreq(freq, method="ffill")

def to_context(matdata, n=None):
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
    return tuple(cont_list)

def cont_by_cont(cont, matdata, threhold):
    ''' 
        A function with input: 
            cont (context data),
            matdata (factor data),
            threhold (divide into two parts by threhold)
        output:
            cont (context data)
    '''
    times = cont.index & matdata.index
    
    cont_list = [pd.DataFrame(), pd.DataFrame()]
    for i in range(len(times)):

        # only use tickers in context
        online = cont.loc[times[i],][cont.loc[times[i],]!=0]
        
        # only use tickers with available factor data
        facs = matdata.loc[times[i],].replace([np.inf, -np.inf], np.nan).dropna()

        names = online.index & facs.index

        facs = facs[names]
        q_head = facs.quantile(threhold)
        q_tail = facs.quantile(1-threhold)
        
        df_head = matdata.loc[times[i],].apply(lambda x: x <= q_head)
        df_tail = matdata.loc[times[i],].apply(lambda x: x >= q_tail)

        cont_list[0] = cont_list[0].append(df_head & cont.loc[times[i],]).astype('int')
        cont_list[1] = cont_list[1].append(df_tail & cont.loc[times[i],]).astype('int')
    
    return tuple(cont_list)

def find_weights(cont):
    ''' 
        A function with input: 
            cont (context data),
        output:
            equal Weights time series as a dataframe
    '''
    return cont.apply(lambda x: x/ cont.sum(axis=1))

def portfolio_ret(rets, weights, start_date, end_date):
    times = rets.index & weights.index
    times = times[(times >= start_date) & (times <= end_date)]
    rets = rets.loc[times,]
    weights = weights.loc[times,]

    ret_list = []
    for i in range(len(rets)-1):
        month_ret = (rets.iloc[i+1,:] * weights.iloc[i,]).sum()
        ret_list.append(month_ret)
    cum_ret = np.cumsum(ret_list)

    return cum_ret


