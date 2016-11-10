import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def cleanData():
	headers=['date','close', 'volume', 'turnover', 'day_diff', 'MA_15', 'MA_30', 'MA_60',
       'MA_90', 'MA_120', 'Vol_15', 'Vol_30', 'Vol_60', 'Vol_90', 'Vol_120',
       'Day_diff_15', 'Day_diff_30', 'Day_diff_60', 'Day_diff_90',
       'Day_diff_120', 'turnover_15', 'turnover_30', 'turnover_60',
       'turnover_90', 'turnover_120', 'macd', 'macd_15', 'macd_30', 'macd_60',
       'macd_90', 'macd_120' , 'code' , 'target']
	train=pd.read_csv(r'data.csv',names=headers)
	# train['group']=train.apply(lambda row:str(row['code'])+'_'+str(row['times']),axis=1)
	needDelete=['date','close', 'volume', 'turnover', 'day_diff' , 'code']
	train.drop(needDelete,axis=1,inplace=True)
	train.replace([np.inf, -np.inf], np.nan,inplace=True)
	train.fillna(1,inplace=True)
	return train

def cleanTestData(train):
	needDelete=['close', 'volume', 'turnover', 'day_diff'];
	train.drop(needDelete,axis=1,inplace=True)
	train.replace([np.inf, -np.inf], np.nan,inplace=True)
	train.fillna(1,inplace=True)
	return train

how={'date':['close','volume','ma10','turnover']}

def plot(unique,how,name):
	row=len(how.keys())
	length=len([item for sublist in list(how.values()) for item in sublist])
	column=np.ceil(length/row)
	i=1
	for key in how:
		sub=how[key]
		for j in sub:
			plt.subplot(column,row,i)
			plt.plot(unique[key],unique[j])
			title=str(key)+'--'+str(j)
			plt.title(title)
			i=i+1
		path=r'picture/'+name+'.png'	
		plt.savefig(path)
	plt.close()		