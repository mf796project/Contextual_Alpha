# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 13:00:17 2019

@author: Yadi Xie
"""

"""Calculate IC within different sector
"""
#Consume
from MF796_Proj_onesizefitall import find_IC
from IC_WholeUniverse import *
import pandas as pd
import scipy.stats as st

cate=pd.read_csv("4LargeSectors.csv")
tic=pd.read_csv("S&P500_gic_sector_code.csv")# contains campanies and its industry
tic["Gind"]=tic["Gind"]//100 # first four digit of industry code
"""
gic=cate.iloc[:,0][cate.iloc[:,2]=="Consumer"]# industry code for consumer industry


mem=tic["tic"][tic["Gind"].isin(gic)]
crets=rets[mem]

co=constit.columns&crets.columns
new_con=constit[co]
crets=crets[co]
"""
factor=[eps,sps,prof_mar,lgro,roic,ninc,gmar,cfo,cf,sg,mom,cfni,art,ar,goodwill,leve,tar,rc,inv_turn,spread,quick,a_turn,fpe,fpb,pe,pb]
fnames=['eps','sps','prof_mar','lgro','roic','ninc','gmar','cfo','cf','sg','mom','cfni','art','ar','goodwill','leve','tar','rc','inv_turn','spread','quick','a_turn','fpe','fpb','pe','pb']



def Sector_IC (constit,rets,factor,fnames,ind,IC_Whole,alpha):
    gic=cate.iloc[:,0][cate.iloc[:,2]==ind]
    mem=tic["tic"][tic["Gind"].isin(gic)]
    crets=rets[mem]

    co=constit.columns&crets.columns
    new_con=constit[co]
    crets=crets[co]
    
    IC=pd.DataFrame(index=factor[0].index)
    tstat=pd.DataFrame(index=["tstat","significance"])
    
    
    for i in range(len(factor)):
        ic=find_IC(new_con,crets,factor[i])
        ic.columns=[fnames[i]]
        IC=IC.join(ic,how="right")
        
        ic=ic.dropna(axis=0,how="any")
        p=st.ttest_ind(ic,IC_Whole[fnames[i]].dropna(axis=0,how="any")).pvalue[0]
        if p<alpha:
            p=[p,1]
        else:
            p=[p,0]
        
        df=pd.DataFrame(p,index=tstat.index,columns=[fnames[i]])
        tstat=tstat.join(df)
        
    
    return IC,tstat

alpha=0.05
con_IC,con_sig=Sector_IC (constit,rets,factor,fnames,"Consumer",IC_Whole,alpha)
fin_IC,fin_sig=Sector_IC (constit,rets,factor,fnames,"Finance",IC_Whole,alpha)
tech_IC,tech_sig=Sector_IC (constit,rets,factor,fnames,"Technology",IC_Whole,alpha)     
others_IC,others_sig=Sector_IC (constit,rets,factor,fnames,"Others",IC_Whole,alpha)
        
        
con_IC.to_csv("Consumer_IC.csv")
fin_IC.to_csv("Finance_IC.csv")
tech_IC.to_csv("Technology_IC.csv")
others_IC.to_csv("Others_IC.csv")

con_sig.to_csv("Consumer_sig.csv")
fin_sig.to_csv("Finance_sig.csv")
tech_sig.to_csv("Technology_sig.csv")
others_sig.to_csv("Others_sig.csv")
        
    
    




