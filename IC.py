from ult import res_path, get_matdata
import numpy as np
import pandas as pd

def find_IC(factor, ret, cont_list, limit=2):
    ''' 
        A function with input: 
            ret (returns of constituents), 
            factor (factor data), 
            context_list (context data),
            limit (lowese number of tickers to compute IC)
        output:
            factor IC time series as a dataframe
    '''
    times = factor.index & ret.index
    for cont in cont_list:
        times = times & cont.index

    IC = []
    for i in range(len(times)-1):
        # only use tickers in context
        # print(i)
        # if i == 314:
        #     x = 1
        for j in range(len(cont_list)):
            cont = cont_list[j]
            if j == 0:
                online = cont.loc[times[i+1],][cont.loc[times[i+1],]!=0]
            else:
                online = online & \
                    cont.loc[times[i+1],][cont.loc[times[i+1],]!=0]
        
        # only use tickers with available return data
        rts = ret.loc[times[i+1],].replace([np.inf, -np.inf], np.nan).dropna()
        
        # only use tickers with available factor data
        facs = factor.loc[times[i],].replace([np.inf, -np.inf], np.nan).dropna()

        names = online.index & rts.index & facs.index
            
        if len(names) <= limit:
            IC.append(None)
        else:
            rts=rts[names]
            facs=facs[names]
            corr = np.corrcoef(list(rts),list(facs))[0,1]
            IC.append(corr)
            # print(corr)
    
    ICdf = pd.DataFrame(data=IC,index=times[1:],columns=['factor'])

    return ICdf

    
if __name__ == '__main__':
    # Whole Universe
    ret = get_matdata('EXRET', 'M')
    constit = get_matdata('constituents', 'M') 
    eps = get_matdata('5Y_GEO_GROWTH_DILUTED_EPS' ,'M')

    factor = find_IC(eps, ret, [constit])

    # Contextual
    beta_low = get_matdata('beta_1_2', 'M') # low beta

    factor = find_IC(eps, ret, [constit, beta_low])
