from ult import matdata_path, get_matdata
import os
import numpy as np
import pandas as pd

price = get_matdata('clsprc', 'M')
spx = get_matdata('index', 'M')
constit = get_matdata('constituents', 'M')                   

rets = np.log(price / price.shift(1))
rets = rets.iloc[1:,] 

mret = np.log(spx / spx.shift(1))
mret = mret.iloc[1:,]

excess = rets.sub(pd.Series(mret.iloc[:,0],index=mret.index),axis="index")
excess.to_csv(os.path.join(matdata_path, "S&P500_exret.csv"))
