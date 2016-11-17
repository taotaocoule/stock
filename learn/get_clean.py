import pandas as pd
import tushare as ts

def getData(code):
	a=ts.get_hist_data(code)
	# a.sort_index(inplace=True)
	return a

def ma(data,column,type,name='MA_'):
	for i in type:
		data[name+str(i)]=pd.rolling_mean(data[column],i)

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
 

def cleanData(code,type=[3,5,10,15,20,30,60,90,120]):
	try:
		a=getData(code)
	except:
		print('{} is wrong'.format(code))	
	else:	
		print('{} is running'.format(code))
		if a is not None:
			a['day_diff']=(a.high-a.low)/a.open
			kdj(a,9,3,3)
			a.drop(['high','low','open','p_change','price_change','ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20'],axis=1,inplace=True)
			a.sort_index(inplace=True)
			ma(a,'close',type)
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
			return a

a=cleanData('600000')
print(a.columns)
print(a.shape)		
