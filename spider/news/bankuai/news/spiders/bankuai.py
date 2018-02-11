# -*- coding: utf-8 -*-
import scrapy
from news.items import Bankuai
from scrapy.shell import inspect_response

class BankuaiSpider(scrapy.Spider):
    name = 'bankuai'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/center/BKList.html#trade_0_0?sortRule=0',
                  'http://quote.eastmoney.com/center/BKList.html#notion_0_0?sortRule=0']

    def parse(self, response):
        split_url = 'http://quote.eastmoney.com/web/'
        token_url = 'http://pifm3.eastmoney.com/EM_Finance2014PictureInterface/Index.aspx?ID=BK{}&UnitWidth=-6&imageType=KXL&EF=&Formula=RSI&type=&token=44c9d251add88e27b65ed86506f6e5da&r=0.5798964046082205'
        newList = response.xpath('//table[@class="table-data"]/tbody/tr')
        for i in range(1,len(newList)):
            tds = newList[i].xpath("td")
            item = Bankuai()
            item['catagory'] = 'trade' in response.url
            item['name'] = str(i)+'_'+tds[1].xpath('./a/text()').extract()[0]
            item['link'] = tds[2].xpath('./a')[0].xpath('./@href').extract()[0].split(split_url)[1].split('.')[0].split('bk')[1]
            item['image'] = token_url.format(item['link'])
            yield item
