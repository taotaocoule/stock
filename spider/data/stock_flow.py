# 个股净流入:http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(FFRank)&sr=1&p=1&ps=10000&js=[(x)]&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=50602335
# 板块净流入

import urllib.request
import pandas as pd
import json

class Stock_Flow(object):
	"""docstring for Stock_Flow"""
	def __init__(self):
		self.arg = 0

# 主力净流入排名情况 当日排名
	def stock_flow_main_index(self):
		url = r'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(FFRank)&sr=1&p=1&ps=10000&js=[(x)]&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=50602335'
		raw = json.loads(urllib.request.urlopen(url).read())
		head = ['市场','股票代码','股票名','最新价','主力净占比','今日排名','今日涨跌','5日主力净占比','5日排名','5日涨跌','10日主力净占比','10日排名','10日涨跌','所属板块','板块代码','日期']
		return pd.DataFrame(list(map(lambda x:x.split(','),raw)),columns=head)

# 个股资金情况 当日排名
	def stock_flow_share_index(self):
		url = r'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=10000&js=[(x)]&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA&rt=50602511'
		raw = json.loads(urllib.request.urlopen(url).read())
		#  "2,000725,京东方A,5.78,3.40,69702.53,12.32,89270.16,15.78,-19567.64,-3.46,-33980.60,-6.01,-35721.92,-6.31,2018-03-06 14:26:45,0.19"
		head = ['市场','股票代码','股票名','最新价','涨跌幅','主力净流入','主力净占比','超大单净流入','超大单净占比','大单净流入','大单净占比','中单净流入','中单净占比','小单净流入','小单净占比','日期','涨跌额']
		return pd.DataFrame(list(map(lambda x:x.split(','),raw)),columns=head)

# 板块资金情况 当日排名
	def stock_flow_bk_index(self):
		url = r'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKHY&type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=10000&js=[(x)]&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK&rt=50602537'
		raw = json.loads(urllib.request.urlopen(url).read())
		head = ['市场','板块代码','板块名','涨跌幅','主力净流入','主力净占比','超大单净流入','超大单净占比','大单净流入','大单净占比','中单净流入','中单净占比','小单净流入','小单净占比','主力净流入最大股','股票代码']
		return pd.DataFrame(list(map(lambda x:x.split(','),raw)),columns=head)

# 个股历史资金流向:http://ff.eastmoney.com//EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&js=(x)&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id=6000001&_=1518337301854
	def stock_flow_share(self,code):
		market = code.startswith('6') and '1' or '2'
		url = 'http://ff.eastmoney.com//EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&js=(x)&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id={}{}&_=1518337301854'.format(code,market)
		raw = json.loads(urllib.request.urlopen(url).read())
		# "2018-02-09,3737.4048,2.01%,9897.7232,5.33%,-6160.3184,-3.32%,-6793.296,-3.66%,3055.8916,1.65%,12.78,-2.44%"
		head = ['日期','主力净流入额','主力净流入占比','超大单净流入额','超大单净流入占比','大单净流入额','大单净流入占比','中单净流入额','中单净流入占比','小单净流入额','小单净流入占比','收盘价','涨跌幅']
		return pd.DataFrame(list(map(lambda x:x.split(','),raw)),columns=head)