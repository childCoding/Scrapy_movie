# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import json
import MySQLdb as mdb

class TutorialPipeline(object):
	def __init__(self):
		self.db = mdb.connect("localhost","root","carlos940413","scrapymovie",True,charset="utf8")
#		self.file = open("items.js","wb")
		pass
	def __del__(self):
		self.db.close()
		pass

	def open_spider(self,spider):
		pass
	def close_spider(self,spider):
		pass

	def process_item(self, item, spider):
		self.cursor = self.db.cursor()
		insert_temp = "insert into movie(date,title,content,url) values('%s','%s','%s','%s')"
		insert_sql = insert_temp % (item['issue_date'],item['title'],item['content'],item['download_url'])
		spider.log(insert_sql)
		try:
			self.cursor.execute(insert_sql)
			self.db.commit()

#			item_file = open("items/%s" % item['url'],"wb")
#			line = json.dumps(dict(item)) 
#			file.write(line)
#			file.close()
		except mdb.Error,e:
			spider.log(u'db error:%s' % repr(e))
			self.db.rollback()

		return item
