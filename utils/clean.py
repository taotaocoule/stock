import numpy as np

# 转换空值
def Na(pd):
	pd = pd.replace('-',np.nan)
	return pd

# 转化数量单位
def volumn(data):
	if '万亿' in data:
		return float(data.split('万亿')[0])*10000*10000
	elif '亿' in data:
		return float(data.split('亿')[0])*10000
	elif '万' in data:
		return float(data.split('万')[0])

def remove_percent(data):
	return data.replace('%','')