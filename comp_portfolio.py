import numpy as np
import pandas as pd
from ult import get_matdata, cont_by_cont, find_weights

# p_mom_size = array([0.05493932])
lowsize = get_matdata('size_1_2', 'M')
highsize = get_matdata('size_2_2', 'M')
Momentum = get_matdata('REL_SHR_PX_MOMENTUM' ,'M')

size_mom_conts = cont_by_cont(lowsize, Momentum, threhold=0.1)
low_weights = find_weights(size_mom_conts[0])
high_weights = find_weights(size_mom_conts[1])
