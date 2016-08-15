#-*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from tutorial.items import TutorialItem

class Dytt8Spider(CrawlSpider):
	name = "dytt8"
	allowed_domains = ["dytt8.net"]
	start_urls = ['http://dytt8.net']
	index_urls = ['http://dytt8.net/index.html'] #container all list page's url
	item_urls = [] #container all movie page's url
	
	rules = {
		Rule(LinkExtractor(allow = ('index.html'),deny=('/html/game/','/html/music/')),callback='parse_index'),
#		Rule(LinkExtractor(allow = ('list_[0-9]+_[0-9]+.html')),callback='parse_list'),
#		Rule(LinkExtractor(allow = ('[0-9]+.html')),callback='parse_movie'),
	}

#	def parse(self,response):
#		self.log("parse:%s" % response.url)
	def parse_index(self,response):
#		self.log("parse_index:%s" % response.url)
		self.index_urls.append(response.url)
#		find movie page
		urls = response.xpath('//select//option[re:test(@value,"list_[0-9]+_[0-9]+.html")]//@value').extract()
		for url in urls:
			ret = response.url.replace('index.html',url)
			if ret not in self.index_urls:
				self.index_urls.append(ret)
				yield Request(url=ret,callback=self.parse_list)

	def parse_list(self,response):
#		self.log("parse_list:%s" % response.url)
		for link in LinkExtractor(allow='[0-9]+.html').extract_links(response):
			if link.url not in self.item_urls:
				self.item_urls.append(link.url)
#				yield Request(link.url,callback=self.parse_movie)
		
	def parse_movie(self, response):
#		self.log("parse_movie:%s" % response.url)
#		item = TutorialItem()	
#		item['title'] = response.xpath('//div[re:test(@class,"title_all")]/h1//text()').extract()[0]
#		item['issue_date'] =  response.xpath('//div[re:test(@class,"co_content8")]//ul//text()').extract()[0]
#		item['content'] = response.xpath('//div[re:test(@id,"Zoom")]//td//p').extract()[0]
#		item['download_url'] =  response.xpath('//div[re:test(@id,"Zoom")]//td//table//tbody//tr//td//a/@href').extract()
		#self.log("start parse"+title[0])
#		return item
		pass

	def closed(self,reason):
		print "index_urls:%d" % len(self.index_urls)
		print "item_urls:%d" % len(self.item_urls)			
