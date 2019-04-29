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
    IC=pd.DataFrame(index=rets.index)
   
    mean_c=pd.DataFrame(index=["LOW","HIGH"])
    std=pd.DataFrame(index=["LOW","HIGH"])
   
    tstat=pd.DataFrame(index=["L_H"])
    signif=pd.DataFrame(index=["L_H"])
    
    p=pd.DataFrame(index=["L","H"])
    sigdf=pd.DataFrame(index=["L","H"])
    
    for i in range(len(context)):
        for j in range(len(factor)):
            a=find_IC_cont(constit,rets,factor[j],context[i])[["LOW","HIGH"]]            
            a.columns=['LOW/'+fnames[j]+"/"+cnames[i],'HIGH/'+fnames[j]+"/"+cnames[i]]
            IC=IC.join(a,)
            
            m=pd.DataFrame(a.mean(axis=0))
            m.index=mean_c.index
            m.columns=[fnames[j]+"/"+cnames[i]]
            mean_c=mean_c.join(m)
            
            stdev=pd.DataFrame(a.std(axis=0))
            stdev.index=std.index
            stdev.columns=[fnames[j]+"/"+cnames[i]]
            std=std.join(stdev)
            
            
            b=a.join(pd.DataFrame(new_IC_Whole[fnames[j]]))
            b=b.dropna(axis=0,how="any")
            lu=st.ttest_ind(b.iloc[:,0],b.iloc[:,2]).pvalue
            #mu=st.ttest_ind(b.iloc[:,1],b.iloc[:,3]).pvalue
            hu=st.ttest_ind(b.iloc[:,1],b.iloc[:,2]).pvalue
            tt=[lu,hu]
            dd=pd.DataFrame(tt,index=p.index,columns=[fnames[j]+"/"+cnames[i]])
            p=p.join(dd)
            
            sig=[0,0]
            for x in range(len(tt)):
                if tt[x]<alpha:
                    sig[x]=1
                    
            s=pd.DataFrame(sig,index=sigdf.index,columns=[fnames[j]+"/"+cnames[i]])
            sigdf=sigdf.join(s)
            
            
            a=a.dropna(axis=0,how="any")
            #lm=st.ttest_ind(a.iloc[:,0],a.iloc[:,1]).pvalue
            #mh=st.ttest_ind(a.iloc[:,1],a.iloc[:,2]).pvalue
            lh=st.ttest_ind(a.iloc[:,0],a.iloc[:,1]).pvalue
            t=[lh]
            df=pd.DataFrame(t,index=tstat.index,columns=[fnames[j]+"/"+cnames[i]])
            tstat=tstat.join(df)
            
            sig=[0]
            for x in range(len(t)):
                if t[x]<alpha:
                    sig[x]=1
                    
            s=pd.DataFrame(sig,index=signif.index,columns=[fnames[j]+"/"+cnames[i]])
            signif=signif.join(s)
            
    return IC,tstat,signif,mean_c,std,p,sigdf

 
alpha=0.05
"""
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
#beta=beta.iloc[:,1:]
beta=beta.fillna(method="ffill",axis=0)
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



"""
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
"""
#factor:growth value quality(except for liquidity)
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
"""
#########################################context:size
"""
size=pd.read_csv("S&P500_CUR_MKT_CAP.csv")
size.index=pd.to_datetime(size["Date"])
size=size.fillna(method="ffill",axis=0)
size=size.asfreq("M",method="ffill")

"""
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

"""
#Combined factors
"""

#############################################    combined growth
###context: size
ic,std_si,sig_si,m,sd,pu,sigu=IC_cont([comgro],[size],['comgro'],['size'],alpha,new_IC_Whole)
ic.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedGrowth_conIC_size.csv")
std_si.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedGrwoth_ttest_size.csv")

###context Value       
context=[pe,pb]           
cnames=['pe','pb']       
ic_v,std_v,sig_v,m_v,sd_v,pu_v,sigu_v=IC_cont([comgro],context,["comgro"],cnames,alpha,new_IC_Whole)
ic_v.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedGrowth_conIC_value.csv")
std_v.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedGrwoth_ttest_value.csv")            

#Combined quality       
"""            
comqual=pd.read_csv("S&P500_Combined_Quality.csv")  
#comqual=comqual.iloc[:-5,:]
comqual.index=pd.to_datetime(comqual["Date"])
comqual=comqual.asfreq("M",method="ffill")

Comqual=find_IC(constit,rets,comqual)
Comqual.columns=["comqual"]
new_IC_Whole["comqual"]=Comqual

"""
#######growth
context=[eps,sps,prof_mar,roic,ninc,cfo,cf,sg]
cnames=["eps",'sps','prof_mar','lgro','roic','ninc','cfo','cf','sg']

ic_g,std_g,sig_g,m,sd,pu,sigu=IC_cont([comqual],context,['comqual'],cnames,alpha,new_IC_Whole)
ic_g.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedQuality_conIC_growth.csv")
std_g.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedQuality_ttest_growth.csv")

#######value
context=[pe,pb]           
cnames=['pe','pb']       
ic_v,std_v,sig_v_1,m_v_1,sd_v_1,pu_v_1,sigu_v_1=IC_cont([comqual],context,["comqual"],cnames,alpha,new_IC_Whole)
ic_v.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedQuality_conIC_value.csv")
std_v.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedQuality_ttest_value.csv")            

####### beta
ic_b,std_b,sig_b,m_b,sd_b,pu_b,sigu_b=IC_cont([comqual],[beta],["comqual"],["beta"],alpha,new_IC_Whole)
ic_b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedQuality_conIC_beta.csv")
std_b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedQuality_ttest_beta.csv")            
         
######size
ic_si_1,std_si_1,sig_si_1,m_si_1,sd_si_1,pu_si_1,sigu_si_1=IC_cont([comqual],[size],['comqual'],['size'],alpha,new_IC_Whole)
ic_si_1.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedQuality_conIC_size.csv")
std_si_1.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/CombinedQuality_ttest_size.csv")       






"""
# context： size pe
comval=pd.read_csv("S&P500_Combined_Value.csv")  
#comval=comval.iloc[:-5,:]
comval.index=pd.to_datetime(comval["Date"])
comval=comval.asfreq("M",how='end',method="ffill")

Comval=find_IC(constit,rets,comval)
Comval.columns=["comval"]
#new_IC_Whole=new_IC_Whole.iloc[:,:-1]
new_IC_Whole["comval"]=Comval



factor=[comgro,comqual,comval,mom]
fnames=['comgro','comqual','comval','mom']
context=[pe]
cnames=['pe']

a,b,c,d,e,f,g=IC_cont(factor,context,fnames,cnames,alpha,new_IC_Whole)
a.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/4FactorIC_Value.csv")
b.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/4Factor_pvalue_Value.csv")
d.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/4Factor_mean_Value.csv")
e.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/4Factor_std_Value.csv")
"""
"""

factor=[comgro,comqual,comval,mom]
fnames=['comgro','comqual','comval','mom']
context=[size]
cnames=['size']

a1,b1,c1,d1,e1,f1,g1=IC_cont(factor,context,fnames,cnames,alpha,new_IC_Whole)
a1.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/4FactorIC_Size.csv")
b1.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/4Factor_pvalue_Size.csv")
d1.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/4Factor_mean_Size.csv")
e1.to_csv("C:/Users/Yadi Xie/Desktop/MF796 Project/Contextual_Alpha/IC/4Factor_std_Size.csv")






























     