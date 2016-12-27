import get_clean as gc
import get_code as gd
import test as test
import numpy as np
import pandas as pd
import tushare as ts

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
	a=fiveLine(code)
	global can_try
	global test_try
	if a is not None and len(a)>30:
		for i in range(len(a)-10,len(a)-5):
			if calculateFive(a.iloc[i:i+1],needCol):
				can_try+=1
				if a.iloc[i+5:i+6]['close'].get_values()>a.iloc[i:i+1]['close'].get_values():
					test_try+=1
					good.append((a.iloc[i+5:i+6]['close'].get_values()-a.iloc[i:i+1]['close'].get_values())/a.iloc[i:i+1]['close'].get_values())

need=[]
report=[]
def getFive(code):
	a=fiveLine(code)
	trys=0
	tests=0
	tmp=[]
	if a is not None and len(a)>30:
		for i in range(30,len(a)):
			if calculateFive(a.iloc[i:i+1],needCol):
				trys+=1
				tmp.append((a.iloc[i+5:i+6]['close'].get_values()-a.iloc[i:i+1]['close'].get_values())/a.iloc[i:i+1]['close'].get_values())
				good.append((a.iloc[i+5:i+6]['close'].get_values()-a.iloc[i:i+1]['close'].get_values())/a.iloc[i:i+1]['close'].get_values())
				if a.iloc[i+5:i+6]['close'].get_values()>a.iloc[i:i+1]['close'].get_values():
					tests+=1		
		if trys==tests and trys>2:
			need.append(code)
			strs='{} is good, rate is : {}, times is {}'.format(code,np.mean(tmp),tests)
			report.append(strs)			

# for j in code:
# 	kdj_k_min_10(j)

# for j in code:
# 	getFive(j)

# for z in report:
# 	print(z)
# print(need)
# print(np.mean(good))

# print('total:{},try:{},good:{}'.format(total,can_try,test_try))	

def five(fiveNeed):
	right=[]
	for i in fiveNeed:
	    a=fiveLine(i)
	    if a is not None and len(a)>30:
	        if calculateFive(a.tail(1),needCol):
	            right.append(i)
	print(right)
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

def boll(code):
	try:
		a=gc.getData(code)
	except:
		print('{} is wrong'.format(code))	
	else:	
	    if a is not None:
		    a.sort_index(inplace=True)
		    a['std20']=pd.rolling_std(a.ma20,20)
		    a['boll_up']=a.close+2*a.std20
		    a['boll_down']=a.close-2*a.std20
		    a['boll_range']=(pd.rolling_max(a.boll_up,20)-pd.rolling_min(a.boll_down,20))/pd.rolling_mean(a.ma20,20)
		    a['boll_range_p']=a.boll_range.pct_change()
		    a['boll_range_p20']=a.boll_range.pct_change(periods=20)
		    return a

def test_boll(data):
    if data.close.get_values()<data.ma20.get_values():
        range_to_down=(data.low.get_values()-data.boll_down.get_values())/data.low.get_values()
        if range_to_down<0.01 and data.boll_range_p20.get_values()<-0.5:
            if data.boll_range.get_values()<0.035:
                return True   
let_try=0
let_test=0                
j=[]
def try_boll(g):
	global let_test
	global let_try
	for i in range(30,len(g)):
	   if test_boll(g.iloc[i:i+1]):
	       let_try=let_try+1
	       result=(g.iloc[i+10:i+11]['close'].get_values()-g.iloc[i:i+1]['close'].get_values())/g.iloc[i:i+1]['close'].get_values()
	       if result>0:
	           let_test=let_test+1
	           j.append(result)   

def rsi(a,date=14):
	c=pd.rolling_apply(a.price_change,date,lambda x:np.sum(x[x>0]))/date
	d=(-pd.rolling_apply(a.price_change,date,lambda x:np.sum(x[x<0])))/date
	rs=c/d
	rsi=100*(rs/(1+rs))
	return rsi

def boll(a):
	a['std20']=pd.rolling_std(a.ma20,20)
	a['boll_up']=a.close+2*a.std20
	a['boll_down']=a.close-2*a.std20
	a['boll_range']=(pd.rolling_max(a.boll_up,20)-pd.rolling_min(a.boll_down,20))/pd.rolling_mean(a.ma20,20)
	a['boll_range_p']=a.boll_range.pct_change()
	a['boll_range_p20']=a.boll_range.pct_change(periods=20)

let_safe=0
def test_rsi(code):
	global let_test
	global let_try
	global let_safe
	try:
		a=gc.getData(code)
	except:
		print('{} is wrong'.format(code))	
	else:	
	    if a is not None:
		    a.sort_index(inplace=True)
		    a['rsi']=rsi(a)
		    a['after_7']=a.shift(-7).close
		    a['is_ok']=	(a.after_7-a.close)/a.after_7>0.1
		    a['is_safe']=a.after_7>a.close
		    tmp=a[a.rsi<20]
		    let_try=let_try+len(tmp)
		    let_test=let_test+np.sum(tmp.is_ok)
		    let_safe=let_safe+np.sum(tmp.is_safe)
		    if len(tmp)==np.sum(tmp.is_ok):
		    	good.append({'name':code,'time':len(tmp)})
		    print(code)


def get_all_data():
	for i in code:
	    try:
	        a=ts.get_hist_data(i)
	    except:    
	        print('{} is wrong'.format(i))
	    else:    
	        if a is not None:
	            a['code']=str(i)
	            a.sort_index(inplace=True)

def category(x):
    if x>3:
        if x>10:
            return 2
        else:
            return 1
    else:    
        return 0

def cal_gradient(a,b,l):
	return (a-b)/(-l)

def storage(code):
	try:
		a=ts.get_hist_data(code)
	except:
		print('{} is wrong'.format(code))
	else:
		if a is not None:
			a['code']=str(code)		        	            
			a.sort_index(inplace=True)
			boll(a)
			a['rsi']=rsi(a)
			kdj(a,9,3,3)
			a['macd']=pd.ewma(a.close,12)-pd.ewma(a.close,26)
			a['ma30']=pd.rolling_mean(a.close,30)
			a['ma60']=pd.rolling_mean(a.close,60)
			a['ma90']=pd.rolling_mean(a.close,90)
			a['change30']=pd.rolling_std(np.gradient(a.ma30),30)
			for t in [5,10,20,30,60,90]:
				a['max'+str(t)]=pd.rolling_max(a.close,t)
				a['min'+str(t)]=pd.rolling_min(a.close,t)
			a['macd_a']=pd.ewma(a.close,12)
			a['macd_d']=pd.ewma(a.close,26)
			a['diff5']=100*(a.shift(-5).close-a.close)/a.close
			a['diff10']=100*(a.shift(-10).close-a.close)/a.close
			a['diff5_c']=a.diff5.apply(category)
			a['diff10_c']=a.diff10.apply(category)
			a.dropna()
			return a

# 过去15天ma15最大率
# a['max']=a[['ma5','ma10','ma20']].idxmax(axis=1)
# def is_this(x,s):
#     return x==s
# pd.rolling_sum(a['max']=='ma5',15)	
# 
# a['ma15_40']=a.ma15.shift(40)
# a['rate15']=a.apply(lambda x:np.gradient([x['ma15_40'],x['ma15']])[0],axis=1)		

mas=['ma15','ma30','ma60','ma90','ma120']
def newFiveLine(code):
	try:
		a=ts.get_hist_data(code)
	except:
		print('{} is wrong'.format(code))
	else:
		if a is not None:
			a.sort_index(inplace=True)
			for i in [15,30,60,90,120]:
				a['ma'+str(i)]=pd.rolling_mean(a.close,i)
				a['ma'+str(i)+'_40']=a['ma'+str(i)].shift(40)
				a['rate'+str(i)]=a.apply(lambda x:np.gradient([x['ma'+str(i)+'_40'],x['ma'+str(i)]])[0],axis=1)	
			a.dropna(inplace=True)
			a['five']=(a[mas].max(axis=1)-a[mas].min(axis=1))/a[mas].max(axis=1)
