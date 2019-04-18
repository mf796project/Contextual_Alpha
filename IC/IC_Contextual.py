# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 23:38:59 2019

@author: Yadi Xie
"""

from MF796_Proj_contextual import *
from IC_WholeUniverse import *
import pandas as pd
import scipy.stats as st
"""context: value""" #fpe fpb pe pb
rets=excess
########################################
#factor:growth:eps,sps,prof_mar,lgro,roic,ninc,gmar,cfo,cf,sg
#market:mom
#quality:cfni,art,ar,goodwill,leve,tar,rc,inv_turn,spread,quick,a_turn
factor=[eps,sps,prof_mar,roic,ninc,cfo,cf,sg,mom,cfni,art,goodwill,leve,inv_turn,quick,a_turn]
context=[pe,pb]
fnames=["eps",'sps','prof_mar','roic','ninc','cfo','cf','sg','mom','cfni','art','goodwill','leve','inv_turn','quick','a_turn']
cnames=['pe','pb']


def IC_cont(factor,context,fnames,cnames,alpha):
    IC=pd.DataFrame(index=factor[0].index)
    """ 
    mean_c=pd.DataFrame(index=["LOW","MID","HIGH"])
    std=pd.DataFrame(index=["LOW","MID","HIGH"])
    """
    tstat=pd.DataFrame(index=["L_M","M_H","L_H"])
    signif=pd.DataFrame(index=["L_M","M_H","L_H"])
    
    for i in range(len(context)):
        for j in range(len(factor)):
            a=find_IC_cont(constit,rets,factor[j],context[i])
            a.columns=['LOW_'+fnames[j]+'_'+cnames[i],'MID_'+fnames[j]+'_'+cnames[i],'HIGH_'+fnames[j]+'_'+cnames[i]]
            IC=IC.join(a,how="right")
            """
            m=pd.DataFrame(a.mean(axis=0),index=mean_c.index,columns=[fnames[j]+'_'+cnames[i]])
            mean_c=mean_c.join(m)
            
            stdev=pd.DataFrame(a.std(axis=0),index=std.index,columns=[fnames[j]+'_'+cnames[i]])
            std=std.join(stdev)
            """
            a=a.dropna(axis=0,how="any")
            lm=st.ttest_ind(a.iloc[:,0],a.iloc[:,1]).pvalue
            mh=st.ttest_ind(a.iloc[:,1],a.iloc[:,2]).pvalue
            lh=st.ttest_ind(a.iloc[:,0],a.iloc[:,2]).pvalue
            t=[lm,mh,lh]
            df=pd.DataFrame(t,index=tstat.index,columns=[fnames[j]+'_'+cnames[i]])
            tstat=tstat.join(df)
            
            sig=[0,0,0]
            for x in range(len(t)):
                if t[x]<alpha:
                    sig[x]=1
                    
            s=pd.DataFrame(sig,index=signif.index,columns=[fnames[j]+'_'+cnames[i]])
            signif=signif.join(s)
            
    return IC,tstat,signif

 
alpha=0.05
########################################context: Value
factor=[eps,sps,prof_mar,roic,ninc,cfo,cf,sg,mom,cfni,art,goodwill,leve,inv_turn,quick,a_turn]
context=[pe,pb]
fnames=["eps",'sps','prof_mar','roic','ninc','cfo','cf','sg','mom','cfni','art','goodwill','leve','inv_turn','quick','a_turn']
cnames=['pe','pb']          
v,std,sig=IC_cont(factor,context,fnames,cnames,alpha)
v.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Value.csv")
std.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Value.csv")
sig.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Value.csv")

#########################################context: beta
beta=pd.read_csv("beta.csv")
beta.index=pd.to_datetime(beta['Date'])
beta=beta.iloc[:,1:]
beta=beta.fillna(method="bfill",axis=0)
beta=beta.asfreq('M',method='ffill')

#factor contains growth market quality value
factor=reserved
fnames=rnames
b,std_b,sig_b=IC_cont(factor,[beta],fnames,['beta'],alpha)
b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Beta.csv")
std_b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Beta.csv")
sig_b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Beta.csv")






#########################################context: unsystemetic risk
unsys=pd.read_csv("unsystemetic risk.csv")
unsys.index=pd.to_datetime(unsys['Date'])
unsys=unsys.fillna(method="bfill",axis=0)
unsys=unsys.asfreq('M',method='ffill')
#factor contains growth market quality value
un_risk,std_un,sig_un=IC_cont(reserved,[unsys],rnames,['unsys'],alpha)
un_risk.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_risk.csv")
std_un.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_risk.csv")
sig_un.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_risk.csv")



"""
#########################################context:sector
sec=pd.read_csv("S&P500_gic_sector_code.csv")
sec.index=pd.to_datetime(sec['Date'])
sec=sec.fillna(method="bfill",axis=0)
sec=sec.asfreq('M',method='ffill')

#factor contains growth market quality value
factor=[eps,sps,prof_mar,lgro,roic,ninc,gmar,cfo,cf,sg,mom,cfni,art,ar,goodwill,leve,tar,rc,inv_turn,spread,quick,a_turn,fpe,fpb,pe,pb]
fnames=['eps','sps','prof_mar','lgro','roic','ninc','gmar','cfo','cf','sg','mom','cfni','art','ar','goodwill','leve','tar','rc','inv_turn','spread','quick','a_turn','fpe','fpb','pe','pb']
s,std_s,sig_s=IC_cont(factor,[sec],fnames,['sec'],alpha)
s.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Sector.csv")
std_s.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Sector.csv")
sig_s.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Sector.csv")

"""

#########################################context: liquidity
#factor:growth value quality(except for liquidity)
factor=[eps,sps,prof_mar,roic,ninc,cfo,cf,sg,cfni,art,goodwill,leve,pe,pb]
fnames=['eps','sps','prof_mar','roic','ninc','cfo','cf','sg','cfni','art','goodwill','leve','pe','pb']
context=[inv_turn,quick,a_turn]
cnames=['inv_turn','quick','a_turn']

l,std_l,sig_l=IC_cont(factor,context,fnames,cnames,alpha)
l.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Liquidity.csv")
std_l.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Liquidity.csv")
sig_l.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Liquidity.csv")


#########################################context:size
size=pd.read_csv("S&P500_CUR_MKT_CAP.csv")
size.index=pd.to_datetime(size["Date"])
size=size.fillna(method="bfill",axis=0)
size=size.asfreq("M",method="ffill")


#factor contains growth market quality value
factor=reserved
fnames=rnames
si,std_si,sig_si=IC_cont(factor,[size],fnames,['size'],alpha)
si.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Size.csv")
std_si.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Size.csv")
sig_si.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Size.csv")




#########################################context:growth
#factor contains market value quality
factor=[pe,pb,mom,cfni,art,goodwill,leve,inv_turn,quick,a_turn]
fnames=['pe','pb','mom','cfni','art','goodwill','leve','inv_turn','quick','a_turn']
context=[eps,sps,prof_mar,roic,ninc,cfo,cf,sg]
cnames=["eps",'sps','prof_mar','lgro','roic','ninc','cfo','cf','sg']

g,std_g,sig_g=IC_cont(factor,context,fnames,cnames,alpha)
g.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Growth.csv")
std_g.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Growth.csv")
sig_g.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Growth.csv")





            
            
            
            
            
            
            
            