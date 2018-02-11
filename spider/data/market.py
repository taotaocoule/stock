# 当日市场情况
# 沪深成交，最近情况，融资融券余额，平均市盈率等
#市场两融数据：http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=tdate&sr=-1&p=1&ps=50000&js=(x)&type=RZRQ_LSTOTAL_NJ&mk_time=1&rt=50605278 
# 当日市场板块汇总数据：http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKHY&sty=FPGBKI&sortType=(ChangePercent)&sortRule=-1&page=2&pageSize=50&js=var%20kVVKzSwL={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1518317644703
# 单个板块数据：http://quote.eastmoney.com/web/BK04641.html

class Market(object):
	"""docstring for Global"""
	def __init__(self):
		self.title = '当日宏观情况'

	