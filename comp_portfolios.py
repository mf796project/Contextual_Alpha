import os
import numpy as np
import pandas as pd
from ult import res_path, get_matdata, cont_by_cont, find_weights, portfolio_rets_turn
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

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
nv1, turn1 = portfolio_rets_turn(rets, [lowsize, highsize], Combined_Growth, start_date, end_date)
nv2, turn2 = portfolio_rets_turn(rets, [lowsize, highsize], Combined_Quality, start_date, end_date)
nv3, turn3 = portfolio_rets_turn(rets, [lowsize, highsize], Combined_Value, start_date, end_date)
nv4, turn4 = portfolio_rets_turn(rets, [lowsize, highsize], Momentum, start_date, end_date)

nv5, turn5 = portfolio_rets_turn(rets, [lowvalue, highvalue], Combined_Growth, start_date, end_date)
nv6, turn6 = portfolio_rets_turn(rets, [lowvalue, highvalue], Combined_Quality, start_date, end_date)
nv7, turn7  = portfolio_rets_turn(rets, [lowvalue, highvalue], Combined_Value, start_date, end_date)
nv8, turn8 = portfolio_rets_turn(rets, [lowvalue, highvalue], Momentum, start_date, end_date)

nvs = pd.concat([nv1, nv2, nv3, nv4, nv5, nv6, nv7, nv8], axis=1)
nvs.to_csv(os.path.join(res_path, 'nvs.csv'))

turns = pd.concat([turn1, turn2, turn3, turn4, turn5, turn6, turn7, turn8], axis=1)
turns.to_csv(os.path.join(res_path, 'turns.csv'))