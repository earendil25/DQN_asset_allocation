import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import quandl

quandl.ApiConfig.api_key = "59sg9vqYvngzUw5Xizvi"

class UniverseData():
    def __init__(self, sdate, edate):
        self.data_list = []

        self.sdate = sdate
        self.edate = edate
        self.var = sdate
        
        self.data_df = None
        
    def update_yfinance(self, data_list):        
        self.data_list += data_list
        for ticker in data_list:
            ticker_df = yf.Ticker(ticker).history(
            	start = self.sdate, end = self.edate).Close.to_frame().rename(\
                columns = {'Close':ticker})
            self.data_df = pd.concat([self.data_df, ticker_df],axis = 1)
            
    def update_quandl(self, data_list):
        self.data_list += data_list

        for ticker in data_list:
            ticker_df =  quandl.get(ticker, 
            	start_date = self.sdate, end_date = self.edate).rename(\
                columns = {'Value':ticker})
            self.data_df = pd.concat([self.data_df, ticker_df], axis = 1)


class BackTestModule():
    def __init__(self, UniverseData):
        self.UniverseData = UniverseData


    def _run_backtest(self, target_df, sdate, edate, rebal_period):

        wgt_df = target_df.apply(lambda x : 0.*x + 1./len(target_df.columns))

        date_list = list(target_df.index)

        while True:
            if sdate in date_list:
                sdate_idx = date_list.index(sdate) 
                break
            else: 
                sdate += dt.timedelta(days = 1)

        while True:
            if edate in date_list:
                edate_idx = date_list.index(edate)
                break
            else:
                edate -= dt.timedelta(days = 1)

        print(sdate, edate)

        date_list = date_list[sdate_idx : edate_idx]

        wgt_df = wgt_df.loc[date_list]

        ########## First date #############

        date = date_list[0]

        asset = 1
        asset_list = [asset]
        wgt_df.loc[date] = target_df.loc[date]     

        ########## Start backtest #############   

        for date in date_list[1:]:

            asset *= self.get_return(wgt_df, date) 

            wgt_df.loc[date] = self.get_reweight(wgt_df, date)

            if date_list.index(date) % rebal_period == 0:
                wgt_df.loc[date] = target_df.loc[date]

            wgt_df.loc[date] /= np.sum(wgt_df.loc[date])

            try : 
                assert abs(np.sum(wgt_df.loc[date])-1) < 10**(-3)
            except : 
                print('weight error : ', np.sum(wgt_df.loc[date], date))
                break

            asset_list.append(asset)

        ###################################

        asset_df = pd.DataFrame({'asset':asset_list}, index = date_list)

        return asset_df, wgt_df

    def run_backtest(self, target_df, sdate, edate, rebal_period,
                    sub_portfolio):

        sdate = dt.datetime.strptime(sdate, '%Y-%m-%d')
        edate = dt.datetime.strptime(edate, '%Y-%m-%d')

        sdate_list = [sdate - dt.timedelta(days=int(idx*rebal_period/sub_portfolio)) 
                        for idx in range(sub_portfolio)]

        for sdate in sdate_list:
            asset_df, wgt_df = self._run_backtest(target_df, sdate, edate, rebal_period)

            if sdate == sdate_list[0]:
                total_asset_df = asset_df
                total_wgt_df = wgt_df.multiply(asset_df.squeeze(), axis = 0)

            else:
                total_asset_df += asset_df
                total_wgt_df += wgt_df.multiply(asset_df.squeeze(), axis = 0)
        
        total_wgt_df = total_wgt_df.divide(total_asset_df.squeeze(), axis = 0).dropna()

        total_asset_df = total_asset_df.dropna()/total_asset_df.dropna().iloc[0]

        return total_asset_df, total_wgt_df


    def get_return(self, wgt_df, date):

        tickers = list(wgt_df.columns)

        tickers_df = self.UniverseData.data_df[tickers].fillna(method='ffill')

        ret = tickers_df.loc[date] / tickers_df.shift()[tickers].loc[date]

        ret = np.sum(wgt_df.shift().loc[date] * ret)

        return ret

    def get_reweight(self, wgt_df, date):

        tickers = list(wgt_df.columns)

        tickers_df = self.UniverseData.data_df[tickers].fillna(method='ffill')

        ret = tickers_df.loc[date] / tickers_df.shift()[tickers].loc[date]

        new_wgt = wgt_df.shift().loc[date] * ret
        new_wgt /= np.sum(new_wgt)

        return new_wgt






        
        




