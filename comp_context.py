import os
import numpy as np
import pandas as pd
from ult import cont_path, get_matdata, to_context

n = 2 # number of context

beta = get_matdata('BETA_ADJ_OVERRIDABLE')
beta_conts = to_context(beta, n)
name = 'beta'

for i in range(len(beta_conts)):
    file_name = f'{name}_{i+1}_{n}.csv'
    beta_conts[i].to_csv(os.path.join(cont_path, file_name))





