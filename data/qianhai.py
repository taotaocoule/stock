# 前海人寿利率公告
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path_phantomjs=r'D:\software\plantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe'
driver=webdriver.PhantomJS(path_phantomjs)
url=r'https://cms.foreseamall.com/publish/main/qhzx/tzgg/95/index.html'
driver.get(url)
c=driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[3]/ul/li/a')
title=[]
urls=[]
for i in c:
    title.append(i.text.split('万能保险结算利率公告')[0])
    urls.append(i.get_attribute('href'))

import numpy as np
import pandas as pd

table=pd.DataFrame(columns=['name','rate','day','time'])

for j in range(len(urls)):
    u=urls[j]
    ti=title[j]
    driver.get(u)
    print(ti)
    t=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[4]/table')
    q=t.text.split('\n')
    t=np.reshape(q,(30,3))[1:,:]
    ts=pd.DataFrame(t,columns=['name','rate','day'])
    ts['time']=ti
    table=table.append(ts)
