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

rets=excess
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
factor=reserved
fnames=rnames


def Sector_IC (constit,rets,factor,fnames,ind,new_IC_Whole,alpha):
    gic=cate.iloc[:,0][cate.iloc[:,2]==ind]
    mem=tic["tic"][tic["Gind"].isin(gic)]
    crets=rets[mem]

    co=constit.columns&crets.columns
    new_con=constit[co]
    crets=crets[co]
    
    IC=pd.DataFrame(index=factor[0].index)
    tstat=pd.DataFrame(index=["p","significance"])
    
    
    for i in range(len(factor)):
        ic=find_IC(new_con,crets,factor[i])
        ic.columns=[fnames[i]]
        IC=IC.join(ic,how="right")
                
        ic=ic.dropna(axis=0,how="any")
        p=st.ttest_ind(ic,new_IC_Whole[fnames[i]].dropna(axis=0,how="any")).pvalue[0]
        if p<alpha:
            p=[p,1]
        else:
            p=[p,0]
        
        df=pd.DataFrame(p,index=tstat.index,columns=[fnames[i]])
        tstat=tstat.join(df)
        
    
    return IC,tstat

alpha=0.05
con_IC,con_sig=Sector_IC (constit,rets,factor,fnames,"Consumer",new_IC_Whole,alpha)
fin_IC,fin_sig=Sector_IC (constit,rets,factor,fnames,"Finance",new_IC_Whole,alpha)
tech_IC,tech_sig=Sector_IC (constit,rets,factor,fnames,"Technology",new_IC_Whole,alpha)     
others_IC,others_sig=Sector_IC (constit,rets,factor,fnames,"Others",new_IC_Whole,alpha)
        
        
con_IC.to_csv("Consumer_IC.csv")
fin_IC.to_csv("Finance_IC.csv")
tech_IC.to_csv("Technology_IC.csv")
others_IC.to_csv("Others_IC.csv")

con_sig.to_csv("Consumer_sig.csv")
fin_sig.to_csv("Finance_sig.csv")
tech_sig.to_csv("Technology_sig.csv")
others_sig.to_csv("Others_sig.csv")
        
m1=con_IC.mean(axis=0)
#mean=pd.DataFrame(index=["Consumer","Finance","Technology","Others"])
mean=pd.DataFrame(m1,columns=["Consumer"])
m2=pd.DataFrame(fin_IC.mean(axis=0),columns=["Finance"])
mean=mean.join(m2)
m3=pd.DataFrame(tech_IC.mean(axis=0),columns=["Technology"])
mean=mean.join(m3)
m4=pd.DataFrame(others_IC.mean(axis=0),columns=["Others"])
mean=mean.join(m4)

mean=mean.T





