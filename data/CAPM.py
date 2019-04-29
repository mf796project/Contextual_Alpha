# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:08:14 2019

@author: Yadi Xie
"""
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

#calculate beta and unsystemetic risk for each company

spy=pd.read_csv("S&P500_index.csv") #daily SPY index
spy.index=pd.to_datetime(spy["Date"])
spy=spy.iloc[:,1:]
spy=spy.dropna(axis=0,how="all") 

rf=pd.read_csv("S&P500_rf.csv")
rf.index=pd.to_datetime(rf["Date"])
rf=rf.iloc[:,1:]
rf=rf.dropna(axis=0,how="all")
rf=rf.asfreq("D",method="ffill")/252

price=pd.read_csv("S&P500_clsprc.csv") #close price for all stocks
price.index=pd.to_datetime(price['Date']) 
price=price.iloc[:,1:] 
price=price.dropna(axis=1,how="all") # drop stocks with na all the time
price=price.dropna(axis=0,how="all")  # drop times with na for all stocks
   
ret_d=np.log(price.shift(-1)/price)
ret_d=ret_d.iloc[:-1,]

mret_d=np.log(spy.shift(-1)/spy)
mret_d=mret_d.iloc[:-1,]

win=3 #define a rolling window with length of three months
  
def CAPM(mret_d,ret_d,rf,win):
    time=mret_d.index&ret_d.index
    time=time&rf.index
    ret_d=ret_d.reindex(time) # remain days when both spy and price data exist
    mret_d=mret_d.reindex(time) # remain days when both spy and price data exist
    rf=rf.reindex(time)
    #start=time[0]+relativedelta(month=win//21+1) # rolling starts from the first day of the forth month
    
    beta=pd.DataFrame()
    unsys=pd.DataFrame()
    index=[19,41,61]
    
    b=pd.DataFrame(index=ret_d.index,columns=ret_d.columns)
    b=b.fillna(0)
    un=pd.DataFrame(index=ret_d.index,columns=ret_d.columns)
    un=un.fillna(0)
    
    for i in range(62,len(time)-1):
        mar=mret_d.loc[time[i]-relativedelta(months=win):time[i+1]]
        ind=ret_d.loc[time[i]-relativedelta(months=win):time[i+1]]
        r=rf.loc[time[i]-relativedelta(months=win):time[i+1]]
        
        for j in range(len(ind.iloc[0,])):
            a=mar.join(r)
            b.iloc[i,j]=np.cov(a.iloc[:,0]-a.iloc[:,1],ind.iloc[:,j]-a.iloc[:,1])[0,1]/np.var(a.iloc[:,0]-a.iloc[:,1])
            un.iloc[i,j]=np.var(ind.iloc[:,j]-a.iloc[:,1])-b.iloc[i,j]**2*np.var(a.iloc[:,0]-a.iloc[:,1])
            
        if time[i].month<time[i+1].month or (time[i].month==12 and time[i].day==31):
            if i==83:
                for t in range(4):
                    beta=beta.append(b.loc[time[i+1]-relativedelta(months=1):time[i+1]].mean(axis=0),ignore_index=True)
                    unsys=unsys.append(un.loc[time[i+1]-relativedelta(months=1):time[i+1]].mean(axis=0),ignore_index=True)
                
                index.append(i)
            else:
                beta=beta.append(b.loc[time[i+1]-relativedelta(months=1):time[i+1]].mean(axis=0),ignore_index=True)
                unsys=unsys.append(un.loc[time[i+1]-relativedelta(months=1):time[i+1]].mean(axis=0),ignore_index=True)
                index.append(i)
    
   
    beta.index=time[index]
    unsys.index=time[index]
    
    beta=pd.DataFrame(beta.index,index=beta.index).join(beta)
    unsys=pd.DataFrame(unsys.index,index=unsys.index).join(unsys)
    
    return beta,unsys     


beta,unsys=CAPM(mret_d,ret_d,rf,win)
beta.to_csv("beta.csv")
unsys.to_csv("unsystemetic risk.csv")

"""
time=mret_d.index&ret_d.index
time=time&rf.index
ret_d=ret_d.reindex(time) # remain days when both spy and price data exist
mret_d=mret_d.reindex(time) # remain days when both spy and price data exist
    #start=time[0]+relativedelta(month=win//21+1) # rolling starts from the first day of the forth month
rf=rf.reindex(time)


ret_d=ret_d.iloc[0:1000,0:10]
mret_d=mret_d.iloc[0:1000]
rf=rf.iloc[0:1000]
time=time[0:1000]


beta=pd.DataFrame()
unsys=pd.DataFrame()
index=[19,41,61]

b=pd.DataFrame(index=time,columns=ret_d.columns)
b=b.fillna(1)    
un=pd.DataFrame(index=ret_d.index,columns=ret_d.columns)
un=un.fillna(1)
for i in range(62,len(time)-1):
    mar=mret_d.loc[time[i]-relativedelta(months=win):time[i]]
    ind=ret_d.loc[time[i]-relativedelta(months=win):time[i]]
    r=rf.loc[time[i]-relativedelta(months=win):time[i]]
    
    
    
    for j in range(len(ind.iloc[0,])):
        a=mar.join(r)
        #lm=LinearRegression().fit(np.array(a.iloc[:,0]-a.iloc[:,1]),np.array(ind.iloc[:,j]-a.iloc[:,1]))           
        b.iloc[i,j]=np.cov(a.iloc[:,0]-a.iloc[:,1],ind.iloc[:,j]-a.iloc[:,1])[0,1]/np.var(a.iloc[:,0]-a.iloc[:,1])#lm.coef_[0]
        un.iloc[i,j]=np.var(ind.iloc[:,j]-a.iloc[:,1])-b.iloc[i,j]**2*np.var(a.iloc[:,0]-a.iloc[:,1])
        
        
    if time[i].month<time[i+1].month:
        if i==83:            
            beta=beta.append(b.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
            unsys=unsys.append(un.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
            beta=beta.append(b.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
            unsys=unsys.append(un.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
            beta=beta.append(b.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
            unsys=unsys.append(un.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
            beta=beta.append(b.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
            unsys=unsys.append(un.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
                             
            index.append(i)
        else:
            beta=beta.append(b.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
            unsys=unsys.append(un.loc[time[i+1]-relativedelta(months=1):time[i]].mean(axis=0),ignore_index=True)
            index.append(i)
    
   # beta.index=time[index[2:]]
    #beta=pd.DataFrame(beta.iloc[0:2,:],beta.index[0:2],columns=beta.columns).append(beta)
beta.index=time[index]
unsys.index=time[index]
    #if time[i].month<time[i+1].month:
beta=pd.DataFrame(beta.index,index=beta.index).join(beta)
"""