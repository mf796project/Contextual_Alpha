from ult_data import res_path, get_matdata
import numpy as np
import pandas as pd
from find_IC import find_IC_cont

rets = get_matdata("EXRET")
rets = rets.asfreq("M",method="ffill")

constit = get_matdata("constituents") 
constit = constit.asfreq("M",method="ffill")

pb = get_matdata("PX_TO_BOOK_RATIO")
pb = pb.asfreq("M",method="ffill")

beta = get_matdata("BETA_ADJ_OVERRIDABLE")
beta = beta.asfreq("M",method="ffill")


# pb=find_IC(constit,rets,pb)

names_limit = 4
# def find_IC_cont(constit,rets,pb,beta):
"""given constituent of SPY, log-return of constituent of SPY, pb time series data,
and the beta indicator time series, this function gives back the IC time series for different
beta.
"""
IC_low=[]
IC_mid=[]
IC_high=[]

times=constit.index & rets.index & pb.index & beta.index # same time

def drop_ticker(x):
    '''criterin to drop ticker'''
    if x == '#N/A Invalid Security':
        return False
    elif np.isnan(x) == True:
        return False
    else:
        return True

valid_ticker = pb.apply(lambda x: x.apply(lambda y: drop_ticker(y))).any()
pb_col = valid_ticker.index[valid_ticker == True]

valid_ticker2 = beta.apply(lambda x: x.apply(lambda y: drop_ticker(y))).any()
beta_col = valid_ticker2.index[valid_ticker2 == True]

for i in range(len(times)-1):
    online=constit.loc[times[i+1],][constit.loc[times[i+1],]==1]   #SPY constituent
    names=online.index[1:] & pb_col
    names=names & cont_col                     #same constituent
    
    rts=rets.loc[times[i+1],names]
    #rts=rts.dropna(axis=0,how="any")
    rts=rts.fillna(0)
    
    cont=beta.loc[times[i+1],names]
    cont=cont.dropna(axis=0,how="any")
    #cont=cont.fillna(0)
    #cont=cont.sort_values()      #sort by betaual ,from low to high
    
    fac=pb.loc[times[i],names]
    fac=fac.dropna(axis=0,how="any")
    #fac=fac.fillna(0)
    #fac=np.log(fac)
    
    names=names & cont.index 
    names=names &  fac.index
    
    
    
    if len(names) <=9:
        IC_low.append(None)
        IC_mid.append(None)
        IC_high.append(None)
        
    else:
    
        cont=cont[names]
        fac=fac[names]
        rts=rts[names]
    
        cont=cont.sort_values()
    
        increa_index=cont.index
    
        increa_index_low=increa_index[:(len(increa_index)//3)]
        increa_index_mid=increa_index[(len(increa_index)//3):(2*len(increa_index)//3)]
        increa_index_high=increa_index[(2*len(increa_index)//3):]
    
        IC_low.append(np.corrcoef(list(rts[increa_index_low]),list(fac[increa_index_low]))[0,1])
        IC_mid.append(np.corrcoef(list(rts[increa_index_mid]),list(fac[increa_index_mid]))[0,1])
        IC_high.append(np.corrcoef(list(rts[increa_index_high]),list(fac[increa_index_high]))[0,1])
    
IC=[IC_low,IC_mid,IC_high]
IC=pd.DataFrame(data=IC)
IC=IC.T
    
IC.index=times[1:]
IC.columns=['LOW','MID','HIGH']
    