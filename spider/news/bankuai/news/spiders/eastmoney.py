# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem

class EastmoneySpider(scrapy.Spider):
    name = 'eastmoney'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://finance.eastmoney.com/yaowen.html']

    def parse(self, response):
    	newList = response.xpath("//div[@class='gl']").xpath("//a[contains(@href,'http://finance.eastmoney.com/news/')]")
    	for i in newList:
    		link = i.xpath("./@href").extract()
    		title = i.xpath("./text()").extract()
    		yield scrapy.http.Request(link[0],callback=self.parseDetail,meta={'link':link[0],'title':title})

    def parseDetail(self, response):
    	item = NewsItem()
    	item['link'] = response.meta['link']
    	item['title'] = response.meta['title']
    	data = response.xpath("//div[@id='ContentBody']")
    	item['detail'] = data.xpath("//p/text()").extract()
    	yield item
