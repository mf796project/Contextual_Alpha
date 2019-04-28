def to_weights(matdata, threhold=0.1):
    '''transform matdata to two context by threhold'''

    q_head = matdata.quantile(threhold, axis=1)
    q_tail = matdata.quantile(1-threhold, axis=1)
    
    # left close & right open
    df_head = matdata.apply(lambda x: x <= q_head)
    df_tail = matdata.apply(lambda x: x >= q_tail)
    
    return (df_head, df_tail)


def find_weights(factor, ret, cont_list, limit=4):
    ''' 
        A function with input: 
            ret (returns of constituents), 
            factor (factor data), 
            context_list (context data),
            limit (lowese number of tickers to compute IC)
        output:
            factor IC time series as a dataframe
    '''
    times = factor.index & ret.index
    for cont in cont_list:
        times = times & cont.index

    IC = []
    for i in range(len(times)-1):
        # only use tickers in context
        for j in range(len(cont_list)):
            cont = cont_list[j]
            if j == 0:
                online = cont.loc[times[i+1],][cont.loc[times[i+1],]!=0]
            else:
                online = online & \
                    cont.loc[times[i+1],][cont.loc[times[i+1],]!=0]
        
        # only use tickers with available return data
        rts = ret.loc[times[i+1],].dropna()
        
        # only use tickers with available factor data
        facs = factor.loc[times[i],].dropna()

        names = online.index & rts.index & facs.index
            
        if len(names) <= limit:
            IC.append(None)   
        else:
            rts=rts[names]
            facs=facs[names]
            IC.append(np.corrcoef(list(rts),list(facs))[0,1])
    
    ICdf = pd.DataFrame(data=IC,index=times[1:],columns=['factor'])

    return ICdf
