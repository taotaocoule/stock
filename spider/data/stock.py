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

# 股东信息：http://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/ShareholderResearchAjax?code=sh600000
	def shareholder(self):
		url = 'http://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/ShareholderResearchAjax?code={}{}'.format(self.market_,self.code)
		raw = json.loads(urllib.request.urlopen(url).read())
		head = {
			"rq": "日期",
			"gdrs": "股东人数",
			"gdrs_jsqbh": "股东人数较上期变动幅度",
			"rjltg": "人均流通股数",
			"rjltg_jsqbh": "人均流通股数较上期变动幅度",
			"cmjzd": "筹码集中度",
			"gj": "股价",
			"rjcgje": "人均持股金额",
			"qsdgdcghj": "前十大股东持股合计",
			"qsdltgdcghj": "前十大流通股东持股合计",
			"mc": "名次",
			"gdmc": "股东名称",
			"gdxz": "股东性质",
			"gflx": "股份类型",
			"cgs": "持股数",
			"zltgbcgbl": "占总流通股本持股比例",
			"zj": "增减",
			"bdbl": "变动比例",
			"jjdm": "基金代码",
			"jjmc": "基金名称",
			"cgsz": "持仓市值",
			"zzgbb": "占总股本比",
			"zltb": "占流通比",
			"zjzb": "占净值比",
			"jjsj": "解禁时间",
			"jjsl": "解禁数量",
			"jjgzzgbbl": "解禁股占总股本比例",
			"jjgzltgbbl": "解禁股占流通股本比例",
			"gplx": "股票类型",
			"bdsj": "变动时间",
			"zzgbcgbl": "占总股本比例",
			"cj": "增减",
			"cjgzygdcgbl": "增减股占原股东持股比例",
			"bdyy": "变动原因"
		}
		# 股东人数
		gdrs_pd = pd.DataFrame(raw['gdrs'])
		# 限售解禁
		xsjj_pd = pd.DataFrame(raw['xsjj'])
		# 十大股东持股变动
		sdgdcgbd_pd = pd.DataFrame(raw['sdgdcgbd'])
		# 流通股东
		ltgd = []
		for i in raw['sdltgd']:
			ltgd.extend(i['sdltgd'])
		ltgd_pd = pd.DataFrame(ltgd)
		# 十大股东
		sdgd = []
		for i in raw['sdgd']:
			sdgd.extend(i['sdgd'])
		sdgd_pd = pd.DataFrame(sdgd)
		# 基金持股
		jjcg = []
		for i in raw['jjcg']:
			jjcg.extend(i['jjcg'])
		jjcg_pd = pd.DataFrame(jjcg)
		result = {
			"股东人数":gdrs_pd.rename(columns=head),
			"十大流通股东":ltgd_pd.rename(columns=head),
			"十大股东":sdgd_pd.rename(columns=head),
			"十大股东持股变动":sdgdcgbd_pd.rename(columns=head),
			"基金持股":jjcg_pd.rename(columns=head),
			"限售解禁":xsjj_pd.rename(columns=head)
		}
		return result

# 基金持仓明细:http://datapc.eastmoney.com/soft/zlsj_nonav/detail.aspx?code=600000&stat=0&data=2017-12-31
	def fund(self):
		url = 'http://datapc.eastmoney.com/soft/zlsj_nonav/detail.aspx?code={}&stat=0&data=2017-12-31'.format(self.code)
		return url