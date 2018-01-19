import numpy as np
import pandas as pd
import tushare as ts

datas=ts.get_k_data('600000',start='2015-06-30')
time=[15,30,60,90,120]
j=["MA_"+str(i) for i in time]

def format_data(data):
	for i in time:
		data["MA_"+str(i)]=data["close"].rolling(i).mean()
	for x in j:
		data[x+"_Change"]=1000*(data[x]-data[x].shift(30))/data[x]	
	data["vol_max_22"]=data.volume.rolling(10).max().shift()
	data['vol_multi']=data.volume/data.vol_max_22	
	data['five_change']=1000*(data[j].max(axis=1)-data[j].min(axis=1))/data[j].min(axis=1)
	data['is_vol_right']=data.vol_multi.rolling(22).max().shift()
	data['is_five_change']=data.five_change.rolling(22).min().shift()
	data=data[(data.high>data.MA_15) & (data.low < data.MA_15)]
	data['price']=data.close.shift(-22)
	data['price_change']=1000*(data.price-data.close)/data.close
	data['type']=data.apply(get_type,axis=1)
	return data

def test_strategy(data):
	m=data[data.is_vol_right>5]

def get_type(data):
	if data.price_change<0:
		return 0
	elif data.price_change<100:
		return 1
	elif data.price_change<200:
		return 2
	elif np.isnan(data.price_change):
		return 5	
	else:
		return 3			

for c in code:
    try:
        a=ts.get_k_data(c,start='2015-06-30')
    except:    
        print('{} is wrong'.format(c))
    else:    
        print('{} is running'.format(c))
        if(len(a)>0):
        	format_data(a).to_csv('data.csv',mode='a',index=False)


