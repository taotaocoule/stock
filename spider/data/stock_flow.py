# 个股净流入:http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(FFRank)&sr=1&p=1&ps=10000&js=[(x)]&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=50602335
# 板块净流入

import urllib.request
import pandas as pd
import json

class Stock_Flow(object):
	"""docstring for Stock_Flow"""
	def __init__(self):
		self.arg = 0

# 主力净流入排名情况
	def stock_flow_main(self):
		url = r'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(FFRank)&sr=1&p=1&ps=10000&js=[(x)]&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=50602335'
		raw = json.loads(urllib.request.urlopen(url).read())
		head = ['市场','股票代码','股票名','最新价','主力净占比','今日排名','今日涨跌','5日主力净占比','5日排名','5日涨跌','10日主力净占比','10日排名','10日涨跌','所属板块','板块代码','日期']
		return pd.DataFrame(list(map(lambda x:x.split(','),raw)),columns=head)

# 个股资金情况
	def stock_flow_share(self):
		url = r'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=10000&js=[(x)]&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA&rt=50602511'
		raw = json.loads(urllib.request.urlopen(url).read())
		head = ['市场','股票代码','股票名','最新价','涨跌幅','主力净流入','主力净占比','超大单净流入','超大单净占比','大单净流入','大单净占比','中单净流入','中单净占比','小单净流入','小单净占比','日期']
		return pd.DataFrame(list(map(lambda x:x.split(','),raw)),columns=head)

# 板块资金情况
	def stock_flow_bk(self):
		url = r'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKHY&type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=10000&js=[(x)]&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK&rt=50602537'
		raw = json.loads(urllib.request.urlopen(url).read())
		head = ['市场','板块代码','板块名','涨跌幅','主力净流入','主力净占比','超大单净流入','超大单净占比','大单净流入','大单净占比','中单净流入','中单净占比','小单净流入','小单净占比','主力净流入最大股','股票代码']
		return pd.DataFrame(list(map(lambda x:x.split(','),raw)),columns=head)