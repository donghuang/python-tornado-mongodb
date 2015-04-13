#!/usr/bin/env python
# -*- coding: utf-8 -*-
#============================================
# @Date        : 2015-01-06 20:12:48
# @Author      : dh (huang081112@126.com)
# @Link        : https://github.com/donghuang
# @Version     : 1.1
# @Description :
#============================================

import os
from tornado import web,httpserver,ioloop
from tornado.options import options,define
from mongoengine import *
from mongoengine.connection import connect,get_db
connect(db='blogdb',alias='blogdb',host='192.168.182.80',port=27017,username='blogetl',password='blogetl')

import datetime

class Page(DynamicDocument):  
    title = StringField(max_length=200, required=True)
    meta = {"db_alias": "blogdb"}

page = Page(title='DONGHUANG1')  

page.save()
print '=====ok======'

page1=Page.objects(title='DONGHUANG1111') or Page.objects(title='DONGHUANG1111')
print page1

define('port',default=8000,help="run on the given port",type=int)

class LoginHandler(web.RequestHandler):
	def get(self):
		self.render('login.html')

	def post(self):
		name=self.get_argument('username')
		pw=self.get_argument('password')
		res=check(name)
		if res:
			self.redirect('/register')
		else:
			insert(name,pw)
			self.set_cookie('hackerName',name)
			self.redirect('/')

class RegisterHandler(web.RequestHandler):
	def get(self):
		self.render('register.html')

	def post(self):
		name=self.get_argument('username')
		pw=self.get_argument('password')
		res=check(name)
		if res:
			self.redirect('/register')
		else:
			insert(name,pw)
			self.set_cookie('hackerName',name)
			self.redirect('/')

if __name__ == '__main__':
	options.parse_command_line()
	app = web.Application(
		handlers=[(r'/login',LoginHandler),(r'/register',RegisterHandler)],
		static_path=os.path.join(os.path.dirname(__file__),'static'),
		template_path=os.path.join(os.path.dirname(__file__),'template'),
		debug=True
		)
	httpserver.HTTPServer(app).listen(options.port)
	ioloop.IOLoop.instance().start()