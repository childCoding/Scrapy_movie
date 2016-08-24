#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cgi
import MySQLdb as mdb
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def mysql_select(id):
	db = mdb.connect("localhost","root","carlos940413","scrapymovie",charset='utf8')
	cursor = db.cursor()
	sql = "select * from movie where id=%s" % id

	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			result_dict = {}
			result_dict[u'state'] = "success"
			result_dict[u'type'] = row[1]
#			result_dict[u'date'] = row[2]
			result_dict[u'title'] = row[3]
			result_dict[u'content'] = row[4]
			result_dict[u'url'] = row[5]
#			print row
			detail = json.dumps(result_dict,ensure_ascii=False)
			return detail
	except mdb.Error,e:
		return "db error:%s" % str(e)

	db.close()


header = "Content-Type:text/html;charset=utf-8\r\n"

form = cgi.FieldStorage()

id = form.getvalue('id')

print header

if id:
	print mysql_select(id)
else:
	print json.dumps({"state":"failure","msg":"参数不足！"},ensure_ascii=False)
