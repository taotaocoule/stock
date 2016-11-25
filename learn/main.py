import get_clean as gc
import get_code as gd
import test as test
import numpy as np
import pandas as pd

good=[]

total=0
can_try=0
test_try=0
diff_list=[]

def cal(code):
	try:
		a=gc.getData(code)
	except:
		print('{} is wrong'.format(code))	
	else:	
		print('{} is running'.format(code))
		if a is not None and len(a)>60:
			global total
			total=total+1
			a.sort_index(inplace=True)
			gc.ma(a,'close',[5,10,15,20,25])
			MA_column=a.columns[-5:]
			a['Diff']= 100 * ((a[MA_column].max(axis=1) - a[MA_column].min(axis=1))/a[MA_column].max(axis=1))
			b=a[-65:-5]['Diff'].mean()
			if b<2 and a[-65:-5]['Diff'].max()<10:
				good.append(code)
				global can_try
				can_try=can_try+1
				# print('{},{}'.format(a[-2:-1].index.values[0],a[-1:].index.values[0]))
				diff=test.test(code,a[-6:-5].index.values[0],a[-1:].index.values[0])
				diff_list.append(diff)
				if diff>0:
					global test_try
					test_try=test_try+1	


def get_low(code):
	try:
		a=gc.getData(code)
	except:
		print('{} is wrong'.format(code))	
	else:	
		print('{} is running'.format(code))
		if a is not None:
			a.sort_index(inplace=True)
			gc.ma(a,'close',[15,30,60,90,120])
			MA_column=a.columns[-5:]
			a['Diff']=100 * ((a[MA_column].max(axis=1) - a[MA_column].min(axis=1))/a[MA_column].max(axis=1))
			a['Min']= a[MA_column].min(axis=1)
			b=a[-2:-1]
			if b['Min'].values[0] == b['MA_15'].values[0] and b['Diff'].values[0] > 40:
				good.append(code)

def clean_data(code):
	i=30
	j=0
	a=gc.cleanData(code)
	if a is not None:
		while i<len(a):
			if (a.iloc[i+7:i+8]['close'].get_values()-a.iloc[i:i+1]['close'].get_values())/a.iloc[i:i+1]['close'].get_values() >0.2:
				print('code : {} times : {}'.format(code,j))
				datas=a.iloc[i:i+1]
				datas['code']=code
				datas['target']=1
				datas.to_csv('data.csv',mode='a',header=False)
				i=i+8
				j=j+1
				good=datas.columns
			else:
				if np.random.random()>0.3:
					datas=a.iloc[i:i+1]
					datas['code']=code
					datas['target']=0
					print(datas.shape)
					print(datas.columns)
					datas.to_csv('data.csv',mode='a',header=False)
				i=i+1				

good=[]

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

def kdj_k_min_10(code):
	a=gc.cleanData(code)
	if a is not None:
		if a.ix[-1:].kdj_k.get_values()<10:
			good.append(code)


def calculateLocation(now,max,min):
	mean=(max+min)/2
	return np.sign(now-mean)*(np.sqrt((now-mean)**2)/mean)+1

needCol=['MA_15','MA_30', 'MA_60', 'MA_90', 'MA_120']
def fiveLine(code):
	try:
		a=gc.getData(code)
	except:
		print('{} is wrong'.format(code))	
	else:	
		print('{} is running'.format(code))
		if a is not None:
			a.sort_index(inplace=True)
			gc.ma(a,'close',[15,30,60,90,120])
			return a

def calculateFive(a,needCol):
	std=a[needCol].std(axis=1).get_values()
	max=a[needCol].max(axis=1).get_values()
	min=a[needCol].min(axis=1).get_values()
	val_15=a.MA_15.get_values()
	val_now=a.close.get_values()
	loc_15=calculateLocation(a.MA_15,max,min).get_values()
	loc_now=calculateLocation(a.close,a.MA_15,a.MA_15).get_values()
	print('{} , {} , {} , {}'.format(val_15,val_now,loc_now,std))
	if std<0.3 and val_15<max:
		if loc_now>1.02 and val_now<max:
			return True			

code=gd.get_all_code()

def useFive(code):
	try:
		a=fiveLine(code)
	else:	
		global can_try
		global test_try
		if len(a)>30:
			for i in range(30,a.shape[0]):
				if calculateFive(a.iloc[i:i+1],needCol):
					can_try+=1
					if a.iloc[i+5:i+6]['close'].get_values()>a.iloc[i:i+1]['close'].get_values():
						test_try+=1
						good.append((a.iloc[i+5:i+6]['close'].get_values()-a.iloc[i:i+1]['close'].get_values())/a.iloc[i:i+1]['close'].get_values())


# for j in code:
# 	kdj_k_min_10(j)

for j in code:
	useFive(j)
print(can_try)
print(test_try)

print(good)
print(np.mean(good))
# print('total:{},try:{},good:{}'.format(total,can_try,test_try))	

# if test_try/can_try>0.5:
# 	x=np.array(diff_list)
# 	print('this strage max:{},min:{},mean:{},std:{}'.format(x.max(),x.min(),x.mean(),x.std()))

# print(good)
# 	get_low(code)

# print(good)	

# good=['600234', '600959', '601016', '601021', '603019', '603021', '603028', '603029', '603085', '603117', '603131', '603169', '603223', '603315', '603318', '603338', '603528', '603588', '603598', '603601', '603663', '603678', '603686', '603703', '603779', '603818', '603869', '603959', '000897', '002143', '002195', '002240', '002354', '002520', '002577', '002602', '002681', '002739', '002743', '002746', '002747', '002751', '002752', '002771', '002773', '002777', '002780', '002785', '002796', '002798', '002799', '002800', '002801', '002803', '002805', '002806']

# j=0

# for i in good:
# 	diff=test.test(i,'2016-09-19','2016-09-20')
# 	if diff>0:
# 		j=j+1

# print('total:{},good:{}'.format(len(good),j))		