import os
import numpy as np
import pandas as pd
from ult import cont_path, get_matdata, to_context

# number of context
n = 2 
# naming convention: beta_1_2(low beta), beta_2_2(high beta)

# beta
beta = get_matdata('BETA_ADJ_OVERRIDABLE', 'M')
beta_conts = to_context(beta, n)
name = 'beta'
for i in range(len(beta_conts)):
    file_name = f'{name}_{i+1}_{n}.csv' 
    beta_conts[i].to_csv(os.path.join(cont_path, file_name))

# growth
growth_eps = get_matdata('5Y_GEO_GROWTH_DILUTED_EPS', 'M')
growth_eps_conts = to_context(growth_eps, n)
name = 'growth_eps'
for i in range(len(growth_eps_conts)):
    file_name = f'{name}_{i+1}_{n}.csv'
    growth_eps_conts[i].to_csv(os.path.join(cont_path, file_name))

# value
value_pe = get_matdata('PE_RATIO', 'M')
value_pe_conts = to_context(value_pe, n)
name = 'value_pe'
for i in range(len(value_pe_conts)):
    file_name = f'{name}_{i+1}_{n}.csv' 
    value_pe_conts[i].to_csv(os.path.join(cont_path, file_name))

value_pb = get_matdata('PX_TO_BOOK_RATIO', 'M')
value_pb_conts = to_context(value_pb, n)
name = 'value_pb'
for i in range(len(value_pb_conts)):
    file_name = f'{name}_{i+1}_{n}.csv' 
    value_pb_conts[i].to_csv(os.path.join(cont_path, file_name))

# size
size = get_matdata('CUR_MKT_CAP', 'M')
size_conts = to_context(size, n)
name = 'size'
for i in range(len(size_conts)):
    file_name = f'{name}_{i+1}_{n}.csv' 
    size_conts[i].to_csv(os.path.join(cont_path, file_name))


