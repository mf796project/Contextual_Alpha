from ult import res_path, get_matdata
from IC import find_IC
import os
import numpy as np
import pandas as pd

const = get_matdata('constituents', 'M')
ret = get_matdata('EXRET', 'M')

eps = get_matdata('5Y_GEO_GROWTH_DILUTED_EPS' ,'M')
sps = get_matdata('GEO_GROW_SALES_PER_SH', 'M')
prof_mar = get_matdata('PROF_MARGIN', 'M')
roic = get_matdata('RETURN_ON_INV_CAPITAL', 'M')
ninc = get_matdata('NET_INC_GROWTH', 'M')
gmar = get_matdata('GROSS_MARGIN_ADJUSTED', 'M')
cfo = get_matdata('GEO_GROW_CASH_OPER_ACT', 'M')
cf = get_matdata('CASH_FLOW_GROWTH', 'M')
sg = get_matdata('SALES_GROWTH', 'M')

whole_dict = {
    'eps':eps, 'sps':sps, 'prof_mar':prof_mar, 'roic':roic, 
    'ninc':ninc, 'gmar':gmar, 'cfo':cfo, 'cf':cf, 'sg':sg,
}

IC_Whole = pd.DataFrame()
for key, value in whole_dict.items():
    factor = find_IC(value, ret, [const])
    factor.columns = [key]
    IC_Whole = pd.concat([IC_Whole, factor], axis=1)
IC_Whole.to_csv(os.path.join(res_path, 'IC_WholeUniverse.csv'))
