# 融资融券数据
# http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(scode=%27600000%27)
# 解析列明：
# tdate：日期，sname：股票名，scode：股票代码，market：所在市场，close：收盘价
# zdf：涨跌幅，
# rzye：融资余额，rzyezb：融资余额占比，rzmre：融资买入额，
# rzche：融资偿还额，rzjmre：融资净买入额，
# rqye：融券余额，rqyl：融券余量，rqmcl：融券卖出量，rqchl：融券偿还量，rqjmcl：融券净卖出量
# rzrqye：融资融券余额，rzrqyecz：融资融券余额差额
import pandas as pd
import urllib.request

class Margin(object):
	"""docstring for margin"""
	def __init__(self, code):
		self.data = download(code)

	def get(self):
		head = {"tdate":"日期","sname":"股票名","scode":"股票代码",
				"market":"所在市场","close":"收盘价","zdf":"涨跌幅",
				"rzye":"融资余额","rzyezb":"融资余额占比","rzmre":"融资买入额",
				"rzche":"融资偿还额","rzjmre":"融资净买入额","rqye":"融券余额",
				"rqyl":"融券余量","rqmcl":"融券卖出量","rqchl":"融券偿还量",
				"rqjmcl":"融券净卖出量","rzrqye":"融资融券余额","rzrqyecz":"融资融券余额差额"
				}
		raw = self.data.rename(columns=head)
		return raw

def download(code):
	url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(scode=%27{}%27)'.format(code)
	data = urllib.request.urlopen(url).read()
	return pd.read_json(data)
