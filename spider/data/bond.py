# 国债指数：id=0000121;http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000121&TYPE=k&js=(x)&rtntype=5&isCR=false&fsData1518154947301=fsData1518154947301
# 沪市企业: id=0000131;http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000131&TYPE=k&js=(x)&rtntype=5&isCR=false&fsData1518156740923=fsData1518156740923
# 深圳企业：id=3994812;http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=3994812&TYPE=k&js=(x)&rtntype=5&isCR=false&fsData1518156947700=fsData1518156947700

import urllib.request
import pandas as pd
import json

class Bond(object):
	"""docstring for Bond"""
	def __init__(self):
		self.index = {
			'国债指数':'0000121',
			'沪市企业债':'0000131',
			'深圳企业债':'3994812'
		}

	def bond_index(self,id):
		url = r'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id={}&TYPE=k&js=(x)&rtntype=5&isCR=false&fsData1518154947301=fsData1518154947301'.format(id)
		raw = json.loads(urllib.request.urlopen(url).read())
		head = ['日期','开盘','收盘','最高','最低','成交量','成交金额','振幅']
		return pd.DataFrame(list(map(lambda x:x.split(','),raw['data'])),columns=head)