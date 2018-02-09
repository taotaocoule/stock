# 当日市场情况
# 沪深成交，最近情况，融资融券余额，平均市盈率等
#市场两融数据：http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=tdate&sr=-1&p=1&ps=50000&js=(x)&type=RZRQ_LSTOTAL_NJ&mk_time=1&rt=50605278 

class Market(object):
	"""docstring for Global"""
	def __init__(self):
		self.title = '当日宏观情况'

	