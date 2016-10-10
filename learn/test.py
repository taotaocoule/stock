import tushare as ts

def test(code,date1,date2):
	try:
		today=ts.get_hist_data(code)
	except:
		print('{} is wrong'.format(code))	
	else:	
		print('{} is running'.format(code))
		if today is not None:
			if not today.empty:
				tb=today[today.index==date1]
				ta=today[today.index==date2]
				if len(tb)>0 and len(ta)>0:
					diff=100*(ta.values[0,2]-tb.values[0,2])/tb.values[0,2]
					print('{} diff is {}'.format(code,diff))
					return diff
				else:
					return -11	

# for code in tests:
# 	test(code,'2016-08-29','2016-08-30')	