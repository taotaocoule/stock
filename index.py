import spider.data.stock as stock
import spider.data.index as index

# 中证行业指数列表
# 绘制中证指数一览图
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

# 绘图
# good=[]
def pic(filename):
    location='./database/stock/'+filename
    data=pd.read_csv(location)
    b=data[data.BS == 'B']
    for i in b.index:
        if int(i)>60 and int(i)<len(data)-30:
            period=b.loc[i]['period']+3
            raw=data.iloc[i-60:i+period,:]
            raw.BS.replace({'N':'yellow','S':'green','B':'red'},inplace=True)
            plt.subplot(3,3,5)
            plt.scatter(range(len(raw)),raw['收盘价'],c=raw.BS)
            plt.subplot(3,3,1)
            plt.plot(range(len(raw)),raw['rsi6'])
            plt.plot(range(len(raw)),raw['rsi12'])
            plt.plot(range(len(raw)),raw['rsi24'])
            plt.title('RSI')
            plt.subplot(3,3,2)
            plt.plot(range(len(raw)),raw['kdj_k'])
            plt.plot(range(len(raw)),raw['kdj_d'])
            plt.plot(range(len(raw)),raw['kdj_j'])
            plt.title('KDJ')
            plt.subplot(3,3,3)
            plt.plot(range(len(raw)),raw['diff'])
            plt.plot(range(len(raw)),raw['dea'])
            plt.plot(range(len(raw)),raw['macd'])
            plt.title('MACD')
            plt.subplot(3,3,4)
            plt.plot(range(len(raw)),raw['wr10'])
            plt.plot(range(len(raw)),raw['wr6'])
            plt.title('WR')
            plt.subplot(3,3,9)
            plt.plot(range(len(raw)),raw['roc'])
            plt.plot(range(len(raw)),raw['rocma'])
            plt.title('ROC')
            plt.subplot(3,3,7)
            plt.plot(range(len(raw)),raw['pdi'])
            plt.plot(range(len(raw)),raw['mdi'])
            plt.plot(range(len(raw)),raw['adx'])
            plt.plot(range(len(raw)),raw['adxr'])
            plt.title('PDI')
            plt.subplot(3,3,8)
            plt.plot(range(len(raw)),raw['成交量'])
            plt.title('Volume')
            plt.subplot(3,3,6)
            plt.plot(range(len(raw)),raw['振幅'])
            plt.title('zheng')
            this=b.loc[i]
            imgName='./database/img/'+str(this['股票代码'])+'-'+str(i)+'.png'
            plt.savefig(imgName)
            plt.close()
            print(imgName)
            s=[this['股票代码'],i,this['表现'],imgName]
            good.append(s)