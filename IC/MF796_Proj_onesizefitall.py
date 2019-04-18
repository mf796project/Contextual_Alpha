# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:21:14 2019

@author: Haomiao Yu
"""

## a test with contextual growth, facotrs:market(momentum), value, quality

#test contextual growth, factor ,momentum

import pandas as pd
import numpy as np

price=pd.read_csv("S&P500_clsprc.csv")
price.index=pd.to_datetime(price['Date'])  #use time as index
price=price.iloc[:,1:]                         #elinimate date column
price=price.dropna(axis=0,how="all")           #if for one time all data are NA, we drop it

price_m=price.asfreq('M',method="ffill")       #resample to monthly frequency, fill NA with last valid value

spy=pd.read_csv("S&P500_index.csv") #daily SPY index
spy.index=pd.to_datetime(spy["Date"])
spy=spy.iloc[:,1:]
spy=spy.dropna(axis=0,how="all") 
spy=spy.asfreq("M",method="ffill")


constit=pd.read_csv("S&P500_constituents.csv")    #consitiuent of SPY

constit.index=pd.to_datetime(constit['Date'])
constit=constit.asfreq("M",method="ffill")    #resample

times=price_m.index & constit.index  
times=times&spy.index
price_m=price_m.loc[times]
spy=spy.loc[times]
constit=constit.loc[times]          #time that both constituent data and price data exist
tot_names=price_m.columns & constit.columns     #stock names that both price data and constituent data exist
price_m=price_m[tot_names]                         
constit=constit[tot_names]                         #reselect

rets=np.log(price_m.shift(-1)/price_m)
rets=rets.iloc[:-1,]
rets.index=times[1:]                        #monthly log return

mret=np.log(spy.shift(-1)/spy)
mret=mret.iloc[:-1,]
mret.index=times[1:]


excess=rets.sub(pd.Series(mret.iloc[:,0],index=mret.index),axis="index")#excess return
"""
mom=pd.read_csv("S&P500_REL_SHR_PX_MOMENTUM.csv")
mom.index=pd.to_datetime(mom['Date'])
mom=mom.asfreq("M",method="ffill")          #momentum factor resampled at monthly frequency
times=times & mom.index                       

mom1=mom.iloc[0,][mom.iloc[0,]!="#N/A Invalid Security"]    #stocks that momentom factor appliable
mom_col=mom1.index
mom_col=mom_col[1:]

rets.to_csv("logrets_missing.csv")

IC_mom=[]

for i in range(len(times)-1):
    online=constit.loc[times[i+1],][constit.loc[times[i+1],]!=0]
    names=online.index[1:]
    names=names & mom_col
    
    rt=rets.loc[times[i+1],names]
    mo=mom.loc[times[i],names]
    mo=mo.fillna(0)
    rt=rt.fillna(0)
    
    
    IC_mom.append(np.corrcoef(rt,mo)[0,1])
    
IC_mom=pd.DataFrame(IC_mom,index=times[1:],columns=["Momentum"])

"""

def find_IC(constit,rets,factor):
    """ a function with variables constit (constituent of SPY), rets (returns of constituent of SPY), 
    factor (factor data), return the IC time series as a data frame"""
    times=constit.index & rets.index
    times=times & factor.index         #times that triple data exist
    
    factor_col=factor.iloc[0,][factor.iloc[0,:]!='#N/A Invalid Security']
    factor_col=factor_col.index[1:]     #stocks that factor appliable
    
    IC=[]
    
    for i in range(len(times)-1):
        online=constit.loc[times[i+1],][constit.loc[times[i+1],]!=0]    #for a given time, constituents of SPY
        names=online.index[1:] & factor_col     #constituents having factor data
                          
        rts=rets.loc[times[i+1],names]
        rts=rts.dropna(axis=0,how="any")
        
        facs=factor.loc[times[i],names]
        facs=facs.dropna(axis=0,how="any")
        
        names=names & rts.index & facs.index
        
        rts=rts[names]
        facs=facs[names]
        
        
        rts=rts.fillna(0)
        facs=facs.fillna(0)
        
        IC.append(np.corrcoef(list(rts),list(facs))[0,1])
        
    ICdf=pd.DataFrame(data=IC,index=times[1:])
    
    return ICdf
    

pe=pd.read_csv("S&P500_PE_RATIO.csv")
pe.index=pd.to_datetime(pe['Date'])
pe=pe.asfreq("M",method="ffill")

find_IC(constit,rets,pe)
    
    
    
    
    

#spy_mom=pd.read_csv("S&P500_REL_SHR_PX_MOMENTUM.csv")
#spy_mom.index=pd.to_datetime(spy_mom["Date"])
#columns=spy_mom.columns
#constit=constit[columns]
#spy_price_m=spy_price_m[columns]
#
#spy_rt=np.log(spy_price_m.iloc[1:,]/spy_price_m.iloc[:-1,])
#
