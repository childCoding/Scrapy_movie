#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cgi
import MySQLdb as mdb
import json
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


def mysql_select(id):
	db = mdb.connect("localhost","root","carlos_940413","scrapymovie",charset='utf8')
	cursor = db.cursor()
	sql = "select id,icon,type,date,title,content,url from movie where id=%s" % id
	result = ""
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			result_dict = {}
			result_dict[u'state'] = "success"
			result_dict[u'icon'] = row[1]
			result_dict[u'type'] = row[2]
			result_dict[u'date'] = unicode(row[3])
			result_dict[u'title'] = row[4]
			result_dict[u'content'] = row[5]
			result_dict[u'url'] = row[6]
#			print row
			result = json.dumps(result_dict,ensure_ascii=False)
	except mdb.Error,e:
		result = "db error:%s" % str(e)
	
	db.close()
	return result;	

header = "Content-Type:text/html;charset=utf-8\r\n"

form = cgi.FieldStorage()

id = form.getvalue('id')

print header

if id:
	print mysql_select(id)
else:
	print json.dumps({"state":"failure","msg":"参数不足！"},ensure_ascii=False)
