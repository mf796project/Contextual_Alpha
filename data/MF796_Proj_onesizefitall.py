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
price=price.iloc[:,1:]                         #delete date column
price=price.dropna(axis=0,how="all")           #if for one time all data are NA, we drop it

price_m=price.asfreq('M',method="ffill")       #resample to monthly frequency, fill NA with last valid value

constit=pd.read_csv("S&P500_constituents.csv")    #consitiuent of SPY

constit.index=pd.to_datetime(constit['Date'])
constit=constit.asfreq("M",method="ffill")    #resample

times=price_m.index & constit.index            #time that both constituent data and price data exist
tot_names=price_m.columns & constit.columns     #stock names that both price data and constituent data exist
price_m=price_m[tot_names]                         
constit=constit[tot_names]                         #reselect

rets=np.log(price_m.shift(-1)/price_m)
rets=rets.iloc[:-1,]
rets.index=times[1:]                        #monthly log return
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
        names=online.index[1:] & factor_col                             #constituents having factor data
        rts=rets.loc[times[i+1],names]
        facs=factor.loc[times[i],names]
        
        rts=rts.fillna(0)
        facs=facs.fillna(0)
        
        IC.append(np.corrcoef(rts,facs)[0,1])
        
    ICdf=pd.DataFrame(data=IC,index=times[1:])
    
    return ICdf
    

"""

Calculate IC of each factor


######################################### factor: eps growth  whole universe
eps=pd.read_csv("S&P500_5Y_GEO_GROWTH_DILUTED_EPS.csv")
eps.index=pd.to_datetime(eps['Date'])   
eps=eps.fillna(method="bfill",axis=0)
eps=eps.asfreq("M",method="ffill")

find_IC(constit,rets,eps)
######################################### factor: sales/share  whole universe
sps=pd.read_csv("S&P500_GEO_GROW_SALES_PER_SH.csv")
sps.index=pd.to_datetime(sps["Date"])
sps=sps.asfreq("M",method="ffill")

find_IC(constit,rets,sps)
######################################### factor: profit margin(growth) whole universe
prof_mar=pd.read_csv("S&P500_PROF_MARGIN.csv")
prof_mar.index=pd.to_datetime(prof_mar["Date"])
prof_mar=prof_mar.asfreq("M",method="ffill")

find_IC(constit,rets,prof_mar)
######################################## factor: long term growth(growth)  whole universe
lgro=pd.read_csv("S&P500_BEST_EST_LONG_TERM_GROWTH.csv")
lgro.index=pd.to_datetime(lgro["Date"])
lgro=lgro.asfreq("M",method="ffill")

find_IC(constit,rets,lgro)
######################################### factor: ROIC (growth)  whole universe
roic=pd.read_csv("S&P500_RETURN_ON_INV_CAPITAL.csv")
roic.index=pd.to_datetime(roic["Date"])
roic=roic.asfreq("M",method="ffill")

find_IC(constit,rets,roic)
#########################################factor: net income growth(growth) whole universe
ninc=pd.read_csv("S&P500_NET_INC_GROWTH.csv")
ninc.index=pd.to_datetime(ninc["Date"])
ninc=ninc.asfreq("M",method="ffill")

find_IC(constit,rets,ninc)
#########################################factor: gross margin (growth)  whole universe
gmar=pd.read_csv("S&P500_GROSS_MARGIN_ADJUSTED.csv")
gmar.index=pd.to_datetime(gmar["Date"])
gmar=gmar.asfreq("M",method="ffill")

find_IC(constit,rets,gmar) 
######################################### factor :growth of cash from operating act(growth)
cfo=pd.read_csv("S&P500_GEO_GROW_CASH_OPER_ACT.csv")
cfo.index=pd.to_datetime(cfo["Date"])
cfo=cfo.asfreq("M",method="ffill")

find_IC(constit,rets,cfo) 
######################################### factor: growth of cash flow
cf=pd.read_csv("S&P500_CASH_FLOW_GROWTH.csv")
cf.index=pd.to_datetime(cf["Date"])
cf=cf.asfreq("M",method="ffill")

find_IC(constit,rets,cf)
#########################################factor: sales growth (growth)  whole universe
sg=pd.read_csv("S&P500_SALES_GROWTH.csv1")
sg.index=pd.to_datetime(sg["Date"])
sg=sg.asfreq("M",method="ffill")

find_IC(constit,rets,sg)
#########################################factor: P/E next year(value)
fpe=pd.read_csv("S&P500_BEST_PE_NXT_YR.csv")
fpe.index=pd.to_datetime(fpe["Date"])
fpe=fpe.asfreq("M",method="ffill")

find_IC(constit,rets,fpe)
#########################################factor P/B ratio (value)
pb=pd.read_csv("S&P500_BEST_PX_BPS_RATIO.csv")
pb.index=pd.to_datetime(pb["Date"])
pb=pb.asfreq("M",method="ffill")

find_IC(constit,rets,pb)
######################################### factor: P/E ratio(value)  whole universe  
pe=pd.read_csv("S&P500_PE_RATIO.csv")
pe.index=pd.to_datetime(pe['Date'])
pe=pe.asfreq("M",method="ffill")

find_IC(constit,rets,pe)    
#########################################factor:momentum(market)  whole universe
mom=pd.read_csv("S&P500_REL_SHR_PX_MOMENTUM.csv")
mom.index=pd.to_datetime(mom['Date'])
mom=mom.asfreq("M",method="ffill") 

find_IC(constit,rets,mom)
#########################################factor: cash flow to net income(quality)
cfni=pd.read_csv("S&P500_CASH_FLOW_TO_NET_INC.csv")
cfni.index=pd.to_datetime(cfni["Date"])
cfni=cfni.asfreq("M",method="ffill")

find_IC(constit,rets,cfni)
#########################################factor: Accounts Receivable Turnover(quality)
art=pd.read_csv("S&P500_ACCT_RCV_TURN.csv")
art.index=pd.to_datetime(art["Date"])
art=art.asfreq("M",method="ffill")

find_IC(constit,rets,art)
#########################################factor: Best analyst rating(quality)
ar=pd.read_csv("S&P500_BEST_ANALYST_RATING.csv")
ar.index=pd.to_datetime(ar["Date"])
ar=art.asfreq("M",method="ffill")

find_IC(constit,rets,ar)
######################################### factor: goodwill to asset(quality)
goodwill=pd.read_csv("S&P500_GOODWILL_ASSETS_%.csv")
goodwill.index=pd.to_datetime(goodwill["Date"])
goodwill=goodwill.asfreq("M",method="ffill")

find_IC(constit,rets,goodwill)
######################################### factor: Total Debt to Total Assets(quality)
leve=pd.read_csv("S&P500_TOT_DEBT_TO_TOT_ASSET.csv")
leve.index=pd.to_datetime(leve["Date"])
leve=leve.asfreq("M",method="ffill")

find_IC(constit,rets,leve)
######################################### factor: Total Analyst Recommendations(quality)
tar=pd.read_csv("S&P500_TOT_ANALYST_REC.csv")
tar.index=pd.to_datetime(tar["Date"])
tar=tar.asfreq("M",method="ffill")

find_IC(constit,rets,tar)
######################################### factor: Recommendation Consensus(quality)
rc=pd.read_csv("S&P500_EQY_REC_CONS.csv")
rc.index=pd.to_datetime(rc["Date"])
rc=rc.asfreq("M",method="ffill")

find_IC(constit,rets,rc)
######################################### factor: Inventory Turnover(liquidity, quality)
inv_turn=pd.read_csv("S&P500_INVENT_TURN.csv")
inv_turn.index=pd.to_datetime(inv_turn["Date"])
inv_turn=inv_turn.asfreq("M",method="ffill")

find_IC(constit,rets,inv_turn)
######################################### factor: Average Bid Ask Spread Percentage(liquidity, quality)
spread=pd.read_csv("S&P500_AVERAGE_BID_ASK_SPREAD_%.csv")
spread.index=pd.to_datetime(spread["Date"])
spread=spread.asfreq("M",method="ffill")

find_IC(constit,rets,spread)
######################################### factor:Quick Ratio(liquidity, quality)
quick=pd.read_csv("S&P500_QUICK_RATIO.csv")
quick.index=pd.to_datetime(quick["Date"])
quick=quick.asfreq("M",method="ffill")

find_IC(constit,rets,quick)
######################################### factor:Asset Turnover(liquidity, quality)
a_turn=pd.read_csv("S&P500_ASSET_TURNOVER.csv")
a_turn.index=pd.to_datetime(a_turn["Date"])
a_turn=a_turn.asfreq("M",method="ffill")

find_IC(constit,rets,a_turn)
#########################################
#spy_mom=pd.read_csv("S&P500_REL_SHR_PX_MOMENTUM.csv")
#spy_mom.index=pd.to_datetime(spy_mom["Date"])
#columns=spy_mom.columns
#constit=constit[columns]
#spy_price_m=spy_price_m[columns]
#
#spy_rt=np.log(spy_price_m.iloc[1:,]/spy_price_m.iloc[:-1,])
#
     
"""