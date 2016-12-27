import numpy as np
import pandas as pd
import tushare as ts

import sklearn
import sklearn.preprocessing

close_range=sklearn.preprocessing.MinMaxScaler(feature_range=(-100,100))

def getData(code):
    try:
        a=ts.get_hist_data(code)
    except:
        print('wrong')
    else:
        if a is not None:
            if len(a)>120:
                a['code']=str(code)
                a.sort_index(inplace=True)
                a['close_range']=close_range.fit_transform(a.close.reshape(-1, 1))
                a['volume_range']=close_range.fit_transform(a.volume.reshape(-1, 1))
                return a

def ma(data,l=[15,30,60,90,120],t=['close','close_range','volume','volume_range']):
    for i in l:
        for j in t:
            data[j+str(i)]=pd.rolling_mean(data[j],i)
            data[j+'_std'+str(i)]=pd.rolling_mean(data[j],i)      

def isOK(data,l=[5,10,15,30],t=0.1):
    for i in l:
        change=data.close.pct_change(periods=i)
        data['isOK_'+str(i)]=change>t
        data['change_'+str(i)]=change

def boll(a):
    a['std20']=pd.rolling_std(a.ma20,20)
    a['boll_up']=a.close+2*a.std20
    a['boll_down']=a.close-2*a.std20
    a['boll_range']=(pd.rolling_max(a.boll_up,20)-pd.rolling_min(a.boll_down,20))/pd.rolling_mean(a.ma20,20)
    a['boll_range_p']=a.boll_range.pct_change()
    a['boll_change']=a.boll_up-a.boll_down
    a['boll_range_p20']=a.boll_range.pct_change(periods=20)    
    a['macd']=pd.ewma(a.close,12)-pd.ewma(a.close,26)

def rsi(a,date=14):
    c=pd.rolling_apply(a.price_change,date,lambda x:np.sum(x[x>0]))/date
    d=(-pd.rolling_apply(a.price_change,date,lambda x:np.sum(x[x<0])))/date
    rs=c/d
    rsi=100*(rs/(1+rs))
    return rsi

def gradient(a,l=[5,10,15,30]):
    for i in l:
        tmp=a.close.shift(i)
        a['close_gradient'+str(i)]=100*(a.close-tmp)/i

def clean(code):
    a=getData(code) 
    if a is not None:           
        if len(a)>10:
            ma(a)
            boll(a)
            isOK(a)
            a['rsi']=rsi(a)
            gradient(a)
            a.dropna(inplace=True)
            a.to_csv('data.csv',mode='a',header=False)
            return a

import get_code as gd
code=gd.get_all_code()
for i in code:
    clean(i)