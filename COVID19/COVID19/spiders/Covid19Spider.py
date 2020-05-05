# -*- coding: utf-8 -*-
import scrapy
from COVID19.items import Covid19Item
from scrapy.selector import Selector
from time import sleep


class Covid19Spider(scrapy.Spider):
    name = 'covid19spider'
    allowed_domains = ['news.qq.com']
    start_urls = ['https://news.qq.com/']

    def start_requests(self):
        # 定义要爬取的页面列表
        urls = ["https://news.qq.com/zt2020/page/feiyan.htm#/?ct=United%20States&nojump=1",
                "https://news.qq.com/zt2020/page/feiyan.htm#/global?ct=United%20States&nojump=1"]
        # 循环发送请求
        for i in range(len(urls)):
            if i == 0:
                # 执行中国疫情页面的parer
                yield scrapy.Request(urls[i], callback=self.parse_China, meta={'page': i}, dont_filter=True)
            else:
                 # 执行海外疫情页面的parer
                yield scrapy.Request(urls[i], callback=self.parse_Outsee, meta={'page': i}, dont_filter=True)

    # 疫情 中国
    def parse_China(self, response):
        # 中国
        chinaItem = Covid19Item()
        chinaItem['name'] =  '中国'
        chinaItem['parent'] = '全球'
        chinaNew =response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/span//text()').extract_first().strip()
        chinaItem['new'] = ''.join(list(filter(str.isdigit,chinaNew)))
        chinaItem['now'] =  response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[4]/div[2]//text()').extract_first().strip()
        chinaItem['total'] = response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[1]/div[2]//text()').extract_first().strip()
        chinaItem['cure'] = response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[2]/div[2]//text()').extract_first().strip()
        chinaItem['death'] = response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[3]/div[2]//text()').extract_first().strip()
        chinaItem['time'] = response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[2]/p/span//text()').extract_first().strip()
        yield chinaItem

        chinaItem1 = Covid19Item()
        chinaItem1['name'] =  '国内'
        chinaItem1['parent'] = '中国'
        chinaNew =response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/span//text()').extract_first().strip()
        chinaItem1['new'] = ''.join(list(filter(str.isdigit,chinaNew)))
        chinaItem1['now'] =  response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[4]/div[2]//text()').extract_first().strip()
        chinaItem1['total'] = response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[1]/div[2]//text()').extract_first().strip()
        chinaItem1['cure'] = response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[2]/div[2]//text()').extract_first().strip()
        chinaItem1['death'] = response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[3]/div[3]/div[2]//text()').extract_first().strip()
        chinaItem1['time'] = response.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[2]/p/span//text()').extract_first().strip()
        yield chinaItem1
        # 省份
        provinces = response.xpath('//*[@id="listWraper"]/table[2]/tbody').extract()
        for prn in provinces:
            item = Covid19Item()
            prnNode = Selector(text=prn)
            item['name'] =  prnNode.xpath('//tr[1]/th/p[1]/span//text()').extract_first().replace('区','').strip()
            item['parent'] = '中国'
            prnNew =  prnNode.xpath('//tr[1]/td[2]/p[2]//text()').extract_first().strip()
            item['new'] = ''.join(list(filter(str.isdigit,prnNew)))
            item['now'] =  prnNode.xpath('//tr[1]/td[1]/p[1]//text()').extract_first().strip()
            item['total'] = prnNode.xpath('//tr[1]/td[2]/p[1]//text()').extract_first().strip()
            item['cure'] = prnNode.xpath('//tr[1]/td[3]/p[1]//text()').extract_first().strip()
            item['death'] = prnNode.xpath('//tr[1]/td[4]/p[1]//text()').extract_first().strip()
            item['time'] = chinaItem['time']           
            # 城市
            cityNodes = prnNode.xpath('//*[@class="city"]').extract()
            for city in cityNodes:
                cityItem = Covid19Item()
                cityNode = Selector(text=city)

                cityItem['name'] =  cityNode.xpath('//th/span//text()').extract_first().replace('区','').strip()
                cityItem['parent'] = item['name'] 
                cityItem['new'] = ''
                cityItem['now'] = cityNode.xpath('//td[1]//text()').extract_first().strip()
                cityItem['total'] = cityNode.xpath('//td[2]//text()').extract_first().strip()
                cityItem['cure'] = cityNode.xpath('//td[3]//text()').extract_first().strip()
                cityItem['death'] = cityNode.xpath('//td[4]//text()').extract_first().strip()
                cityItem['time'] = chinaItem['time']
                yield cityItem
            yield item

    # 海外
    def parse_Outsee(self,response):
        # 海外 
        globeItem = Covid19Item()
        globeItem['name'] =  '海外'
        globeItem['parent'] = '全球'
        globeNew = response.xpath('//*[@id="foreignList"]/div[1]/div[3]/div[2]/p/span//text()').extract_first().strip()
        globeItem['new'] =  ''.join(list(filter(str.isdigit,globeNew)))
        globeItem['now'] = response.xpath('//*[@id="foreignList"]/div[1]/div[3]/div[1]/div[1]//text()').extract_first().strip()
        globeItem['total'] = response.xpath('//*[@id="foreignList"]/div[1]/div[3]/div[2]/div[1]//text()').extract_first().strip()
        globeItem['cure'] = response.xpath('//*[@id="foreignList"]/div[1]/div[3]/div[3]/div[1]//text()').extract_first().strip()
        globeItem['death'] = response.xpath('//*[@id="foreignList"]/div[1]/div[3]/div[4]/div[1]//text()').extract_first().strip()
        globeItem['time'] = response.xpath('//*[@id="foreignList"]/div[1]/div[2]/p/span//text()').extract_first().strip()
        yield globeItem
        # 国家
        countries = response.xpath('//*[@id="foreignWraper"]/table/tbody').extract()
        for country in countries:
            countryNode = Selector(text=country)
            item = Covid19Item()
            item['name'] =  countryNode.xpath('//tr[1]/th/span//text()').extract_first().strip()
            item['parent'] = globeItem['name'] 
            countryNew = countryNode.xpath('//tr[1]/td[1]//text()').extract_first().strip()
            item['new'] =''.join(list(filter(str.isdigit,countryNew)))
            item['now'] = ''.strip()
            item['total'] = countryNode.xpath('//tr[1]/td[2]//text()').extract_first().strip()
            item['cure'] = countryNode.xpath('//tr[1]/td[2]//text()').extract_first().strip()
            item['death'] = countryNode.xpath('//tr[1]/td[4]//text()').extract_first().strip()
            item['time'] = globeItem['time']
            yield item
