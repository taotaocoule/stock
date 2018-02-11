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
		self.market_ = self.market == '1' and 'sh' or 'sz'
	
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

	def business(self):
		url = 'http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code={}{}'.format(self.market_,self.code)
		raw = json.loads(urllib.request.urlopen(url).read())
		head = {
			"zygc":'主营构成',
			"zysr":'主营收入',
			"srbl":'收入比例',
			"zycb":'主营成本',
			"cbbl":'成本比例',
			"zylr":'主营利润',
			"lrbl":'利润比例',
			"mll":'毛利率',
			"rq":'日期',
			"dw":'单位'
		}
		# 行业分类
		hy = []
		# 区域分类
		qy = []
		# 产品分类
		cp = []
		for i in raw['zygcfx']:
			hy.extend(i['hy'])
			qy.extend(i['qy'])
			cp.extend(i['cp'])
		hy_pd = pd.DataFrame(hy)
		qy_pd = pd.DataFrame(qy)
		cp_pd = pd.DataFrame(cp)
		result = {
			'业务描述':raw['zyfw'][0]['ms'],
			'经营评述':raw['jyps'][0]['ms'],
			'行业业绩':hy_pd.rename(columns=head),
			'区域业绩':qy_pd.rename(columns=head),
			'产品业绩':cp_pd.rename(columns=head)
		}
		return result

# 题材信息：http://emweb.securities.eastmoney.com/PC_HSF10/CoreConception/CoreConceptionAjax?code=sh600000
	def theme(self):
		url = 'http://emweb.securities.eastmoney.com/PC_HSF10/CoreConception/CoreConceptionAjax?code={}{}'.format(self.market_,self.code)
		raw = json.loads(urllib.request.urlopen(url).read())
		result = raw["hxtc"][0]["ydnr"].split(' ')
		return result
