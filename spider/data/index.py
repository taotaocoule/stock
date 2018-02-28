# 指数数据
# 中证指数官网:http://www.csindex.com.cn/zh-CN/indices/index
# 中证指数列表：http://www.csindex.com.cn/zh-CN/indices/index?page=1&page_size=50&by=desc&order=%E6%8C%87%E6%95%B0%E4%BB%A3%E7%A0%81&data_type=json&class_18=18&class_19=19
# 中证指数：http://www.csindex.com.cn/zh-CN/indices/index-detail/000908?earnings_performance=5%E5%B9%B4&data_type=json
import pandas as pd
import urllib.request
import json

class Index(object):
	"""docstring for Index"""
	def __init__(self):
		self.title = '各类指数信息'

# 中证指数,参数指数代码
	def csindex(self,code):
		url = 'http://www.csindex.com.cn/zh-CN/indices/index-detail/{}?earnings_performance=5%E5%B9%B4&data_type=json'.format(code)
		data = urllib.request.urlopen(url).read()
		return pd.DataFrame(json.loads(data))

# 所有中证指数：http://www.csindex.com.cn/zh-CN/indices/index?page=1&page_size=50&by=desc&order=%E6%8C%87%E6%95%B0%E4%BB%A3%E7%A0%81&data_type=json
	def index_list(self):
		url = 'http://www.csindex.com.cn/zh-CN/indices/index?page={}&page_size=50&by=desc&order=%E6%8C%87%E6%95%B0%E4%BB%A3%E7%A0%81&data_type=json'
		start = url.format(1)
		data = []
		raw = json.loads(urllib.request.urlopen(start).read())
		total_page = int(raw['total_page'])
		data.extend(raw['list'])
		for i in range(2,total_page+1):
			next_url = url.format(i)
			raw = json.loads(urllib.request.urlopen(start).read())
			print('{}/{}'.format(i,total_page))
			data.extend(raw['list'])
		return pd.DataFrame(data)

