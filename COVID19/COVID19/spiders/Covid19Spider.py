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

        provinces = response.xpath(
            '//*[@id="listWraper"]/table[2]/tbody').extract()

        for prn in provinces:
            item = Covid19Item()
            prnNode = Selector(text=prn)
            item['name'] = prnNode.xpath(
                '//tr[1]/th/p[1]/span//text()').extract_first().replace('区', '')
            item['parent'] = ''
            item['new'] = prnNode.xpath(
                '//tr[1]/td[2]/p[2]//text()').extract_first()
            item['now'] = prnNode.xpath(
                '//tr[1]/td[1]/p[1]//text()').extract_first()
            item['total'] = prnNode.xpath(
                '//tr[1]/td[2]/p[1]//text()').extract_first()
            item['cure'] = prnNode.xpath(
                '//tr[1]/td[3]/p[1]//text()').extract_first()
            item['death'] = prnNode.xpath(
                '//tr[1]/td[4]/p[1]//text()').extract_first()

            cityNodes = prnNode.xpath('//*[@class="city"]').extract()
            for city in cityNodes:
                cityItem = Covid19Item()
                cityNode = Selector(text=city)
                cityItem['name'] = cityNode.xpath(
                    '//th/span//text()').extract_first().replace('区', '')
                cityItem['parent'] = item['name']
                cityItem['new'] = ''
                cityItem['now'] = cityNode.xpath(
                    '//td[1]//text()').extract_first()
                cityItem['total'] = cityNode.xpath(
                    '//td[2]//text()').extract_first()
                cityItem['cure'] = cityNode.xpath(
                    '//td[3]//text()').extract_first()
                cityItem['death'] = cityNode.xpath(
                    '//td[4]//text()').extract_first()
                yield cityItem

            yield item

    # 海外
    def parse_Outsee(self, response):
        countries = response.xpath(
            '//*[@id="foreignWraper"]/table/tbody').extract()
        for country in countries:
            countryNode = Selector(text=country)
            item = Covid19Item()
            item['name'] = countryNode.xpath(
                '//tr/th/span//text()').extract_first()
            item['parent'] = ''
            item['new'] = countryNode.xpath(
                '//tr/td[1]//text()').extract_first()
            item['now'] = ''
            item['total'] = countryNode.xpath(
                '//tr/td[2]//text()').extract_first()
            item['cure'] = countryNode.xpath(
                '//tr/td[3]//text()').extract_first()
            item['death'] = countryNode.xpath(
                '//tr/td[4]//text()').extract_first()
            yield item
