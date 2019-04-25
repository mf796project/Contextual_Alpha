from ult_data import res_path, get_matdata
import numpy as np
import pandas as pd

price = get_matdata("clsprc")
price_m = price.asfreq('M',method="ffill")

spy = get_matdata("index")
spy = spy.asfreq("M",method="ffill")

constit = get_matdata("constituents") 
constit = constit.asfreq("M",method="ffill")

#TODO: integrity check: time that both constituent data and price data exist
# times=price_m.index & constit.index  
# times=times&spy.index
# price_m=price_m.loc[times]
# spy=spy.loc[times]
# constit=constit.loc[times]

#TODO: integrity check: stock names that both price data and constituent data exist
# tot_names=price_m.columns & constit.columns
# price_m=price_m[tot_names]                         
# constit=constit[tot_names]                        

rets = np.log(price_m / price_m.shift(1))
rets = rets.iloc[1:,] 

mret = np.log(spy / spy.shift(1))
mret = mret.iloc[1:,]

excess = rets.sub(pd.Series(mret.iloc[:,0],index=mret.index),axis="index")
excess.to_csv("S&P500_exret.csv")
#excess return
