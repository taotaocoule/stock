# 获取统一的股票数据格式
# 传入的data为pandas格式，tushare获取
import pandas as pd

# 过去一段时间的极差（用来知道当前是暴涨后还是暴跌后）
# 过去一段时间的方差（用来知道过去一段时间的波动性）
# 过去一段时间的开口（均线开口情况）
class Stock(object):
	"""docstring for Stock"""
	def __init__(self, data):
		self.data = data

	def clean(self):
		cleaned = self.data
		cleaned = get_type(cleaned)
		return cleaned

# 找极值
# 1.选定阈值【变动>20，距离>10】
# 2.选择前10个数据，求最大值和最小值，记录极差1
# 3.从最小值开始索引到第11个位置，求最大值和最小值，记录极差2，
# 如果极差2>极差1，开始索引第12个位置，重复
# 如果极差2<极差1，继续向后索引5个位置，如果5个位置中没有极差2>极差1的，结束
# 4.如果极差>20且距离>10，记录位置，最小值和最大值索引，分别标记为BS，
# 然后从最后一个位置开始重复
import numpy as np

def calculate_change_distance(data,start=0,end=10):
	a=data[start:end]
	max=np.max(a)
	argmax=start+np.argmax(a)
	min=np.min(a)
	argmin=start+np.argmin(a)
	change=(max-min)/min
	return {
		"max":max,
		"min":min,
		"argmax":argmax,
		"argmin":argmin,
		"change":change
	}


def calculate_next(data,start,end):
	first=calculate_change_distance(data,start,end)
	calculate_list=[]
	start=first["argmin"]
	for i in range(1,6):
		end=end+i
		second=calculate_change_distance(data,start,end)
		calculate_list.append(second["change"])
	if np.max(calculate_list)>first["change"]:
		max_index=start+np.argmax(calculate_list)+1
		change=np.max(calculate_list)
		return {
			"argmax":end,
			"argmin":start,
			"change":change,
			"continue":True
		}
	else:
		return {
			"argmax":first["argmax"],
			"argmin":start,
			"change":first["change"],
			"continue":False
		}

def get_type(data):
	start=0
	end=10
	good_list=[]
	while end<len(data):
		a=calculate_next(data.close.values,start,end)
		if a["continue"]:
			start=a["argmin"]
			end=a["argmax"]
		else:
			if a["change"]>0.2:
				good_list.append(a)
				start=end+1
				end=end+10
			else:
				start=a["argmin"]
				end=end+1
	data['type']='y'
	b=[]
	s=[]
	for i in good_list:
		if data.iloc[i["argmax"]].close>data.iloc[i["argmin"]].close:
			b.append(i["argmax"])
			s.append(i["argmin"])
		else:
			b.append(i["argmin"])
			s.append(i["argmax"])
	data.loc[s,'type']='r'
	data.loc[b,'type']='g'
	return data