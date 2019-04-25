from ult_cln import matdata_paths
import numpy as np
import pandas as pd

for matdata_path in matdata_paths:

    df = pd.read_csv(matdata_path)

    df.iloc[0,:] = df.iloc[0,:].apply(lambda x: x if x != '#N/A Invalid Security' else np.nan)
    df.to_csv(matdata_path, index=False)