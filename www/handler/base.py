#!/usr/bin/env python
#coding:utf-8

import sys,re
reload(sys)
sys.setdefaultencoding('utf-8') 
from tornado import web
from model.models import User

_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')


class BaseHandler(web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("username")

class IndexHandler(BaseHandler):
	
	def get(self):
		self.render('index.html',cookieName=self.current_user)


class LoginHandler(BaseHandler):
	def get(self):
		self.render('login.html',msg=None)

	def post(self):
		username=self.get_argument('username',None)
		password=self.get_argument('password',None)
		reg_user=User.objects(name=username) or User.objects(email=username)

		if reg_user:
			if reg_user[0].password==password:
				self.set_secure_cookie("username", username)
				self.render('index.html',cookieName=username)
			else:
				self.render('login.html',msg='密码错误')
		else:
			self.render('login.html',msg='用户名/邮箱不存在')


class RegisterHandler(BaseHandler):
	
	def get(self):
		self.render('register.html',msg=None)

	def post(self):
		msg=None

		username=self.get_argument('username',None)
		email=self.get_argument('email',None)
		password=self.get_argument('password',None)
		password2=self.get_argument('password2',None)

		if User.objects(name=username):
			msg = ' 用户名'
		if User.objects(email=email):
			msg = msg and msg +' 邮箱' or ' 邮箱'
		if msg:
			msg = msg +'已被占用'
			self.render('register.html',msg=msg)
		else:
			user=User(name=username,email=email,password=password)
			user.save()
			self.set_secure_cookie("username", username)
			self.render('index.html',cookieName=username)

class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("username")
		self.redirect("/")
