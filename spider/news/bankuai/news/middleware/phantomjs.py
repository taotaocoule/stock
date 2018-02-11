# -*- coding: utf-8 -*-

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

path_phantomjs=r'D:\software\plantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe'

class dynamic(object):
	def process_request(self, request, spider):
		driver=webdriver.PhantomJS(path_phantomjs)
		driver.get(request.url)
		WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="table-data"]')))
		body=driver.page_source
		url=driver.current_url
		driver.close()
		return HtmlResponse(url,body=body,encoding='utf-8', request=request)