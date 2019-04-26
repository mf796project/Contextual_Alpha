from ult import res_path, get_matdata
import numpy as np
import pandas as pd

def find_IC(factor, ret, cont_list, limit=4):
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
        for j in range(len(cont_list)):
            cont = cont_list[j]
            if j == 0:
                online = cont.loc[times[i+1],][cont.loc[times[i+1],]!=0]
            else:
                online = online & \
                    cont.loc[times[i+1],][cont.loc[times[i+1],]!=0]
        
        # only use tickers with available return data
        rts = ret.loc[times[i+1],].dropna()
        
        # only use tickers with available factor data
        facs = factor.loc[times[i],].dropna()

        names = online.index & rts.index & facs.index
            
        if len(names) <= limit:
            IC.append(None)   
        else:
            rts=rts[names]
            facs=facs[names]
            IC.append(np.corrcoef(list(rts),list(facs))[0,1])
    
    ICdf = pd.DataFrame(data=IC,index=times[1:],columns=['factor'])

    return ICdf

    


