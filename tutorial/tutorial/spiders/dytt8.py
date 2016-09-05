#-*- coding: utf-8 -*-
import scrapy
import re
import os
import time
import json
from scrapy.exceptions import DropItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from tutorial.items import TutorialItem
from scrapy import log

class Dytt8Spider(CrawlSpider):
	name = "dytt8"
	allowed_domains = ["dytt8.net"]
	start_urls = ['http://dytt8.net']
#	start_urls = ['http://www.dytt8.net/html/tv/oumeitv/20120920/39429.html']
	index_urls = ['http://dytt8.net/index.html'] #container all list page's url
	item_urls = [] #container all movie page's url

	rules = {
		Rule(LinkExtractor(allow = ('index.html'),deny=('/html/game/','/html/music/','/html/2009zongyi/')),callback='parse_index'),
#		Rule(LinkExtractor(allow = ('list_[0-9]+_[0-9]+.html')),callback='parse_list'),
#		Rule(LinkExtractor(allow = ('[0-9]+.html')),callback='parse_movie'),
	}
	
	def __init__(self):
		super(Dytt8Spider,self).__init__()
		self.starttime = time.time()
		#init mysql
		self.log( os.path.dirname(__file__),log.WARNING)
		self.secret_file = os.path.dirname(__file__) + "/../../../secret.js"
		with open(self.secret_file,"r") as fo:
			secret = json.load(fo)
			self.mysql_host = secret["mysql"]["host"];
			self.mysql_user = secret["mysql"]["user"];
			self.mysql_database = secret["mysql"]["database"];
			self.mysql_pw = secret["mysql"]["pw"];

			self.oss_host = secret["oss"]["host"];
			self.oss_bucket = secret["oss"]["bucket"];
			self.oss_keyid = secret["oss"]["AccessKeyID"];
			self.oss_keysecret = secret["oss"]["AccessKeySecret"];
			
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
				yield Request(link.url,callback=self.parse_movie)
		
	def parse_movie(self, response):
#	def parse(self, response):
#		self.log("parse_movie:%s" % response.url)
		item = TutorialItem()
		item['origin'] = response.url
		item['type'] = self.gettypebyurl(response.url)
		item['title'] = response.xpath('//div[re:test(@class,"title_all")]/h1//text()').extract_first()
		
		issue_date =  response.xpath('//div[re:test(@class,"co_content8")]//ul//text()').re_first('[0-9]{4}-[0-9]+-[0-9]+')
		if issue_date is not None:
			if time.strptime(issue_date,"%Y-%m-%d") > time.strptime("2014-01-01","%Y-%m-%d"):
				item['issue_date'] = issue_date
			else:
				return DropItem("issue_date %s" % issue_date)
		else:
			return DropItem("issue_date is None.")

#		content = response.xpath('//div[re:test(@id,"Zoom")]//td//p').extract_first()
		content = response.xpath('//div[re:test(@id,"Zoom")]').extract_first()
		if content is not None:
			content = content.replace(u'\'',u'\\\'')
			content = content.replace(u'\"',u'\\\"')
			item['content'] = content
		else:
			self.log(u'[%s] content is None.' % response.url, level = log.WARNING)
			return DropItem(response.url)

		item['icon'] = response.xpath('//div[re:test(@id,"Zoom")]//td//p//img//@src').extract_first()

		download_urls =  response.xpath('//div[re:test(@id,"Zoom")]//td//table//tbody//tr//td//a/@href').extract()
		item['download_url'] = u''
		for url in download_urls:
			item['download_url'] = item['download_url'] + url + u';'
		
		item['image_urls'] = []
#		item['image_urls'] = response.xpath('//div[re:test(@id,"Zoom")]//td//p//img//@src').extract_first()
#		item['image_urls'].append('http://juqing.9duw.com/UploadPic/2016-6/2016628054693733.jpg')

#		item['download_url'] =  response.xpath('//div[re:test(@id,"Zoom")]//td//table//tbody//tr//td//a/@href').extract()
		#self.log("start parse"+title[0])
		return item

	def gettypebyurl(self,url):
		temp = re.search(r'/[a-z]+/[0-9]+',url) 
		if temp:
			movietype = re.search(r'[a-z]+',temp.group())
			if movietype:
				return movietype.group()
		return "";

	def closed(self,reason):
		self.log("index_urls:%d" % len(self.index_urls),level = log.WARNING)
		self.log("item_urls:%d" % len(self.item_urls),level = log.WARNING)			
		self.log("run time:%ds" % (time.time() - self.starttime),level = log.WARNING)			
