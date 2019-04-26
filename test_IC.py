from ult import res_path, get_matdata
from IC import find_IC

# Whole Universe
ret = get_matdata('EXRET', 'M')
constit = get_matdata('constituents', 'M') 
eps = get_matdata('5Y_GEO_GROWTH_DILUTED_EPS' ,'M')

factor = find_IC(eps, ret, [constit])

# Contextual
beta_low = get_matdata('beta_1_2', 'M') # low beta

factor = find_IC(eps, ret, [constit, beta_low])