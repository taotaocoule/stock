import get_clean as gc
import get_code as gd
import test as test
import numpy as np

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
					datas.to_csv('data.csv',mode='a',header=False)
				i=i+1				

code=gd.get_all_code()

for code in code:
	clean_data(code)

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