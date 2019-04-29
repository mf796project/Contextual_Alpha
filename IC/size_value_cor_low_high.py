# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 15:23:09 2019

@author: Yadi Xie
"""
import pandas as pd
import numpy as np

v=pd.read_csv("4FactorIC_Value.csv")
s=pd.read_csv("4FactorIC_Size.csv")

high_v=v.iloc[:,[2,4,6,8]].dropna(axis=0,how="any")
low_v=v.iloc[:,[1,3,5,7]].dropna(axis=0,how="any")





cor_low_v=np.zeros((3,3))
cor_high_v=np.zeros((3,3))
Xh=high_v.iloc[:,[0,1,2]].dropna(axis=0,how="any")
Yh=high_v.iloc[:,[1,2,3]].dropna(axis=0,how="any")
Xl=low_v.iloc[:,[0,1,2]].dropna(axis=0,how="any")
Yl=low_v.iloc[:,[1,2,3]].dropna(axis=0,how="any")


for i in range(3):
    for j in range(3):
        cor_high_v[i,j]=np.corrcoef(Xh.iloc[:,i],Yh.iloc[:,j],rowvar=False)[0][1]
        cor_low_v[i,j]=np.corrcoef(Xl.iloc[:,i],Yl.iloc[:,j],rowvar=False)[0][1]







high_s=s.iloc[:,[2,4,6,8]].dropna(axis=0,how="any")
low_s=s.iloc[:,[1,3,5,7]].dropna(axis=0,how="any")


cor_low_s=np.zeros((3,3))
cor_high_s=np.zeros((3,3))
Xh=high_s.iloc[:,[0,1,2]].dropna(axis=0,how="any")
Yh=high_s.iloc[:,[1,2,3]].dropna(axis=0,how="any")
Xl=low_s.iloc[:,[0,1,2]].dropna(axis=0,how="any")
Yl=low_s.iloc[:,[1,2,3]].dropna(axis=0,how="any")


for i in range(3):
    for j in range(3):
        cor_high_s[i,j]=np.corrcoef(Xh.iloc[:,i],Yh.iloc[:,j],rowvar=False)[0][1]
        cor_low_s[i,j]=np.corrcoef(Xl.iloc[:,i],Yl.iloc[:,j],rowvar=False)[0][1]
        
cor_low_v=pd.DataFrame(cor_low_v,index=["grow","qual","val"],columns=["qual","val","mom"])
cor_high_v=pd.DataFrame(cor_high_v,index=["grow","qual","val"],columns=["qual","val","mom"])

cor_low_s=pd.DataFrame(cor_low_s,index=["grow","qual","val"],columns=["qual","val","mom"])
cor_high_s=pd.DataFrame(cor_high_s,index=["grow","qual","val"],columns=["qual","val","mom"])

cor_low_v.to_csv("cor_low_v.csv")
cor_high_v.to_csv("cor_high_v.csv")
cor_low_s.to_csv("cor_low_s.csv")
cor_high_s.to_csv("cor_high_s.csv")

