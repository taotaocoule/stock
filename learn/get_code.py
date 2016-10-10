import urllib.request as request
from bs4 import BeautifulSoup
import re 

def get_all_code():
	url=r'http://quote.eastmoney.com/stocklist.html' 
	get=request.urlopen(url).read()
	soup=BeautifulSoup(get)
	li=[]
	for link in soup.find("div",{"class":"qox"}).find_all("a")[3:]:
		if len(link):
			a=re.compile('(\d{6})').findall(link.contents[0])[0]
			if a[0]=="0" or a[0]=="6":
				li.append(a)
	return li		
