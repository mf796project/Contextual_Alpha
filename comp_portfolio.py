import numpy as np
import pandas as pd
from ult import get_matdata, cont_by_cont, find_weights, portfolio_ret
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

p1 = portfolio_ret(rets, low_size_low_mom_weights, start_date, end_date)
p2 = portfolio_ret(rets, low_size_high_mom_weights, start_date, end_date)
p3 = portfolio_ret(rets, high_size_low_mom_weights, start_date, end_date)
p4 = portfolio_ret(rets, high_size_high_mom_weights, start_date, end_date)

p = np.exp(p2 - p1 - p4 + p3)

plt.plot(p)
plt.show()