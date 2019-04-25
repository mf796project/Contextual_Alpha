import os
from ult import rawdata_path, matdata_path
import pandas as pd

# paths
factor_paths = [os.path.join(rawdata_path, i) for i in os.listdir(rawdata_path) if i.endswith('.csv')]
matdata_paths = [os.path.join(matdata_path, i) for i in os.listdir(matdata_path) if i.startswith('S&P500')]