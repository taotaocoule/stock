# 获取股票列表：
# 获取板块列表：http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKHY&sty=FPGBKI&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=5000&js=[(x)]&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1518417715207
# 板块参考页面：http://quote.eastmoney.com/centerv2/hsbk/hybk
# 概念板块列表：http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKGN&sty=FPGBKI&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=5000&js=[(x)]&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1518418323061
# 参考页面：http://quote.eastmoney.com/centerv2/hsbk/gnbk
import urllib.request
import json
import pandas as pd

class Board(object):
	"""docstring for Board"""
	def __init__(self):
		self.title = "板块列表"

	def board(self):
		raw = []
		# 行业板块/概念板块
		market = ['HY','GN']
		for i in market:
			url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BK{}&sty=FPGBKI&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=5000&js=[(x)]&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1518417715207'.format(i)
			data = json.loads(urllib.request.urlopen(url).read())
			raw.extend(list(map(lambda x:x.split(',')[1:6],data)))
		head = ['代码','板块名称','涨跌幅','总市值','换手率']
		return pd.DataFrame(raw,columns=head)