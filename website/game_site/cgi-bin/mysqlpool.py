#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import MySQLdb
from DBUtils.PooledDB import PooledDB

secret_file = os.path.dirname(__file__) + "/../../../secret.js"
with open(secret_file) as fo:
	secret = json.load(fo)

connect_config = {"host":secret["mysql"]["host"],"user":secret["mysql"]["user"],"passwd":secret["mysql"]["pw"],"db":secret["mysql"]["database"],"port":3306,"charset":"utf8"}
 #5为连接池里的最少连接数
pool = PooledDB(MySQLdb,5,**connect_config) 

def connect():
	return pool.connection()
