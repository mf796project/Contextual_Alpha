# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 16:01:20 2019

@author: yumeng cui
"""
#split to sub-universe based on contextual cluster
import numpy as np
import pandas as pd
from scipy import stats
from tabulate import tabulate
import matplotlib.pyplot as plt

#deal with single risk factor per time

class constr_port():
    def __init__(self,rets,riskFactors,alphaFactors,nStocks = 15,signiLevel = 0.05):
        #stocks = stock prices  formed as T+1*K
        #riskFactors: raw factor data, formed as T*K(tickers), dataframe
        #alphaFactors: raw factor data, formed as dict
        #special_handling = 'unsystemetic_risk'/'sector'/'momentum'  
        self.rets = rets
        self.date = self.rets.index.values
        self.riskFactors = riskFactors
        self.alphaFactors = alphaFactors
        self.signiLevel = signiLevel
        self.T = len(self.rets.index.values)
        self.tickers = self.rets.columns.values
        self.alphas =  pd.Series(list(alphaFactors.keys()))
        self.K = self.rets.shape[1]#number of stocks
        self.nStocks = nStocks

        
    

    def get_partitionIndex(self,weights = 0.3):
        n = int(np.floor(self.riskFactors.shape[1]*weights))
        lowIndex = pd.DataFrame()
        highIndex = pd.DataFrame()
        for t in self.date:
            x = self.riskFactors.loc[t,:]
            sortedIndex = np.argsort(x)
            if max(sortedIndex) >= 2*n - 1 :
                sortedIndex = sortedIndex[sortedIndex!=-1].sort_values()
                lowIndex[t] = sortedIndex.index.values[:n] #take first 40%
                highIndex[t] = sortedIndex.index.values[-n:] #take last 40%
            else: 
                lowIndex[t] = np.repeat(np.NaN,n)
                highIndex[t] = np.repeat(np.NaN,n)
        self.lowIndex = lowIndex.T.dropna(how = 'all')
        self.highIndex = highIndex.T.dropna(how = 'all')
        if self.lowIndex.shape[0] < self.T:
            self.date = pd.Series(self.lowIndex.index.values.tolist())
            self.T = self.lowIndex.shape[0] 
        
        
        
        
        
        
    def get_lowIC(self,key): 
        #return stocks with low risk factor (40%) for all alpha factors
        lowIC = pd.Series(index = self.date[:-1])
        for t,t1 in zip(self.date[:-1],self.date[1:]):
#            print(t)
            stockIndex = self.lowIndex.loc[t]
            f = self.alphaFactors[key][stockIndex].loc[t].dropna()
#            print('2')
            r = self.rets[stockIndex].loc[t1].dropna()
#            print('3')
            with np.errstate(all ='ignore'):
                lowIC.at[t] = r.corr(f)
        return lowIC
        
    def get_highIC(self,key): 
        #return stocks with low risk factor (40%) for all alpha factors
        highIC = pd.Series(index = self.date[:-1])
        for t,t1 in zip(self.date[:-1],self.date[1:]):
            stockIndex = self.highIndex.loc[t]
#            print('1')
            f = self.alphaFactors[key][stockIndex].loc[t]
            r = self.rets[stockIndex].loc[t1]
            with np.errstate(all='ignore'):
                highIC.at[t] = r.corr(f)
        return highIC
    
    def get_total_IC(self,ics = None):
        
#        if given is None:
#            highIC = pd.DataFrame()
#            lowIC = pd.DataFrame()
#            for key in self.alphas:
#                highIC[key] = self.get_highIC(key)
#                lowIC[key] = self.get_lowIC(key)
#            
#        else:

        n = int(ics.shape[1]/2)
        lowIC = ics.iloc[:,range(0,2*n,2)]
        highIC = ics.iloc[:,range(1,2*n,2)]
        highIC.columns = lowIC.columns.values
        self.T = lowIC.shape[0]
        self.alphas = pd.Series(lowIC.columns.values)
        self.highIC = highIC
        self.lowIC = lowIC
        self.date = pd.Series(self.lowIC.index.values.tolist())
        self.T = self.lowIC.shape[0]
    
    
    def ide_alpha(self,given=None):
        
        self.get_total_IC(given)
        #check if the alpha factor is statistically significant
#        highMean = self.highIC.mean()
#        lowMean = self.lowIC.mean()
        highVol = self.highIC.std()
        lowVol = self.lowIC.std()
        #two sample t-test
        self.F = highVol / lowVol
        df1 = self.T - 1
        df2 = self.T - 1
        self.p_f = stats.f.sf(self.F, df1, df2)
        self.t,self.p_t = stats.ttest_ind(self.highIC,self.lowIC,equal_var = [self.p_f > 0.05],nan_policy = 'omit')
        self.alphaIndex = np.where(self.p_t<self.signiLevel)
        #f test for variance

        self.surAlpha = self.alphas.iloc[self.alphaIndex]      #list
        self.nAlpha = len(self.surAlpha)
        try:
            self.ifkeep = 1/self.nAlpha
            print('Effective alphas are', self.surAlpha.values)
        except ZeroDivisionError:
            print('no alpha factor found')
            self.ifkeep = False           
             
    def weighting_scheme(self):
        #turn risk partitions into weighting ( IR weighting )
        
        self.alphaModel_high = self.highIC[self.surAlpha] 
        self.alphaModel_low = self.lowIC[self.surAlpha]  
        
        SigmaHigh = self.alphaModel_high.cov()
        weightsHigh = np.dot(np.linalg.inv(SigmaHigh), self.alphaModel_high.mean().T)
        
        self.weightsHigh = weightsHigh/np.sum(weightsHigh) #weighting alphas np.array
        
        SigmaLow = self.alphaModel_low.cov()
        weightsLow = np.dot(np.linalg.inv(SigmaLow), self.alphaModel_low.mean().T)
        
        self.weightsLow = weightsLow/np.sum(weightsLow) #weighting alphas np.array
        
    def constr_alphaAssets(self):
        
        n = self.nStocks
        
        alphaAssetHigh = pd.DataFrame(dtype = float)
        alphaAssetLow = pd.DataFrame(dtype = float)
        alphaHighBuy = pd.DataFrame(dtype = float)
        alphaHighSell = pd.DataFrame(dtype = float)
        alphaLowBuy = pd.DataFrame(dtype = float)
        alphaLowSell = pd.DataFrame(dtype = float)
        
        for key in self.surAlpha.values:
            
            for t,t1 in zip(self.date[:-1],self.date[1:]):
                #high                
                aFHigh = self.alphaFactors[key][self.highIndex.loc[t]].loc[t]
                sortedIndex = np.argsort(aFHigh)
                sortedIndex = sortedIndex.replace(-1,np.NaN)
                x1 = sortedIndex[sortedIndex < n].index.values #low
                with np.warnings.catch_warnings():
                    np.warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')
                    x2 = sortedIndex[sortedIndex >  np.nanmax(sortedIndex)-n].index.values #high
                r1 = self.rets[x1].loc[t1]
                r2 = self.rets[x2].loc[t1]
                r = r2.mean()-r1.mean()
                alphaAssetHigh.at[t1,key] = r
                #low
                aFLow = self.alphaFactors[key][self.lowIndex.loc[t]].loc[t]
                sortedIndex = np.argsort(aFLow)
                sortedIndex = sortedIndex.replace(-1,np.NaN)
                x1 = sortedIndex[sortedIndex < n].index.values #low
                with np.warnings.catch_warnings():
                    np.warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')
                    x2 = sortedIndex[sortedIndex >=  np.nanmax(sortedIndex)-n].index.values #high
                r1 = self.rets[x1].loc[t1]
                r2 = self.rets[x2].loc[t1]
                r = r2.mean()-r1.mean()
                alphaAssetLow.at[t1,key] = r
             
            t = self.date.iloc[-1]
            aFHigh = self.alphaFactors[key][self.highIndex.loc[t]].loc[t]
            sortedIndex = np.argsort(aFHigh)
            sortedIndex = sortedIndex.replace(-1,np.NaN)
            alphaHighSell[key] =  sortedIndex[sortedIndex < n].index.values #low
            alphaHighBuy[key] = sortedIndex[sortedIndex >  np.nanmax(sortedIndex)-n].index.values #high

            aFLow = self.alphaFactors[key][self.lowIndex.loc[t]].loc[t]
            sortedIndex = np.argsort(aFLow)
            sortedIndex = sortedIndex.replace(-1,np.NaN)
            alphaLowSell[key] =sortedIndex[sortedIndex < n].index.values #low
            alphaLowBuy[key] = sortedIndex[sortedIndex >  np.nanmax(sortedIndex)-n].index.values #high
                            
        self.alphaHighSell = alphaHighSell
        self.alphaHighBuy = alphaHighBuy
        self.alphaLowBuy = alphaLowBuy
        self.alphaLowSell = alphaLowSell
        
        self.alphaAssetHigh = alphaAssetHigh        
        self.alphaAssetLow  = alphaAssetLow 
        
    def constr_riskAsset(self):#weights = [high,low]
        
        weightsRisk = pd.DataFrame(dtype = float)
        for key in self.surAlpha:
            covv = self.alphaAssetHigh[key].cov(self.alphaAssetLow[key])
            SigmaRisk = np.array([[self.alphaAssetHigh[key].var(),covv],[covv,self.alphaAssetLow[key].var()]])
            w =  np.dot(np.linalg.inv(SigmaRisk), np.array([self.alphaAssetHigh.mean().loc[key],self.alphaAssetLow.mean().loc[key]]).T)
            weightsRisk[key] = (w/np.sum(w)).round(2)
        self.weightRisk = weightsRisk

        #risk asset historical based on today's optimization
        
        riskAsset = (self.alphaAssetHigh*self.weightsHigh*weightsRisk.iloc[0,:].values).sum(axis = 1) +(self.alphaAssetLow *self.weightsLow*self.weightRisk.iloc[1,:].values).sum(axis = 1)
        return riskAsset
    
    def print_ttTest(self):
        print(tabulate(np.array([self.t,self.p_t]).T, headers=['two sample t-stat', 'pValue']))
        
    def print_fTest(self):
        print(tabulate(np.array([self.F,self.p_f]).T, headers=['F-stat', 'pValue']))
        print('df1=df2=%f' %(self.T-1))
    def print_IC_stat(self):
        print('low ic summary')
        print(self.lowIC.describe())
        print('high ic summary')
        print(self.highIC.describe())
        
    
    
def constr_crPort(riskAssets): #construct cross risk factor port
    Sigma = riskAssets.cov()
    weights = np.dot(np.linalg.inv(Sigma), riskAssets.mean().T)
    return weights/weights.sum()
    

def constr_rollingPort(ret,riskFactor,Factors,cc,n = 30):
    T = ret.shape[0]
#    

    profit = np.zeros(n)
    aI = {}
    for i in range(n):
        print(i+1)
        r= ret.iloc[T-n+i]
        index = ret.index.values[:T-n+i]
        
        riskAsset = pd.DataFrame(dtype = float)
        rSingleRisk = []
        objs  = {}
        for keys,values in riskFactor.items():
             print(keys)
             riskFactors = Factors[keys].loc[index]
             alphaFactors = {key: value.loc[index] for key, value in Factors.items() if key in values}
             ics = cc[keys].loc[:index[-1]]
             obj = constr_port(ret.loc[index],riskFactors,alphaFactors)
             obj.ide_alpha(ics)             
             if obj.ifkeep != False:
                objs[keys] = obj
                obj.get_partitionIndex()
                obj.constr_alphaAssets()
                obj.weighting_scheme()
                aI[(i,keys)] = obj.surAlpha
                riskAsset[keys] = obj.constr_riskAsset()
                alHigh = obj.alphaHighBuy.apply(lambda x:r.loc[x].reset_index(drop=True)).mean() - obj.alphaHighSell.apply(lambda x:r.loc[x].reset_index(drop=True)).mean()
                alLow = obj.alphaLowBuy.apply(lambda x:r.loc[x].reset_index(drop=True)).mean() - obj.alphaLowSell.apply(lambda x:r.loc[x].reset_index(drop=True)).mean()
                rAlphaHigh = alHigh*obj.weightsHigh * obj.weightRisk.iloc[0,:].values
                rAlphaLow = alLow*obj.weightsLow* obj.weightRisk.iloc[0,:].values
                r_port = rAlphaHigh.sum() +  rAlphaLow.sum()
                rSingleRisk.append(r_port)
                
        weightsForRisk = constr_crPort(riskAsset)
        r_total = (np.array(rSingleRisk)*weightsForRisk).sum()
        profit[i] = r_total       
    return profit
                
   

    
#    
if __name__=='main':

    
#    pool = pd.read_csv('pools.csv',index_col = False).Pool    

#
#    stocks1 = pd.read_csv(r'C:\Users\mdejg\Documents\GitHub\Contextual_Alpha\mat_data\S&P500_clsprc.csv',index_col=0)
#    stocks = stocks1[pool].loc[dates]
#    rets = np.log(stocks/stocks.shift(1)).dropna(how='all')
#     rets = rets.replace(0,np.NaN)
#    names = pd.read_excel('Abbr_FileName.xlsx',index_col=3)
#    allAlpha = np.array(names.index.values[:-3])
#    
#    Factors = {}
#    fail = []
#    
#    for key in allAlpha:
#        try:
#            data = pd.read_csv(r'C:\Users\mdejg\Documents\GitHub\Contextual_Alpha\mat_data\%s' %names['FileName'].loc[key],index_col = 0)
#            data = data[pool]
#            if data.shape[0] < 200:
#                data = data.loc[data.index.repeat(3)].reset_index(drop=True)
#                data.index = dates
#            else:
#                data = data.loc[dates]
#            Factors[key] = data
#        except KeyError:
#            print(names.FileName.loc[key])
#            pass
#     
#    Factors['beta'] = pd.read_csv(r'C:\Users\mdejg\Documents\GitHub\Contextual_Alpha\mat_data\S&P500_BETA_ADJ_OVERRIDABLE.csv',index_col = 0)[pool].iloc[:-3]
#    Factors['size'] = pd.read_csv(r'C:\Users\mdejg\Documents\GitHub\Contextual_Alpha\mat_data\S&P500_CUR_MKT_CAP.csv',index_col = 0)[pool].iloc[:-3]

#     
#    a = pd.read_csv('Context_factor_Alpha_factor_final.csv')
#    riskFactor = {}
#    for key in a.columns.values:
#         riskFactor[key] = a[key].dropna().values
#         
#    del riskFactor['unsys']
#    del riskFactor['beta']
#    del riskFactor['sg']
#    del riskFactor['eps']
#    del riskFactor['sps']
#    del riskFactor['prof_mar']
#    del riskFactor['ninc']
##    
#    b =  pd.Series(dates,index = dates)
#    cc = {}
#    for k in riskFactor.keys():
#          a = pd.read_csv('IC_%s.csv' %k,index_col=0, parse_dates=['Date'])
#          index = b.loc[str(a.index.values[0])[:10]:str(a.index.values[-1])[:10]]
#          a.index = index.values
#          cc[k] = a
    
#    objs = {}
#    aI = {}
#    riskAsset = pd.DataFrame(dtype = float)
#     #apply strategy for each risk factor
#    for keys,values in riskFactor.items():
#         print(keys)
#         riskFactors = Factors[keys]
#         alphaFactors = {key: value for key, value in Factors.items() if key in values}
#         ics = cc[keys]
#         obj = constr_port(rets,riskFactors,alphaFactors)
#         obj.ide_alpha(ics)
#         if obj.ifkeep != False:
#            obj.get_partitionIndex()
#            obj.constr_alphaAssets()
#            objs[keys] = obj
#            aI[keys] = obj.surAlpha
#            obj.weighting_scheme()
#            riskAsset[keys] = obj.constr_riskAsset()
            
#construct rolling port  
            
     p = constr_rollingPort(rets,riskFactor,Factors,cc,30)
         
         
         

     
    
