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

def custom(data,name):
	plt.hist(data,bins=100,range=(data.quantile(q=0.05),data.quantile(q=0.95)))
	plt.savefig(name)
	plt.close()		

def diff(good,bad,name):
	plt.subplot(1,2,1)
	data=good
	plt.hist(data,bins=100,range=(data.quantile(q=0.05),data.quantile(q=0.95)))	
	data=bad
	plt.subplot(1,2,2)
	plt.hist(data,bins=100,range=(data.quantile(q=0.05),data.quantile(q=0.95)))
	plt.savefig(name)
	plt.close()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import get_clean as gc

a=gc.cleanData('600000')
col=np.append(a.columns,['code','target'])

def new_clean_data():
	data=pd.read_csv(r'data.csv',names=col)	
	return data

train=new_clean_data()
clean=train.copy()
clean.replace([np.inf, -np.inf], np.nan,inplace=True)
needClean=[]
for i in col:
    if np.sum(train[i].isnull())>0:
        needClean.append(i)

needClean=needClean[4:]
clean.rsv.fillna(clean.rsv.mean(),inplace=True)
clean.kdj_k.fillna(clean.kdj_k.mean(),inplace=True)
clean.kdj_d.fillna(clean.kdj_d.mean(),inplace=True)
clean.kdj_j.fillna(clean.kdj_j.mean(),inplace=True)
import re
def clean_nan_col(a):
    b=re.match(r'(.*)\D+',a)
    try:
        b.group()
    except:    
        print('{} is needless'.format(a))
    else:    
        return b.group()[:-1]


clean['MA']=clean.close
clean['Vol']=clean.volume
clean['Day_diff']=0
for i in needClean:
    clean[i].fillna(clean[clean_nan_col(i)],inplace=True)

del clean['MA']
del clean['Vol']
del clean['Day_diff']
	
def location(now,max,min):
	mean=(max+min)/2
	return np.sign(now-mean)*(np.sqrt((now-mean)**2)/mean)+1

needClean=[]
for i in col:
    if i.startswith('MA_'):
        needClean.append(i)

clean['MA_max']=clean[needClean].idxmax(axis=1)
clean['MA_min']=clean[needClean].idxmin(axis=1)
clean['MA_std']=clean[needClean].std(axis=1)
clean['tmp_ma_min']=clean[needClean].min(axis=1)
clean['tmp_ma_max']=clean[needClean].max(axis=1)
clean['MA_range']=clean.tmp_ma_max-clean.tmp_ma_min
clean.MA_range=100*clean.MA_range.div(clean.tmp_ma_min)

clean['MA_loc']=clean.apply(lambda row:location(row['close'],row['tmp_ma_max'],row['tmp_ma_min']),axis=1)
clean['MA_loc']=100*clean['MA_loc']     

del clean['tmp_ma_min']
del clean['tmp_ma_max']   

needClean=[]    

for i in col:
    if i.startswith('Vol_'):
        needClean.append(i)

clean['Vol_max']=clean[needClean].idxmax(axis=1)
clean['Vol_min']=clean[needClean].idxmin(axis=1)
clean['Vol_std']=clean[needClean].std(axis=1)
clean['tmp_ma_min']=clean[needClean].min(axis=1)
clean['tmp_ma_max']=clean[needClean].max(axis=1)
clean['Vol_range']=clean.tmp_ma_max-clean.tmp_ma_min
clean['Vol_range']=100*clean['Vol_range'].div(clean.tmp_ma_min)

clean['Vol_loc']=clean.apply(lambda row:location(row['volume'],row['tmp_ma_max'],row['tmp_ma_min']),axis=1)
clean['Vol_loc']=100*clean['Vol_loc']     

del clean['tmp_ma_min']
del clean['tmp_ma_max']  

needClean=[]
for i in col:
    if i.startswith('Day_diff_'):
        needClean.append(i)  

for i in needClean:
    del clean[i]           