from cln_ult import mat_paths
import numpy as np
import pandas as pd

start_date = pd.to_datetime('1990/01/01')
end_date = pd.to_datetime('2019/03/25')

for mat_path in mat_paths:
    # mat_path = mat_paths[0] # del
    file_name = mat_path.split('/')[-1]
    raw_df = pd.read_csv(mat_path)
    date = pd.to_datetime(raw_df['Date']) 
    df = raw_df[(date >= start_date) & (date <= end_date)]
    df.to_csv(file_name, index=False)

