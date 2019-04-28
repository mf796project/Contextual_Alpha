from ult import res_path, get_matdata
from IC import find_IC
import scipy.stats as st


ret = get_matdata('EXRET', 'M')
constit = get_matdata('constituents', 'M')

Combined_Growth = get_matdata('Combined_Growth' ,'M')
Combined_Quality = get_matdata('Combined_Quality' ,'M')
Combined_Value = get_matdata('Combined_Value' ,'M')
Momentum = get_matdata('REL_SHR_PX_MOMENTUM' ,'M')
Cap = get_matdata('CUR_MKT_CAP' ,'M')

size_low = get_matdata('size_1_2', 'M')
size_high = get_matdata('size_2_2', 'M')

value_low = get_matdata('value_pe_1_2', 'M')
value_high = get_matdata('value_pe_2_2', 'M')

# Context: Size
growth_lowsize = find_IC(Combined_Growth, ret, [constit, size_low])
growth_highsize = find_IC(Combined_Growth, ret, [constit, size_high])
p_growth_size = st.ttest_ind(growth_lowsize, growth_highsize).pvalue

quality_lowsize = find_IC(Combined_Quality, ret, [constit, size_low])
quality_highsize = find_IC(Combined_Quality, ret, [constit, size_high])
p_quality_size = st.ttest_ind(quality_lowsize, quality_highsize).pvalue

value_lowsize = find_IC(Combined_Value, ret, [constit, size_low])
value_highsize = find_IC(Combined_Value, ret, [constit, size_high])
p_value_size = st.ttest_ind(value_lowsize, value_highsize).pvalue

mom_lowsize = find_IC(Momentum, ret, [constit, size_low])
mom_highsize = find_IC(Momentum, ret, [constit, size_high])
p_mom_size = st.ttest_ind(mom_lowsize, mom_highsize).pvalue

# Context: Value
growth_lowvalue = find_IC(Combined_Growth, ret, [constit, value_low])
growth_highvalue = find_IC(Combined_Growth, ret, [constit, value_high])
p_growth_value = st.ttest_ind(growth_lowvalue, growth_highvalue).pvalue

quality_lowvalue = find_IC(Combined_Quality, ret, [constit, value_low])
quality_highvalue = find_IC(Combined_Quality, ret, [constit, value_high])
p_quality_value = st.ttest_ind(quality_lowvalue, quality_highvalue).pvalue

size_lowvalue = find_IC(Cap, ret, [constit, value_low])
size_highvalue = find_IC(Cap, ret, [constit, value_high])
p_size_value = st.ttest_ind(size_lowvalue, size_highvalue).pvalue

mom_lowvalue = find_IC(Momentum, ret, [constit, value_low])
mom_highvalue = find_IC(Momentum, ret, [constit, value_high])
p_mom_value = st.ttest_ind(mom_lowvalue, mom_highvalue).pvalue