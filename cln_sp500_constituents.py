from cln_ult import wrds_sp500_cons_path, sp500_ticker_list_path
import numpy as np
import pandas as pd
import pandas_market_calendars as mcal

start_date = pd.to_datetime('1990/01/01')
end_date = pd.to_datetime('2019/03/25')
# find index: trading dates(freq='M)
nyse = mcal.get_calendar('NYSE')
trading_date_d = nyse.valid_days(start_date=start_date, end_date=end_date)
trading_date_m = trading_date_d[np.append(np.diff(trading_date_d.month)!=0,False)]
trading_date_m = pd.to_datetime(trading_date_m.date)
# find columns: ticker list
with open(sp500_ticker_list_path) as f:
    ticker_list = f.read().splitlines()
ticker_list = list(set(ticker_list))
sp500_cons = pd.DataFrame(index=trading_date_m, columns=ticker_list)

wrds_sp500_cons = pd.read_csv(wrds_sp500_cons_path)
birth_death = wrds_sp500_cons[['co_tic', 'from', 'thru']].fillna(value='2019/03/25')
birth_death = birth_death[pd.to_datetime(birth_death['thru']) >= start_date]
for i in range(len(birth_death)):
    living_period = pd.date_range(birth_death.iloc[i]['from'],birth_death.iloc[i]['thru'])
    ticker = birth_death.iloc[i]['co_tic']
    try:
        sp500_cons[ticker][[i in living_period for i in sp500_cons[ticker].index]] = 1
    except KeyError:
        pass
sp500_cons = sp500_cons.fillna(value=0)
sp500_cons = sp500_cons.reset_index().rename(columns={'index':'Date'})
sp500_cons.to_csv('S&P500_constituents.csv',index=False)

