# 资金情况
# 沪港通，逆回购，债券市场的成交量
# 上海逆回购：http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._DEBT_SH_H&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=2&pageSize=20&js=var%20maAWFzQD={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1518418515784
# 上海逆回购参考：http://quote.eastmoney.com/centerv2/zqsc/shhg
# 深圳逆回购：http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._DEBT_SZ_H&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=20&js=var%20agQHFwRQ={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1518418637700
# 深圳逆回购参考：http://quote.eastmoney.com/centerv2/zqsc/szhg
import urllib.request
import json
import pandas as pd

class Capital(object):
	"""docstring for Capital"""
	def __init__(self):
		self.title = "资金情况"
		self.CentralBank = "http://www.pbc.gov.cn/diaochatongjisi/116219/116225/index.html"

# 逆回购情况
	def repurchase(self):
		raw = []
		for market in ['SH','SZ']:
			url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._DEBT_{}_H&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=500&js=[(x)]&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1518418515784'.format(market)
			data = json.loads(urllib.request.urlopen(url).read())
			raw.extend(list(map(lambda x:x.split(',')[:13],data)))
		head = ['序号','代码','逆回购名称','最新价','涨跌额','涨跌幅','振幅','成交量','成交额','昨收','今开','最高','最低']
		# 1,204003,GC003,4.550,1.300,40.00%,22.00,13837900,13837900032,3.250,4.350,4.735,4.020,-,-,-,-,-,-,-,-,5.20%,1.16,-,-,0001-01-01
		return pd.DataFrame(raw,columns=head)