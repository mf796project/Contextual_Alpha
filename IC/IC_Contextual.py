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



def IC_cont(factor,context,fnames,cnames,alpha,new_IC_Whole):
    IC=pd.DataFrame(index=factor[0].index)
   
    mean_c=pd.DataFrame(index=["LOW","MID","HIGH"])
    std=pd.DataFrame(index=["LOW","MID","HIGH"])
   
    tstat=pd.DataFrame(index=["L_M","M_H","L_H"])
    signif=pd.DataFrame(index=["L_M","M_H","L_H"])
    
    p=pd.DataFrame(index=["L_M","M_H","L_H"])
    sigdf=pd.DataFrame(index=["L_M","M_H","L_H"])
    
    for i in range(len(context)):
        for j in range(len(factor)):
            a=find_IC_cont(constit,rets,factor[j],context[i])            
            a.columns=['LOW_'+fnames[j]+'_'+cnames[i],'MID_'+fnames[j]+'_'+cnames[i],'HIGH_'+fnames[j]+'_'+cnames[i]]
            IC=IC.join(a,how="right")
            
            m=pd.DataFrame(a.mean(axis=0)*12)
            m.index=mean_c.index
            m.columns=[fnames[j]+'_'+cnames[i]]
            mean_c=mean_c.join(m)
            
            stdev=pd.DataFrame(a.std(axis=0)*np.sqrt(12))
            stdev.index=std.index
            stdev.columns=[fnames[j]+'_'+cnames[i]]
            std=std.join(stdev)
            
            
            b=a.join(pd.DataFrame(new_IC_Whole[fnames[j]]))
            b=b.dropna(axis=0,how="any")
            lu=st.ttest_ind(b.iloc[:,0],b.iloc[:,3]).pvalue
            mu=st.ttest_ind(b.iloc[:,1],b.iloc[:,3]).pvalue
            hu=st.ttest_ind(b.iloc[:,2],b.iloc[:,1]).pvalue
            tt=[lu,mu,hu]
            dd=pd.DataFrame(tt,index=tstat.index,columns=[fnames[j]+'_'+cnames[i]])
            p=p.join(dd)
            
            sig=[0,0,0]
            for x in range(len(tt)):
                if tt[x]<alpha:
                    sig[x]=1
                    
            s=pd.DataFrame(sig,index=sigdf.index,columns=[fnames[j]+'_'+cnames[i]])
            sigdf=sigdf.join(s)
            
            
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
            
    return IC,tstat,signif,mean_c,std,p,sigdf

 
alpha=0.05
########################################context: Value
factor=[eps,sps,prof_mar,roic,ninc,cfo,cf,sg,mom,cfni,art,goodwill,leve,quick,a_turn]
context=[pe,pb]
fnames=["eps",'sps','prof_mar','roic','ninc','cfo','cf','sg','mom','cfni','art','goodwill','leve','quick','a_turn']
cnames=['pe','pb']          
v,std,sig,m,sd,pu,sigu=IC_cont(factor,context,fnames,cnames,alpha,new_IC_Whole)
v.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Value.csv")
std.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Value.csv")
sig.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Value.csv")
m.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/mean_Value.csv")
sd.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/std_Value.csv")
pu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/pu_Value.csv")
sigu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sigu_Value.csv")

#########################################context: beta
beta=pd.read_csv("S&P500_BETA_ADJ_OVERRIDABLE.csv")
beta.index=pd.to_datetime(beta['Date'])
#beta=beta.fillna(method="bfill",axis=0)
beta=beta.asfreq('M',method='ffill')

#factor contains growth market quality value
factor=reserved[0:15]
fnames=rnames[0:15]
b,std_b,sig_b,m_b,sd_b,pu,sigu=IC_cont(factor,[beta],fnames,['beta'],alpha,new_IC_Whole)
b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Beta.csv")
std_b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Beta.csv")
sig_b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Beta.csv")
m_b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/mean_Beta.csv")
sd_b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/std_Beta.csv")
pu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/pu_Beta.csv")
sigu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sigu_Beta.csv")




#########################################context: unsystemetic risk
"""
unsys=pd.read_csv("unsystemetic risk.csv")
unsys.index=pd.to_datetime(unsys['Date'])
unsys=unsys.fillna(method="ffill",axis=0)
unsys=unsys.asfreq('M',method='ffill')
#factor contains growth market quality value
un_risk,std_un,sig_un,m_un,sd_un,pu,sigu=IC_cont(reserved,[unsys],rnames,['unsys'],alpha,new_IC_Whole)
un_risk.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_risk.csv")
std_un.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_risk.csv")
sig_un.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_risk.csv")
m_un.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/mean_risk.csv")
sd_un.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/std_risk.csv")
pu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/pu_risk.csv")
sigu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sigu_arisk.csv")
"""
#########################################context: liquidity
#factor:growth value quality(except for liquidity)
"""
factor=[eps,sps,prof_mar,roic,ninc,cfo,cf,sg,cfni,art,goodwill,leve,pe,pb]
fnames=['eps','sps','prof_mar','roic','ninc','cfo','cf','sg','cfni','art','goodwill','leve','pe','pb']
context=[quick,a_turn]
cnames=['quick','a_turn']

l,std_l,sig_l,m,sd,pu,sigu=IC_cont(factor,context,fnames,cnames,alpha,new_IC_Whole)
l.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Liquidity.csv")
std_l.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Liquidity.csv")
sig_l.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Liquidity.csv")
m.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/mean_Liquidity.csv")
sd.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/std_Liquidity.csv")
pu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/pu_Liquidity.csv")
sigu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sigu_Liquidity.csv")
"""
#########################################context:size
size=pd.read_csv("S&P500_CUR_MKT_CAP.csv")
size.index=pd.to_datetime(size["Date"])
size=size.fillna(method="ffill",axis=0)
size=size.asfreq("M",method="ffill")


#factor contains growth market quality value
factor=[eps,sps,prof_mar,roic,ninc,cfo,cf,sg,mom,pe,pb]
fnames=['eps','sps','prof_mar','roic','ninc','cfo','cf','sg','mom','pe','pb']
si,std_si,sig_si,m,sd,pu,sigu=IC_cont(factor,[size],fnames,['size'],alpha,new_IC_Whole)
si.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Size.csv")
std_si.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Size.csv")
sig_si.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Size.csv")
m.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/mean_Size.csv")
sd.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/std_Size.csv")
pu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/pu_Size.csv")
sigu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sigu_Size.csv")


#########################################context:growth
#factor contains market value quality
factor=[pe,pb,mom,cfni,art,goodwill,leve,quick,a_turn]
fnames=['pe','pb','mom','cfni','art','goodwill','leve','quick','a_turn']
context=[eps,sps,prof_mar,roic,ninc,cfo,cf,sg]
cnames=["eps",'sps','prof_mar','lgro','roic','ninc','cfo','cf','sg']

g,std_g,sig_g,m,d,pu,sigu=IC_cont(factor,context,fnames,cnames,alpha,new_IC_Whole)
g.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/IC_Growth.csv")
std_g.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/ttest_Growth.csv")
sig_g.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sig_Growth.csv")
m.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/mean_Growth.csv")
sd.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/std_Growth.csv")
pu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/pu_Growth.csv")
sigu.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/sigu_Growth.csv")


            
            
            
            
            
            
            
            