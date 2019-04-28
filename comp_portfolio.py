import numpy as np
import pandas as pd
from ult import get_matdata, cont_by_cont, find_weights
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

rets = get_matdata('ret', 'M')

# p_mom_size = array([0.05493932])
lowsize = get_matdata('size_1_2', 'M')
highsize = get_matdata('size_2_2', 'M')
Momentum = get_matdata('REL_SHR_PX_MOMENTUM' ,'M')

low_size_mom_conts = cont_by_cont(lowsize, Momentum, threhold=0.1)
low_size_low_mom_weights = find_weights(low_size_mom_conts[0])
low_size_high_mom_weights = find_weights(low_size_mom_conts[1])

high_size_mom_conts = cont_by_cont(highsize, Momentum, threhold=0.1)
high_size_low_mom_weights = find_weights(high_size_mom_conts[0])
high_size_high_mom_weights = find_weights(high_size_mom_conts[1])

start_date = pd.to_datetime('1990/01/01')
end_date = pd.to_datetime('2018/12/31')

def portfolio_nv(rets, weights, start_date, end_date):
    times = rets.index & weights.index
    times = times[(times >= start_date) & (times <= end_date)]
    rets.loc[times,]
    weights.loc[times,]

    ret_list = []
    for i in range(len(rets)-1):
        month_ret = (rets.iloc[i+1,:] * weights.iloc[i,]).sum()
        ret_list.append(month_ret)
    cum_ret = np.cumsum(ret_list)

    return cum_ret

p1 = portfolio_nv(rets, low_size_low_mom_weights, start_date, end_date)
p2 = portfolio_nv(rets, low_size_high_mom_weights, start_date, end_date)
p3 = portfolio_nv(rets, high_size_low_mom_weights, start_date, end_date)
p4 = portfolio_nv(rets, high_size_high_mom_weights, start_date, end_date)

p = p2 - p1 - p4 + p3
plt.plot(p)
plt.show()