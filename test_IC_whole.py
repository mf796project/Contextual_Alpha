from ult import res_path, get_matdata
import numpy as np
import pandas as pd

rets = get_matdata("EXRET")
rets = rets.asfreq("M",method="ffill")

constit = get_matdata("constituents") 
constit = constit.asfreq("M",method="ffill")

eps = get_matdata("5Y_GEO_GROWTH_DILUTED_EPS")
eps = eps.asfreq("M",method="ffill")

# EPS=find_IC(constit,rets,eps)

names_limit = 4
""" a function with variables constit (constituent of SPY), rets (returns of constituent of SPY), 
eps (eps data), return the IC time series as a data frame"""
times = constit.index & rets.index & eps.index

def drop_ticker(x):
    '''criterin to drop ticker'''
    if x == '#N/A Invalid Security':
        return False
    elif np.isnan(x) == True:
        return False
    else:
        return True

valid_ticker = eps.apply(lambda x: x.apply(lambda y: drop_ticker(y))).any()
eps_col = valid_ticker.index[valid_ticker == True]

IC=[]


for i in range(len(times)-1):

    online = constit.loc[times[i+1],][constit.loc[times[i+1],]!=0]    #for a given time, constituents of SPY
    
    rts = rets.loc[times[i+1],].dropna()
    rts_col = rts.index
    
    facs=eps.loc[times[i],].dropna()
    facs_col = facs.index

    names = online.index & eps_col & rts_col & facs_col     #constituents having eps data
        
    if len(names) <= names_limit:
        IC.append(None)
        
    else:
        rts=rts[names]
        facs=facs[names]
        #TODO: no need to fillna, rts&facs should be clear by definition
        rts=rts.fillna(0)
        facs=facs.fillna(0)
    
        IC.append(np.corrcoef(list(rts),list(facs))[0,1])
    
ICdf=pd.DataFrame(data=IC,index=times[1:],columns=['eps'])
