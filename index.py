import spider.data.stock as stock
import spider.data.index as index

a=stock.Stock('600000')
b=a.get()
b.to_csv('./database/stock/600000.csv',encoding='utf_8_sig',index=False)

# 中证行业指数列表
a=index.Index()
b=a.index_list()
c=b[(b.class_classify == '行业') & (b.class_eregion == 'China Mainland')]
e=c.drop_duplicates('indx_sname')
f=e.index_code.values
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.figure(figsize=(150,100), dpi=80)
for i in range(1,len(f)+1):
	try:
		z=a.csindex(f[i-1])
	except:
		print(e[e.index_code == f[i-1]]['indx_sname'].values[0])
	else:
		z['tradedate']=z['tradedate'].apply(pd.to_datetime)
		z=z.apply(pd.to_numeric,errors='ignore')
		plt.subplot(6,7,i)
		plt.plot(z.tradedate,z.tclose)
		print(i)
		plt.title(e[e.index_code == f[i-1]]['indx_sname'].values[0])
