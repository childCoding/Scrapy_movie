# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tutorial.items import TutorialItem

class Dytt8MovieSpider(scrapy.Spider):
    name = "dytt8_movie"
    allowed_domains = ["dytt8.net"]
    start_urls = (
        'http://dytt8.net/html/tv/hytv/20160510/50952.html',
    )

    def parse(self, response):
		self.log("parse:%s" % response.url)
		item = TutorialItem()	
		item['title'] = response.xpath('//div[re:test(@class,"title_all")]/h1//text()').extract()[0]
		item['issue_date'] =  response.xpath('//div[re:test(@class,"co_content8")]//ul//text()').extract()[0]
#		item['content'] = response.xpath('//div[re:test(@id,"Zoom")]//td//p').extract()[0]
		item['download_url'] =  response.xpath('//div[re:test(@id,"Zoom")]//td//table//tbody//tr//td//a/@href').extract()
		#self.log("start parse"+title[0])
		return item
