#!/usr/bin/env python
#coding:utf-8

import sys,re
reload(sys)
sys.setdefaultencoding('utf-8') 
from tornado import web
from model.models import User

_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')


class IndexHandler(web.RequestHandler):
	def get(self):
		name=self.get_cookie('hackerName')
		#blogs='a'
		#self.render('index.html',cookieName=name,blogs=blogs)
		self.render('index.html',cookieName=name)
	def post(self):
		name=self.get_argument('username')
		pw=self.get_argument('password')
		res=check(name,pw)
		if res: #密码正确
			self.set_cookie('hackerName',name)
		else: #密码错误
			pass
		self.redirect('/')

class LoginHandler(web.RequestHandler):
	def get(self):
		self.render('login.html')

	def post(self):
		username=self.get_argument('username',None)
		password=self.get_argument('password',None)


class RegisterHandler(web.RequestHandler):
	def get(self):
		self.render('register.html')

	def post(self):
		username=self.get_argument('username',None)
		email=self.get_argument('email',None)
		password=self.get_argument('password',None)
		password2=self.get_argument('password2',None)
		user=User(name=username,email=email,password=password)
		user.save()
		user=User.objects(name=username)
		user=User.objects(email=email)
		if user:
			self.write('already exists')
