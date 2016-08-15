# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import json

class TutorialPipeline(object):
	def __init__(self):
		self.file = open("items.js","wb")

	def process_item(self, item, spider):
		item_file = open("items/%s" % item['url'],"wb")
		line = json.dumps(dict(item)) 
		file.write(line)
		file.close()
		return item
