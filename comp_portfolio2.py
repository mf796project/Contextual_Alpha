import numpy as np
import pandas as pd
from ult import get_matdata, cont_by_cont, find_weights, portfolio_ret
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

rets = get_matdata('ret', 'M')

# p_size_value = array([0.00313491])

lowvalue = get_matdata('value_pe_1_2', 'M')
highvalue = get_matdata('value_pe_2_2', 'M')
size = get_matdata('CUR_MKT_CAP' ,'M')

low_value_size_conts = cont_by_cont(lowvalue, size, threhold=0.1)
low_value_low_size_weights = find_weights(low_value_size_conts[0])
low_value_high_size_weights = find_weights(low_value_size_conts[1])

high_value_size_conts = cont_by_cont(highvalue, size, threhold=0.1)
high_value_low_size_weights = find_weights(high_value_size_conts[0])
high_value_high_size_weights = find_weights(high_value_size_conts[1])

start_date = pd.to_datetime('1990/01/01')
end_date = pd.to_datetime('2018/12/31')

p1 = portfolio_ret(rets, low_value_low_size_weights, start_date, end_date)
p2 = portfolio_ret(rets, low_value_high_size_weights, start_date, end_date)
p3 = portfolio_ret(rets, high_value_low_size_weights, start_date, end_date)
p4 = portfolio_ret(rets, high_value_high_size_weights, start_date, end_date)

p = np.exp(-(p2 - p1 - p4 + p3))
plt.plot(p)
plt.show()