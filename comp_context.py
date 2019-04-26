import os
import numpy as np
import pandas as pd
from ult import cont_path, get_matdata, to_context

# number of context
n = 2 
# naming convention: beta_1_2(low beta), beta_2_2(high beta)
beta = get_matdata('BETA_ADJ_OVERRIDABLE', 'M')
beta_conts = to_context(beta, n)
name = 'beta'
for i in range(len(beta_conts)):
    file_name = f'{name}_{i+1}_{n}.csv' 
    beta_conts[i].to_csv(os.path.join(cont_path, file_name))

growth = get_matdata('NET_INC_GROWTH', 'M')
growth_conts = to_context(growth, n)
name = 'growth'
for i in range(len(growth_conts)):
    file_name = f'{name}_{i+1}_{n}.csv'
    growth_conts[i].to_csv(os.path.join(cont_path, file_name))





