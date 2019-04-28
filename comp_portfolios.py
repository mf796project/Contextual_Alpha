import os
import numpy as np
import pandas as pd
from ult import res_path, get_matdata, cont_by_cont, find_weights, portfolio_ret
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

def portfolio_rets(rets, cont_list, factor, start_date, end_date):
    
    low_cont_fac_conts = cont_by_cont(cont_list[0], factor, threhold=0.1)
    low_cont_low_fac_weights = find_weights(low_cont_fac_conts[0])
    low_cont_high_fac_weights = find_weights(low_cont_fac_conts[1])

    high_cont_fac_conts = cont_by_cont(cont_list[1], factor, threhold=0.1)
    high_cont_low_fac_weights = find_weights(high_cont_fac_conts[0])
    high_cont_high_fac_weights = find_weights(high_cont_fac_conts[1])

    p1 = portfolio_ret(rets, low_cont_low_fac_weights, start_date, end_date)
    p2 = portfolio_ret(rets, low_cont_high_fac_weights, start_date, end_date)
    p3 = portfolio_ret(rets, high_cont_low_fac_weights, start_date, end_date)
    p4 = portfolio_ret(rets, high_cont_high_fac_weights, start_date, end_date)

    p = p2 - p1 - p4 + p3

    return p

# return data
rets = get_matdata('ret', 'M')

# context data
lowsize = get_matdata('size_1_2', 'M')
highsize = get_matdata('size_2_2', 'M')

lowvalue = get_matdata('value_pe_1_2', 'M')
highvalue = get_matdata('value_pe_2_2', 'M')

# factor data
Combined_Growth = get_matdata('Combined_Growth' ,'M')
Combined_Quality = get_matdata('Combined_Quality' ,'M')
Combined_Value = get_matdata('Combined_Value' ,'M')
Momentum = get_matdata('REL_SHR_PX_MOMENTUM' ,'M')
Cap = get_matdata('CUR_MKT_CAP' ,'M')

# backtest period
start_date = pd.to_datetime('1990/01/01')
end_date = pd.to_datetime('2018/12/31')

# loop
nv1 = portfolio_rets(rets, [lowsize, highsize], Combined_Growth, start_date, end_date)
nv2 = portfolio_rets(rets, [lowsize, highsize], Combined_Quality, start_date, end_date)
nv3 = portfolio_rets(rets, [lowsize, highsize], Combined_Value, start_date, end_date)
nv4 = portfolio_rets(rets, [lowsize, highsize], Momentum, start_date, end_date)

nv5 = portfolio_rets(rets, [lowvalue, highvalue], Combined_Growth, start_date, end_date)
nv6 = portfolio_rets(rets, [lowvalue, highvalue], Combined_Quality, start_date, end_date)
nv7 = portfolio_rets(rets, [lowvalue, highvalue], Cap, start_date, end_date)
nv8 = portfolio_rets(rets, [lowvalue, highvalue], Momentum, start_date, end_date)

df = pd.concat([nv1, nv2, nv3, nv4, nv5, nv6, nv7, nv8], axis=1)
df.to_csv(os.path.join(res_path, 'nvs.csv'))
