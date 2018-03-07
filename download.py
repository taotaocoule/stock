import spider.data.stock_flow as flow
import feature.feature as feature
import multiprocessing
import math

flow=flow.Stock_Flow()
b=[]
l=flow.stock_flow_share_index()['股票代码'].values
step=math.ceil(len(l)/7)

for i in range(7):
	b.append(l[i*step:(i+1)*step])

def process(data):
	now=0
	for i in data:
		try:
			a=feature.Stock(i)
		except:
			print('Error {}'.format(i))
			now=now+1
		else:
			raw=a.clean()
			if len(raw)>0:
				loc='./database/stock/{}.csv'.format(i)
				raw.to_csv(loc,encoding='utf_8_sig',index=False)
			now=now+1
			print(now)

if __name__ == '__main__':
	for i in b:
		p=multiprocessing.Process(target=process,args=(i,))
		p.start()