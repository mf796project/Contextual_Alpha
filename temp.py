import pandas as pd

def find_weights(cont):
    ''' 
        A function with input: 
            cont (context data),
        output:
            equal Weights time series as a dataframe
    '''
    return cont / cont.sum(axis=1)

