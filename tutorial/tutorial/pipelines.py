# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import json
import MySQLdb as mdb
from scrapy import log

class TutorialPipeline(object):
	def __init__(self):
		pass
	def __del__(self):
		self.db.close()
		pass

	def open_spider(self,spider):
		self.item_count = 0
		self.error_count = 0
		self.db = mdb.connect(spider.mysql_host,spider.mysql_user,spider.mysql_pw,spider.mysql_database,True,charset="utf8")
#		self.file = open("items.js","wb")
		pass
	def close_spider(self,spider):
		item_msg = u'item ocunt:%d ' % self.item_count
		error_msg = u'db error ocunt:%d ' % self.error_count
		spider.log(item_msg , level = log.WARNING)
		spider.log(error_msg , level = log.WARNING)
		pass

	def process_item(self, item, spider):
		self.cursor = self.db.cursor()
		insert_temp = "insert into movie(type,date,title,icon,content,url) values('%s','%s','%s','%s','%s','%s')"
		insert_sql = insert_temp % (item['type'],item['issue_date'],item['title'],item['icon'],item['content'],item['download_url'])
		spider.log(insert_sql,level = log.DEBUG)
		try:
			self.cursor.execute(insert_sql)
			self.db.commit()

#			item_file = open("items/%s" % item['url'],"wb")
#			line = json.dumps(dict(item)) 
#			file.write(line)
#			file.close()
		except mdb.Error,e:
			msg = u'[%s] db error:%s' % (item['origin'],unicode(e))
			spider.log(msg , level = log.WARNING)
			self.db.rollback()
			self.error_count = self.error_count + 1
		self.item_count = self.item_count + 1
		return item
