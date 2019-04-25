# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 10:57:04 2019

@author: Haomiao Yu
"""

from MF796_Proj_onesizefitall import *

import pandas as pd
import numpy as np

pb=pd.read_csv("S&P500_PX_TO_BOOK_RATIO.csv")
pb.index=pd.to_datetime(pb["Date"])

#pb=pb.fillna(method="bfill",axis=0)
pb=pb.asfreq('M', method='ffill')    #resampled price to book

def find_IC_cont(constit,rets,factor,context):
    """given constituent of SPY, log-return of constituent of SPY, factor time series data,
    and the context indicator time series, this function gives back the IC time series for different
    context.
    """
    IC_low=[]
    IC_mid=[]
    IC_high=[]
    
    times=constit.index & rets.index
    times=times & factor.index
    times=times & context.index                  #same time
    
    factor_col=factor.iloc[0,][factor.iloc[0,]!='#N/A Invalid Security']
    factor_col=factor_col.index[1:]           #factor appliable
    
    cont_col=context.iloc[0,][context.iloc[0,]!='#N/A Invalid Security']
    cont_col=cont_col.index[1:]                  #context appliable 
    
    for i in range(len(times)-1):
        online=constit.loc[times[i+1],][constit.loc[times[i+1],]==1]   #SPY constituent
        names=online.index[1:] & factor_col
        names=names & cont_col                     #same constituent
        
        rts=rets.loc[times[i+1],names]
        #rts=rts.dropna(axis=0,how="any")
        rts=rts.fillna(0)
        
        cont=context.loc[times[i+1],names]
        cont=cont.dropna(axis=0,how="any")
        #cont=cont.fillna(0)
        #cont=cont.sort_values()      #sort by contextual ,from low to high
        
        fac=factor.loc[times[i],names]
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
        
    return IC
        
        
        
#IC=find_IC_cont(constit,rets,pb,pb)
        

import scipy.stats as st


        
    
growth=pd.read_csv("S&P500_NET_INC_GROWTH.csv")
growth.index=pd.to_datetime(growth['Date'])
growth=growth.fillna(method="ffill",axis=0)
#growth=growth.asfreq('M',method='ffill')

leve=pd.read_csv("S&P500_TOT_DEBT_TO_TOT_ASSET.csv")
leve.index=pd.to_datetime(leve['Date'])
#leve=leve.fillna(method="bfill",axis=0)
leve=leve.asfreq('M',method='ffill')
#leve.iloc[:,1:]=np.log(leve.iloc[:,1:])





IC=find_IC_cont(constit,rets,leve,growth)
st.ttest_ind(IC.iloc[:,0],IC.iloc[:,1])