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

    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols_list, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    # Normlized data
    na_price = d_data['close'].values
    normalized_price = na_price / na_price[0, :]

    # calculate daily return
    na_rets = normalized_price.copy()
    tsu.returnize0(na_rets)

    total_daily_ret = 0
    for i in range(len(na_rets[0,:])):
        total_daily_ret += na_rets[:, i] * allocation_list[i]

    # calculate standard deviation
    vol = np.std(total_daily_ret)

    # calcilate mean of daily return
    mean = np.mean(total_daily_ret)

    # sharpe retio
    sharpe = np.sqrt(len(total_daily_ret))*mean/vol
    #sharpe = np.sqrt(252)*mean/vol

    # cumulative return
    def cumret(t, lf_returns):
        """

        :rtype: object
        """
        if t == 0:
            return (1 + lf_returns[0])

        return (cumret(t-1, lf_returns) * (1 + lf_returns[t]))

    cum_ret = cumret(total_daily_ret.size - 1, total_daily_ret)

    print 'Start date: ', start_date
    print 'End dare: ', end_date
    print 'Symbols: ', symbols_list
    print 'Optimal allocation: ', allocation_list
    print 'Sharpe Ratio: ', sharpe
    print 'Volatility (stdev of daily returns): ', vol
    print 'Average Daily Return: ', mean
    print 'Cumulative Return: ', cum_ret

    return vol, total_daily_ret, sharpe, cum_ret


if __name__ == "__main__":
    # Test function
    # inputs:
    '''
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    symbols_list = ['AXP', 'HPQ', 'IBM', 'HNZ']
    allocation_list = [0.0, 0.0, 0.0, 1.0]
    '''
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    symbols_list = ['AAPL', 'GLD', 'GOOG', 'XOM']
    allocation_list = [0.4, 0.4, 0.0, 0.2]

    vol, daily_ret, sharpe, cum_ret = simulate(start_date, end_date,
                                               symbols_list, allocation_list)