# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
import scrapy
from scrapy.item import Item, Field

class TutorialItem(Item):
    # define the fields for your item here like:
    # name = Field()
	type = scrapy.Field()
	title = scrapy.Field()
	icon = scrapy.Field()
	issue_date = scrapy.Field()
	content = scrapy.Field()
	download_url = scrapy.Field()
	image_urls = scrapy.Field()
	images = scrapy.Field()
	origin = scrapy.Field()
