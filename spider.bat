@echo off


E:
cd E:\VDDataServer\COVID19
scrapy crawl covid19spider

TIMEOUT /T 10
exit