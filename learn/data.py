import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

headers=['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change', 'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'turnover','MA_15','MA_30','MA_60','MA_90','MA_120','code', 'times']
train=pd.read_csv(r'data.csv',names=headers)
train['group']=train.apply(lambda row:str(row['code'])+'_'+str(row['times']),axis=1)
needDelete=['open', 'high', 'low', 'ma5', 'ma20', 'v_ma5', 'v_ma20']
train.drop(needDelete,axis=1,inplace=True)

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