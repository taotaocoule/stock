import urllib.request
import json

liveNewsUrl=r'http://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_1_.html?r=0.29795602867346616'

liveNewsData=urllib.request.urlopen(liveNewsUrl)
news=liveNewsData.read()
news=news[15:].decode()

a=json.loads(news)
b=a['LivesList']

print(b)