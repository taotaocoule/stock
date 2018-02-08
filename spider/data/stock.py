# 股票数据地址，带振幅：http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=6000001&TYPE=k
# 参考地址：http://quote.eastmoney.com/chart/h5.html?StockCode=600000
# http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&id=0000012&type=wk&authorityType=&_=1517968253860
# http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&id=6000001&type=k&authorityType=&_=1517967994707
# 沪市：代码+1，深市：代码+2
# 单一个股数据，带振幅
import json
import pandas as pd
import urllib.request

class Stock(object):
	"""docstring for Stock"""
	def __init__(self, code):
		self.code = code
		self.market = self.code.startswith('6') and '1' or '2'
	
	def get(self):
		data = list(map(lambda x:x.split(','),self.download()['data']))
		head = ['日期','开盘价','收盘价','最高价','最低价','成交量','成交额','振幅']
		dataForm = pd.DataFrame(data,columns=head)
		dataForm['股票代码'] = self.code
		return dataForm

	def download(self):
		url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&id={}{}&type=k&authorityType=&_=1517967994707'.format(self.code,self.market)
		raw = json.loads(urllib.request.urlopen(url).read()[1:-1])
		return raw