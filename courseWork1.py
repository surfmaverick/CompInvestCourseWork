import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def simulate(start_date, end_date, symbols_list, allocation_list):
    '''
    Calculate the metrics of a portfolio duting given time period.
    The intent is for you to learn how to assess a portfolio.

    :param start_date: datetime object
    :param end_date: datetime object
    :param symbols_list: list of strings
    :param allocation_list: list of float
    :return: vol, daily_ret, sharpe, cum_ret (all float type)
    '''
    # retrive data
    day_time = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(start_date, end_date, day_time)

    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols_list, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    # Normlized data
    na_price = d_data['close'].values
    normalized_price = na_price / na_price[0, :]

    # calculate daily return
    na_rets = normalized_price.copy()
    tsu.returnize0(na_rets)
    #total_daily_ret = np.sum(na_rets, axis = 1)
    total_daily_ret = na_rets[:,0]
    
    # calculate standard deviation
    vol = np.std(total_daily_ret)
    print 'standard deviation: ', vol

    # calcilate mean of daily return
    mean = np.mean(total_daily_ret)
    print 'mean: ', mean

    # sharpe retio
    sharpe = np.sqrt(len(total_daily_ret))*mean/vol
    print 'shaepe: ', sharpe

    # cumulative return
    cum_ret = np.sum(total_daily_ret)
    print 'cumulative return: ', cum_ret

    return vol, total_daily_ret, sharpe, cum_ret



if __name__ == "__main__":
    # Test function
    # inputs:
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    symbols_list = ['AAPL', 'GLD', 'GOOG', 'XOM']
    allocation_list = [0.4, 0.4, 0.0, 0.2]

    vol, daily_ret, sharpe, cum_ret = simulate(start_date, end_date,
                                               symbols_list, allocation_list)

