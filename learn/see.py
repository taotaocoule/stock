import numpy as np
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
data=ts.get_k_data("600000")

data['value']=100*(data.close.shift(-10)-data.close)/data.close

def ma(data,column,type,name='MA_'):
    for i in type:
        data[name+str(i)]=pd.rolling_mean(data[column],i)
        data[name+'_std_'+str(i)]=pd.rolling_std(data[column],i)
m=[15,30,60,90,120]
ma(data,'close',m)

data['parse_date']=pd.to_datetime(data.date.astype(str), infer_datetime_format = True, exact=False)

# def plot_five(data):
# 	plt.plot(data.parse_date,data.MA_15,label="15",color="yellow")
# 	plt.plot(data.parse_date,data.MA_30,label="30",color="purple")
# 	plt.plot(data.parse_date,data.MA_60,label="60",color="green")
# 	plt.plot(data.parse_date,data.MA_90,label="90",color="red")
# 	plt.plot(data.parse_date,data.MA_120,label="120",color="blue")

# 局部最大值，与局部最大值的位移距离（+-代表前后，index距离代表天数，
# 该段区间内最大最小值的差距（振幅），
# 扩大一倍距离是否有更大的振幅、且最大最小值发生变化）

close_value=data.close.values
data['help_index']=data.index

# 区间是什么形状：平的（<5%），中等（）

# 处在3周内的何等位置
temp_max=data.iloc[0].close
temp_min=data.iloc[0].close
def apply_type_distince(row,length):
	global temp_max,temp_min
	ranges=range(length,len(close_value)-length)
	index=row.help_index
	if (index in ranges):
		this_range=close_value[index-length:index+length]
		this_range_max=this_range.max()
		temp_max=this_range_max
		this_range_max_id=this_range.argmax()
		distance=this_range_max_id-length
		row['max_distance_'+str(length)]=distance
		diff=100*(this_range_max-row.close)/row.close
		row['max_diff_'+str(length)]=diff
		# 开始最小值
		this_range=close_value[index-length:index+length]
		this_range_min=this_range.min()
		temp_min=this_range_min
		this_range_min_id=this_range.argmin()
		distance=this_range_min_id-length
		row['min_distance_'+str(length)]=distance
		diff=(row.close-this_range_min)*100/this_range_min
		row['min_diff_'+str(length)]=diff
		return row
	else:
		if row.close>temp_max:
			temp_max=row.close
			row['max_distance_'+str(length)]=0
		else:
			row['max_distance_'+str(length)]=404
		if row.close<temp_min:
			temp_min=row.close
			row['min_distance_'+str(length)]=0
		else:
			row['min_distance_'+str(length)]=404
		row['max_diff_'+str(length)]=100*(temp_max-row.close)/row.close
		row['min_diff_'+str(length)]=(row.close-temp_min)*100/temp_min
		return row

# 二分法求所有极值
# step1:数组一分为二，中位数，与左右两侧最大值比较，若中位数大，则最大值为中位数
#       若中位数小，得到两个局部最大值
# step2:左右两块重复step1，知道拆分的数组长度小于给定值      

max_min_type=[7,14]
for i in max_min_type:
	data=data.apply(apply_type_distince,axis=1,args=(i,))

title=['min_distance_7', 'min_diff_7', 'max_distance_7',
       'max_diff_7', 'min_distance_14', 'min_diff_14', 'max_distance_14',
       'max_diff_14']

def find_nearest(array, values):
    values = np.atleast_1d(values)
    indices = np.abs(np.int64(np.subtract.outer(array, values))).argmin(0)
    return indices

max_index_7=data[data.max_diff_7==0.]['help_index'].values
min_index_7=data[data.min_diff_7==0.]['help_index'].values

temp_max_index=0
temp_max_diff=100*(data.iloc[max_index_7[0]].close-data.iloc[min_index_7[0]].close)/data.iloc[min_index_7[0]].close
def find_type(row):
	global temp_max_index,temp_max_diff
	if np.abs(row['min_diff_7'])>0:
		row['nearest_max_index_7']=temp_max_index
		row['nearest_max_diff_7']=temp_max_diff
	else:
		find_index=find_nearest(max_index_7,row['help_index'])
		nearest_max_index=max_index_7[find_index[0]]
		if row['help_index']<nearest_max_index and find_index[0]>0:
			nearest_max_index=max_index_7[find_index[0]-1]
		row['nearest_max_index_7']=nearest_max_index
		temp_max_diff=100*(data.iloc[nearest_max_index].close-row.close)/row.close
		row['nearest_max_diff_7']=temp_max_diff
		temp_max_index=nearest_max_index
	return row

data=data.apply(find_type,axis=1)

# 两个最值点，定义为7和14都为最值
data['lower']=data['min_distance_7']+data['min_distance_14']
data['upper']=data['max_distance_7']+data['max_distance_14']