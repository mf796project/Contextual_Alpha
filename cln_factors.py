from ult_data import factor_paths
import numpy as np
import pandas as pd
import json

naming_dict = {} # map name to meaning
for factor_path in factor_paths:
    raw_df = pd.read_csv(factor_path)

    file_name = raw_df.iloc[4,1]
    file_mean = raw_df.iloc[3,1]
    naming_dict[file_name] = file_mean 

    # columns
    ticker_list = [i.split(' ')[0] for i in raw_df.iloc[2,1:].values]
    # index
    date = pd.to_datetime(raw_df.iloc[5:,0].values)
    # cleaned dataframe
    df = pd.DataFrame(
        data=raw_df.iloc[5:,1:].values, 
        index=date, 
        columns=ticker_list)
    df = df[~pd.isnull(df.index)]
    df = df.loc[:,~df.columns.duplicated()]
    df = df.reset_index().rename(columns={'index':'Date'})
    df.to_csv('_'.join(['S&P500', file_name+'.csv']), index=False)

# write naming_dict to json
# with open('naming_dict.json', 'w') as f:
#     json.dump(naming_dict, f)

