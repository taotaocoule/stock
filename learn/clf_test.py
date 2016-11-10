import numpy as np
import pandas as pd
import tushare as ts
from sklearn.externals import joblib

h="clf = joblib.load('filename.pkl') "

def getData(code):
    a=ts.get_hist_data(code)
    # a.sort_index(inplace=True)
    return a
def cleanData(code,type=[15,30,60,90,120]):
    try:
        a=getData(code)
    except:
        print('{} is wrong'.format(code))   
    else:   
        print('{} is running'.format(code))
        if a is not None:
            a['day_diff']=(a.high-a.low)/a.open
            a.drop(['high','low','open','p_change','price_change','ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20'],axis=1,inplace=True)
            a.sort_index(inplace=True)
            ma(a,'close',type)
            ma(a,'volume',type,'Vol_')
            ma(a,'day_diff',type,'Day_diff_')
            ma(a,'turnover',type,'turnover_')
            a['macd']=pd.ewma(a.close,12)-pd.ewma(a.close,26)
            ma(a,'macd',type,'macd_')
            return a

def ma(data,column,type,name='MA_'):
    for i in type:
        data[name+str(i)]=(pd.rolling_mean(data[column],i))/data[column]

def get(code):
    a=cleanData(code)
    a.drop(['close', 'volume', 'turnover', 'day_diff'],inplace=True,axis=1)
    a.replace([np.inf, -np.inf], np.nan,inplace=True)
    a.fillna(1,inplace=True)
    return a

