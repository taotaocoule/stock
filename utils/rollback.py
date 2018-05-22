import datetime
import tushare as ts

# 返回指定区段的变动幅度
def rollback(code,end=datetime.date.today(),interval=30):
	end=datetime.datetime.strptime(end, "%Y-%m-%d").date()
	endtime=end.strftime('%Y-%m-%d')
	starttime=(end-datetime.timedelta(days=interval)).strftime('%Y-%m-%d')
	data=ts.get_k_data(code,start=starttime,end=endtime)
	return 100*(data.tail(1).close.values[0]-data.head(1).close.values[0])/data.head(1).close.values[0]