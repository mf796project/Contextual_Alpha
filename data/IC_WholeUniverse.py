# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:02:36 2019

@author: Yadi Xie
"""

"""Calculate IC of each factor
"""

from MF796_Proj_onesizefitall import *
import pandas as pd

rets=excess
######################################### factor: eps growth  whole universe
eps=pd.read_csv("S&P500_5Y_GEO_GROWTH_DILUTED_EPS.csv")
eps.index=pd.to_datetime(eps['Date']) 
#eps=eps.fillna(method="bfill",axis=0)
eps=eps.asfreq("M",method="ffill")

EPS=find_IC(constit,rets,eps)
EPS.columns=["EPS"]
######################################### factor: sales/share  whole universe
sps=pd.read_csv("S&P500_GEO_GROW_SALES_PER_SH.csv")
sps.index=pd.to_datetime(sps["Date"])

sps=sps.asfreq("M",method="ffill")
SPS=find_IC(constit,rets,sps)
SPS.columns=["SPS"]
IC_Whole=EPS.join(SPS)
######################################### factor: profit margin(growth) whole universe
prof_mar=pd.read_csv("S&P500_PROF_MARGIN.csv")
prof_mar.index=pd.to_datetime(prof_mar["Date"])
prof_mar=prof_mar.asfreq("M",method="ffill")

PROF_MAR=find_IC(constit,rets,prof_mar)
PROF_MAR.columns=["PROF_MAR"]
IC_Whole=IC_Whole.join(PROF_MAR)
######################################## factor: long term growth(growth)  whole universe
"""
lgro=pd.read_csv("S&P500_BEST_EST_LONG_TERM_GROWTH.csv")
lgro.index=pd.to_datetime(lgro["Date"])
lgro=lgro.asfreq("M",method="ffill")

LGRO=find_IC(constit,rets,lgro)
LGRO.columns=["LGRO"]
IC_Whole=IC_Whole.join(LGRO)
"""
######################################### factor: ROIC (growth)  whole universe
roic=pd.read_csv("S&P500_RETURN_ON_INV_CAPITAL.csv")
roic.index=pd.to_datetime(roic["Date"])
roic=roic.asfreq("M",method="ffill")

ROIC=find_IC(constit,rets,roic)
ROIC.columns=["ROIC"]
IC_Whole=IC_Whole.join(ROIC)
#########################################factor: net income growth(growth) whole universe
ninc=pd.read_csv("S&P500_NET_INC_GROWTH.csv")
ninc.index=pd.to_datetime(ninc["Date"])
ninc=ninc.asfreq("M",method="ffill")

NINC=find_IC(constit,rets,ninc)
NINC.columns=["NINC"]
IC_Whole=IC_Whole.join(NINC)
#########################################factor: gross margin (growth)  whole universe
gmar=pd.read_csv("S&P500_GROSS_MARGIN_ADJUSTED.csv")
gmar.index=pd.to_datetime(gmar["Date"])
gmar=gmar.asfreq("M",method="ffill")

GMAR=find_IC(constit,rets,gmar) 
GMAR.columns=["GMAR"]
IC_Whole=IC_Whole.join(GMAR)
######################################### factor :growth of cash from operating act(growth)
cfo=pd.read_csv("S&P500_GEO_GROW_CASH_OPER_ACT.csv")
cfo.index=pd.to_datetime(cfo["Date"])
cfo=cfo.asfreq("M",method="ffill")

CFO=find_IC(constit,rets,cfo) 
CFO.columns=["CFO"]
IC_Whole=IC_Whole.join(CFO)
######################################### factor: growth of cash flow
cf=pd.read_csv("S&P500_CASH_FLOW_GROWTH.csv")
cf.index=pd.to_datetime(cf["Date"])
cf=cf.asfreq("M",method="ffill")

CF=find_IC(constit,rets,cf)
CF.columns=["CF"]
IC_Whole=IC_Whole.join(CF)
#########################################factor: sales growth (growth)  whole universe
sg=pd.read_csv("S&P500_SALES_GROWTH.csv")
sg.index=pd.to_datetime(sg["Date"])
sg=sg.asfreq("M",method="ffill")

SG=find_IC(constit,rets,sg)
SG.columns=["SG"]
IC_Whole=IC_Whole.join(SG)
#########################################factor: P/E next year(value)
fpe=pd.read_csv("S&P500_BEST_PE_NXT_YR.csv")
fpe.index=pd.to_datetime(fpe["Date"])
fpe=fpe.asfreq("M",method="ffill")

FPE=find_IC(constit,rets,fpe)
FPE.columns=["FPE"]
IC_Whole=IC_Whole.join(FPE)
#########################################factor forward P/B ratio (value)
fpb=pd.read_csv("S&P500_BEST_PX_BPS_RATIO.csv")
fpb.index=pd.to_datetime(fpb["Date"])
fpb=fpb.asfreq("M",method="ffill")

FPB=find_IC(constit,rets,fpb)
FPB.columns=["FPB"]
IC_Whole=IC_Whole.join(FPB)
######################################### factor: P/E ratio(value)  whole universe  
pe=pd.read_csv("S&P500_PE_RATIO.csv")
pe.index=pd.to_datetime(pe['Date'])
pe=pe.asfreq("M",method="ffill")

PE=find_IC(constit,rets,pe)  
PE.columns=["PE"]
IC_Whole=IC_Whole.join(PE) 
######################################### factor: P/B ratio(value)  whole universe  
pb=pd.read_csv("S&P500_PX_TO_BOOK_RATIO.csv")
pb.index=pd.to_datetime(pb['Date'])
pb=pb.asfreq("M",method="ffill")

PB=find_IC(constit,rets,pb)  
PB.columns=["PB"]
IC_Whole=IC_Whole.join(PB)
#########################################factor:momentum(market)  whole universe
mom=pd.read_csv("S&P500_REL_SHR_PX_MOMENTUM.csv")
mom.index=pd.to_datetime(mom['Date'])
mom=mom.asfreq("M",method="ffill") 

MOM=find_IC(constit,rets,mom)
MOM.columns=["MOM"]
IC_Whole=IC_Whole.join(MOM)
#########################################factor: cash flow to net income(quality)
cfni=pd.read_csv("S&P500_CASH_FLOW_TO_NET_INC.csv")
cfni.index=pd.to_datetime(cfni["Date"])
cfni=cfni.asfreq("M",method="ffill")

CFNI=find_IC(constit,rets,cfni)
CFNI.columns=["CFNI"]
IC_Whole=IC_Whole.join(CFNI)
#########################################factor: Accounts Receivable Turnover(quality)
art=pd.read_csv("S&P500_ACCT_RCV_TURN.csv")
art.index=pd.to_datetime(art["Date"])
art=art.asfreq("M",method="ffill")

ART=find_IC(constit,rets,art)
ART.columns=["ART"]
IC_Whole=IC_Whole.join(ART)
#########################################factor: Best analyst rating(quality)
ar=pd.read_csv("S&P500_BEST_ANALYST_RATING.csv")
ar.index=pd.to_datetime(ar["Date"])
ar=ar.asfreq("M",method="ffill")

AR=find_IC(constit,rets,ar)
AR.columns=["AR"]
IC_Whole=IC_Whole.join(AR)
######################################### factor: goodwill to asset(quality)
goodwill=pd.read_csv("S&P500_GOODWILL_ASSETS_%.csv")
goodwill.index=pd.to_datetime(goodwill["Date"])
goodwill=goodwill.asfreq("M",method="ffill")

GOODWILL=find_IC(constit,rets,goodwill)
GOODWILL.columns=["GOODWILL"]
IC_Whole=IC_Whole.join(GOODWILL)
######################################### factor: Total Debt to Total Assets(quality)
leve=pd.read_csv("S&P500_TOT_DEBT_TO_TOT_ASSET.csv")
leve.index=pd.to_datetime(leve["Date"])
leve=leve.asfreq("M",method="ffill")

LEVE=find_IC(constit,rets,leve)
LEVE.columns=["LEVE"]
IC_Whole=IC_Whole.join(LEVE)
######################################### factor: Total Analyst Recommendations(quality)
tar=pd.read_csv("S&P500_TOT_ANALYST_REC.csv")
tar.index=pd.to_datetime(tar["Date"])
tar=tar.asfreq("M",method="ffill")

TAR=find_IC(constit,rets,tar)
TAR.columns=["TAR"]
IC_Whole=IC_Whole.join(TAR)
######################################### factor: Recommendation Consensus(quality)
rc=pd.read_csv("S&P500_EQY_REC_CONS.csv")
rc.index=pd.to_datetime(rc["Date"])
rc=rc.asfreq("M",method="ffill")

RC=find_IC(constit,rets,rc)
RC.columns=["RC"]
IC_Whole=IC_Whole.join(RC)
######################################### factor: Inventory Turnover(liquidity, quality)
"""
inv_turn=pd.read_csv("S&P500_INVENT_TURN.csv")
inv_turn.index=pd.to_datetime(inv_turn["Date"])
inv_turn=inv_turn.asfreq("M",method="ffill")

INV_TURN=find_IC(constit,rets,inv_turn)
INV_TURN.columns=["INV_TURN"]
IC_Whole=IC_Whole.join(INV_TURN)
"""
######################################### factor: Average Bid Ask Spread Percentage(liquidity, quality)
"""
spread=pd.read_csv("S&P500_AVERAGE_BID_ASK_SPREAD_%.csv")
spread.index=pd.to_datetime(spread["Date"])
spread=spread.asfreq("M",method="ffill")

SPREAD=find_IC(constit,rets,spread)
SPREAD.columns=["SPREAD"]
IC_Whole=IC_Whole.join(SPREAD)
"""
######################################### factor:Quick Ratio(liquidity, quality)
quick=pd.read_csv("S&P500_QUICK_RATIO.csv")
quick.index=pd.to_datetime(quick["Date"])
quick=quick.asfreq("M",method="ffill")

QUICK=find_IC(constit,rets,quick)
QUICK.columns=["QUICK"]
IC_Whole=IC_Whole.join(QUICK)
######################################### factor:Asset Turnover(liquidity, quality)
a_turn=pd.read_csv("S&P500_ASSET_TURNOVER.csv")
a_turn.index=pd.to_datetime(a_turn["Date"])
a_turn=a_turn.asfreq("M",method="ffill")

A_TURN=find_IC(constit,rets,a_turn)
A_TURN.columns=["A_TURN"]
IC_Whole=IC_Whole.join(A_TURN)

IC_Whole.columns=[x.lower() for x in IC_Whole.columns]
#IC_Whole.to_csv("IC_WholeUniverse.csv")

######################################################################drop factors with NA more than 10% of data amount

factor=[eps,sps,prof_mar,roic,ninc,gmar,cfo,cf,sg,mom,cfni,art,ar,goodwill,leve,tar,rc,quick,a_turn,fpb,pe,pb]
fnames=['eps','sps','prof_mar','roic','ninc','gmar','cfo','cf','sg','mom','cfni','art','ar','goodwill','leve','tar','rc','quick','a_turn','fpb','pe','pb']

reserved=[]
rnames=[]

dropped=[]
dnames=[]
for i in range(len(factor)):
    eff=factor[i].iloc[:,1:].dropna(axis=0,how="all")
    if len(eff)>0.9*len(factor[i]):
        reserved.append(factor[i])
        rnames.append(fnames[i])
    else:
        dropped.append(factor[i])
        dnames.append(fnames[i])
        
dropped.append(fpe)
dnames.append("fpe")
        
new_IC_Whole=IC_Whole[rnames]   

comgro=pd.read_csv("S&P500_Combined_Growth.csv")
comgro=comgro.iloc[:-2,:]
comgro.index=pd.to_datetime(comgro["Date"])
comgro=comgro.asfreq(freq="M",method="ffill")

Comgro=find_IC(constit,rets,comgro)
Comgro.columns=["comgro"]
new_IC_Whole["comgro"]=Comgro     
new_IC_Whole.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/new_IC_Whole.csv")



#######################

Comgro.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedGrowth_IC.csv")