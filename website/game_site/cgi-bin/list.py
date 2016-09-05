#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cgi
import MySQLdb as mdb
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def mysql_select(ty,page = 0):
	db = mdb.connect("localhost","root","carlos_940413","scrapymovie",charset='utf8')
	cursor = db.cursor()
	sql = r"select id,icon,type,date,title from movie where type='%s' order by date desc limit %d,%d" % (ty,page*10,10)

	try:
		result_dict = {}
		result_dict[u'state'] = "success"
		result_dict[u'list'] = []
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			ele = {}
			ele[u'id'] = row[0]
			ele[u'icon'] = row[1]
			ele[u'type'] = row[2]
			ele[u'date'] = unicode(row[3])
			ele[u'title'] = row[4]
#			ele[u'content'] = row[4]
#			ele[u'url'] = row[5]
			result_dict[u'list'].append(ele)
		detail = json.dumps(result_dict,ensure_ascii=False)
		return detail
	except mdb.Error,e:
		return "db error:%s" % str(e)

	db.close()


header = "Content-Type:text/html;charset=utf-8\r\n"

form = cgi.FieldStorage()

ty = form.getvalue('type')
page = form.getvalue('page',0)

print header

if ty and page:
	print mysql_select(ty,int(page))
else:
	print json.dumps({"state":"failure","msg":"参数不足！"},ensure_ascii=False)


