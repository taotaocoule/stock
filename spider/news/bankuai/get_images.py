# 获取板块汇总图片
# 命令行参数：phantomjs地址
# example:python get_images.py D:\software\plantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe
from selenium import webdriver
import json
import os
import sys

if len(sys.argv)<2:
    print("请输入phantomjs地址")
    sys.exit()

os.remove("./item.json")
os.system("scrapy crawl bankuai -o item.json")
print('=============crawled==================')
path_phantomjs=sys.argv[1]
driver=webdriver.PhantomJS(path_phantomjs)

data=json.load(open('item.json'))
for i in data:
    driver.get(i['image'])
    print("+++++++++saving {}+++++++++".format(i['name']))
    if i['catagory']:
        driver.save_screenshot('./bankuai/{}.png'.format(i['name']))
    else:
        driver.save_screenshot('./gainian/{}.png'.format(i['name']))

driver.close()   
print('================painted======================') 

from PIL import Image
import math
import re

def all_in_one(name):
    image_list=os.listdir("./{}".format(name))
    imagefile=[]
    for j in image_list:
        imagefile.append(Image.open("./{}/{}".format(name,j)))
    target=Image.new('RGB',(400*10,300*(1+int(len(image_list)/10))))
    for i in range(1,len(imagefile)+1):
        index = int(image_list[i-1].split('_')[0])
        target.paste(imagefile[i-1],(((index-1) % 10 )*400,(math.ceil(index/10)-1)*300))
    target.save("allInOne_{}.png".format(name))

print('================all_in_one_bankuai======================') 
all_in_one('bankuai')
print('================all_in_one_gainian======================') 
all_in_one('gainian')