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

#deal with single risk factor per time

class constr_port():
    def __init__(self,rets,riskFactors,alphaFactors,test = 30,IC = None,signiLevel = 0.05):
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
        self.alphas = list(alphaFactors.keys())
        self.K = self.rets.shape[1]#number of stocks
        self.test = test


        
    

    def get_partitionIndex(self,weights = 0.3):
        n = int(np.floor(self.riskFactors.shape[1]*weights))
        lowIndex = pd.DataFrame()
        highIndex = pd.DataFrame()
        for t in self.date:
            x = riskFactors.loc[t,:]
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
        
        self.T = self.lowIndex.shape[0]
        self.date = self.lowIndex.index.values.tolist()
        
            
        
#    def get_IC(self):
#        self.n = self.IC.shape[1]/2
#        self.lowIC = self.IC.iloc[:,2(self.n-1)]
#        self.highIC = self.IC.iloc[:,2(self.n-1)+1]
        
        
        
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
    
    def get_total_IC(self,given = None):
        self.get_partitionIndex()
        
        if given != None:
            ics = given.loc[self.date]
            n = int(ics.shape[1]/2)
            lowIC = ics.iloc[:,range(0,2*n,2)]
            highIC = ics.iloc[:,range(1,2*n,2)]
            highIC.columns = lowIC.columns.values
        else:
            highIC = pd.DataFrame()
            lowIC = pd.DataFrame()
            for key in self.alphas:
                highIC[key] = self.get_highIC(key)
                lowIC[key] = self.get_lowIC(key)
        self.highIC = highIC
        self.lowIC = lowIC
    
    
    def ide_alpha(self):
        self.get_total_IC()
        #check if the alpha factor is statistically significant
        highMean = self.highIC.mean()
        lowMean = self.lowIC.mean()
        highVol = self.highIC.std()
        lowVol = self.lowIC.std()
        #two sample t-test
        F = highVol / lowVol
        df1 = self.T - 1
        df2 = self.T - 1
        p_f = stats.f.sf(F, df1, df2)
        t,p_t = stats.ttest_ind(self.highIC,self.lowIC,equal_var = [p_f > 0.05],nan_policy = 'omit')
        self.alphaIndex = np.where(p_t<self.signiLevel)
        #f test for variance
        try:
            self.surAlpha = self.alphas[self.alphaIndex[0]]      #list
            self.nAlpha = len(self.alphaIndex[0])
            print('Effective alphas are', self.surAlpha)
        except TypeError:
            print('No alpha found!')
            pass

    
#def get_cleanData():
#    #delete if any massive consecutive missing
#    #average for the closest two for single missing 
#    #bootstraping if serveral missing values
#
#    print('undefned')
#    
if __name__=='main':

    
#    pool = pd.read_csv('pools.csv',index_col = False).Pool    
# 
#    stocks1 = pd.read_csv(r'C:\Users\mdejg\Documents\GitHub\Contextual_Alpha\mat_data\S&P500_clsprc.csv',index_col=0)
#    stocks = stocks1[pool].loc[dates]
#    rets = np.log(stocks/stocks.shift(1)).dropna(how='all')
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
#    Factors['beta'] = pd.read_csv(r'C:\Users\mdejg\Documents\GitHub\Contextual_Alpha\mat_data\S&P500_BETA_ADJ_OVERRIDABLE.csv',index_col = 0).loc[dates,pool]
#    Factors['size'] = pd.read_csv(r'C:\Users\mdejg\Documents\GitHub\Contextual_Alpha\mat_data\S&P500_CUR_MKT_CAP.csv',index_col = 0).loc[dates,pool]
#
#     
#    a = pd.read_csv('Context_factor_Alpha_factor_final.csv')
#    riskFactor = {}
#    for key in a.columns.values:
#         riskFactor[key] = a[key].dropna().values
#    del riskFactor['unsys']
    
    aI = {}
     #apply strategy for each risk factor
    for keys,values in riskFactor.items():
         print(keys)
         riskFactors = Factors[keys]
         alphaFactors = {key: value for key, value in Factors.items() if key in values}
         obj = constr_port(rets,riskFactors,alphaFactors)
         obj.ide_alpha()
         alphaIndex = obj.alphaIndex
         aI[keys] = alphaIndex
         
         
         
         

     
    
