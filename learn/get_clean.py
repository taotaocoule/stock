import pandas as pd
import numpy as np
import tushare as ts

def getData(code):
	a=ts.get_hist_data(code)
	# a.sort_index(inplace=True)
	return a

def ma(data,column,type,name='MA_'):
	for i in type:
		data[name+str(i)]=pd.rolling_mean(data[column],i)
		data[name+'_std_'+str(i)]=pd.rolling_std(data[column],i)

def diff(data,column,type):
	for i in type:
		data['Diff_'+str(i)]=data[column].diff(i)	

def ema(data,column,type):
	for i in type:
		data['EMA_'+str(i)]=pd.ewma(data[column],i)	

def kdj(data,date,m1,m2):
	data_use=data[['high','low','open','close']]
	data['lown'] = pd.rolling_min(data_use['low'], date)
	data.lown.fillna(value=pd.expanding_min(data_use['low']), inplace=True)
	data['highn'] = pd.rolling_max(data_use['high'], date)
	data.highn.fillna(value=pd.expanding_max(data_use['high']), inplace=True)
	data['rsv']=(data['close'] - data['lown']) / (data['highn'] - data['lown']) * 100
	data['kdj_k'] = pd.ewma(data['rsv'], m1)
	data['kdj_d'] = pd.ewma(data['kdj_k'], m2)
	data['kdj_j'] = 3 * data['kdj_k'] - 2 * data['kdj_d']
 
def calculateLocation(now,max,min):
	mean=(max+min)/2
	return np.sign(now-mean)*(np.sqrt((now-mean)**2)/mean)+1 

def moreMean(data,time,col):
	name=str(col)+'_'+str(time)
	data[name]=pd.rolling_mean(data[col],time)

def moreStd(data,time,col):
	name=str(col)+'_'+str(time)
	data[name]=pd.rolling_std(data[col],time)

def cleanData(code,type=[5,10,15,30,60,90,120]):
	try:
		a=getData(code)
	except:
		print('{} is wrong'.format(code))	
	else:	
		print('{} is running'.format(code))
		if a is not None and len(a)>60:
			a['day_diff']=(a.open-a.close)/a.open
			kdj(a,9,3,3)
			a.dropna()
			a['day_range']=a.high-a.low
			ma(a,'day_range',type,'day_range_')
			a['Vol_change']=a.volume.diff()/a.volume
			a['close_location']=calculateLocation(a.close,a.high,a.low)
			ma(a,'close_location',type,'close_location_')
			q=['MA_','close_location_','kdj_k_','Day_diff_','day_range_','turnover_','Vol_change_']
			a.drop(['high','low','open','p_change','price_change','ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20'],axis=1,inplace=True)
			a.sort_index(inplace=True)
			ma(a,'close',type)
			ma(a,'Vol_change',type,'Vol_change_')
			ma(a,'lown',type,'lown_')
			ma(a,'highn',type,'highn_')
			ma(a,'rsv',type,'rsv_')
			ma(a,'kdj_k',type,'kdj_k_')
			ma(a,'kdj_d',type,'kdj_d_')
			ma(a,'kdj_j',type,'kdj_j_')
			ma(a,'volume',type,'Vol_')
			ma(a,'day_diff',type,'Day_diff_')
			ma(a,'turnover',type,'turnover_')
			a['macd']=pd.ewma(a.close,12)-pd.ewma(a.close,26)
			ma(a,'macd',type,'macd_')
			for t in q:
				z=[]
				for j in type:
					z.append(str(t)+str(j))
				a[str(t)+'range']=a[z].max(axis=1)-a[z].min(axis=1)		
			for t in q:
				for j in type:
					co=t+str(j)
					moreMean(a,30,co)
					co2=t+'_std_'+str(j)
					moreMean(a,30,co2)
			return a

a=cleanData('600000')
print(a.columns)
print(a.shape)		
