import spider.data.stock as stock

a=stock.Stock('600000')
b=a.get()
b.to_csv('./database/stock/600000.csv',encoding='utf_8_sig',index=False)