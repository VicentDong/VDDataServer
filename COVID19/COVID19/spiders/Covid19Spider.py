# -*- coding: utf-8 -*-
import scrapy
from COVID19.items import Covid19Item
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 配置chromedriver
chorme_options = Options()


class Covid19Spider(scrapy.Spider):
    name = 'covid19spider'
    allowed_domains = ['voice.baidu.com']
    start_urls = ['https://voice.baidu.com']

    # 实例化一个浏览器对象
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chorme_options)
        super().__init__()

    def start_requests(self):
        url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3"
        response = scrapy.Request(url, callback=self.parse)
        yield response

    # 整个爬虫结束后关闭浏览器
    def close(self, spider):
        self.browser.quit()

    # 中国
    def parse(self, response):
        prnRows = response.xpath(
            '//*[@id="nationTable"]/table/tbody/tr').extract()
        for row in prnRows:
            item = Covid19Item()
            item['name'] = row.xpath(
                '/td[1]/div/span[2]').extract_first().text()
            item['parent'] = ''
            item['position'] = ''
            item['new'] = row.xpath('/td[2]').text()
            item['now'] = row.xpath('/td[3]').text()
            item['total'] = row.xpath('/td[4]').text()
            item['cure'] = row.xpath('/td[5]').text()
            item['death'] = row.xpath('/td[6]').text()
            yield item
