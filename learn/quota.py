import numpy as np
import pandas as pd
import tushare as ts

import urllib.request as request
from bs4 import BeautifulSoup
import re 

col=['mean15','mean30', 'mean60', 'mean90']
cols=['code', 'boll_diff', 'volDiff', 'volBreak', 'boll_gradient', 'bollBreak', 'lineBreak', 'mean15_gradient', 'mean30_gradient', 'gradientBreak', 'rate60', 'rate90', 'lineDiff', 'dea', 'dea_gradient', 'change', 'type']

def get_all_code():
	url=r'http://quote.eastmoney.com/stocklist.html' 
	get=request.urlopen(url).read()
	soup=BeautifulSoup(get)
	li=[]
	for link in soup.find("div",{"class":"qox"}).find_all("a")[3:]:
		if len(link):
			a=re.compile('(\d{6})').findall(link.contents[0])[0]
			if a[0]=="0" or a[0]=="6":
				li.append(a)
	return li		

def meanLine(data,time=[15,30,60,90,120]):
	tmp={}
	for i in time:
		tmp['mean'+str(i)]=data.rolling(i).mean()
	return tmp	

def boll(data,time=20):
	ma20=data.rolling(time).mean()
	std20=data.rolling(time).std()
	up20=ma20+2*std20.shift(1)
	down20=ma20-2*std20.shift(1)
	diff20=up20-down20
	return diff20

def cleanData(code):
	a=ts.get_k_data(code)
	meanLineTmp=meanLine(a.close)
	for i in [15,30,60,90,120]:
		s='mean'+str(i)
		a[s]=meanLineTmp[s]	
	volLineTmp=meanLine(a.volume,time=[5,10])
	a['vol5'],a['vol10']=volLineTmp['mean5'],volLineTmp['mean10']
	a['boll_diff']=boll(a.close)
	return a

def strategy_boll(a,volBreakCase=1.3,bollBreakCase=3):
	# volume break
	x=a.vol5>a.vol10
	y=a.vol5.shift(1)<a.vol10.shift(1)
	z=(a.volume/a.vol5)>volBreakCase
	a['volDiff']=(a.volume-a.vol5)/a.vol5
	a['volBreak']=x&y&z
	# boll break
	q=a.boll_diff.rolling(40).max()
	a['boll_gradient']=np.gradient(a.boll_diff)
	a['bollBreak']=(q/a.boll_diff)>bollBreakCase
	# line break
	x=a.mean15>a.mean30
	y=a.mean15.shift(1)<a.mean30.shift(1)
	a['lineBreak']= x & y
	# gradient >0
	a['mean15_gradient']=np.gradient(a.mean15)
	a['mean30_gradient']=np.gradient(a.mean30)
	a['gradientBreak']=(a['mean15_gradient']>0) & (a['mean30_gradient']>0) & (a['mean15_gradient'].shift(1)<0) & (a['mean30_gradient'].shift(1)<0)
	a['isOK']=a.volBreak & a.gradientBreak & a.bollBreak & a.lineBreak
	return a

def strategy_five(a):
	x_60=a.mean60.shift(30)
	x_90=a.mean90.shift(30)
	a['rate60']=(a.mean60-x_60)/x_60
	a['rate90']=(a.mean90-x_90)/x_90
	b=a[col]
	a['lineDiff']=(b.max(axis=1)-b.min(axis=1))/b.min(axis=1)
	return a

def strategy_md(a):
	quick=a.close.rolling(12).mean()
	slow=a.close.rolling(26).mean()
	QUICK=quick.shift(1)*11/13+a.close*2/13
	SLOW=slow.shift(1)*25/27+a.close*2/27
	DIF=QUICK-SLOW
	dea=DIF.rolling(9).mean()
	a['dea']=dea.shift(1)*8/10+DIF*2/10
	a['dea_gradient']=(a.dea-a.dea.shift(15))/a.dea.shift(15)
	return a

code=get_all_code()

def getData(code):
	a=cleanData(code)
	if a is not None and len(a)>60:
		a=strategy_boll(a)
		a=strategy_five(a)
		a=strategy_md(a)
		a['after']=a.close.shift(-10)
		a['change']=a.apply(lambda row:100*(row.after-row.close)/row.close,axis=1)
		a['type']=a.change.apply(getType)
		return a

def getType(x):
	if x>30:
		t=3
	elif x>10:
		t=2
	elif x>0:
		t=1
	else:
		t=0			
	return t

def getToday():
	for i in code:
		a=getData(i)
		if a is not None and len(a)>60:
			print(i)
			cols=['code', 'boll_diff', 'volDiff', 'volBreak', 'boll_gradient', 'bollBreak', 'lineBreak', 'mean15_gradient', 'mean30_gradient', 'gradientBreak', 'rate60', 'rate90', 'lineDiff', 'dea', 'dea_gradient', 'change', 'type']
			a=a[cols]
			a.tail(1).to_csv('today.csv',mode='a',header=False)

def get_boll():
	can_try_code=[]
	for j in code:
		try:
			a=cleanData(j)
		except:
			print('{} is wrong'.format(j))
		else:
			if a is not None and len(a)>60:	
				print('{} is running'.format(j))	
				m=strategy_boll(a)
				if m.isOK[-1:].values[0]:
					can_try_code.append(j)
	return can_try_code				


can_try=0
try_test=0
all_rate=[]
good_rate=[]
for j in code:
	try:
		a=cleanData(j)
	except:
		print('{} is wrong'.format(j))
	else:
		if a is not None and len(a)>60:	
			print('{} is running'.format(j))	
			m=strategy_boll(a)
			ok_index=m[m.isOK].index
			for q in ok_index:
				q=int(q)
				p=q+20
				if p<len(a):
					can_try=can_try+1
					thisRate=(m.loc[p].close-m.loc[q].close)/m.loc[q].close
					all_rate.append(thisRate)
					if thisRate>0:
						try_test=try_test+1
						good_rate.append(thisRate)