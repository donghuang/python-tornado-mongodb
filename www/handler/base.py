#!/usr/bin/env python
#coding:utf-8

import sys,re,markdown
reload(sys)
sys.setdefaultencoding('utf-8') 
from tornado import web
from model.models import User,Blog


_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')


class BaseHandler(web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("username")

class HomeHandler(BaseHandler):
	
	def get(self,pn=1):
		pn=int(pn)
		blogs=Blog.objects()[(pn-1)*3:(pn-1)*3+3]
		for blog in blogs:
			blog.content=markdown.markdown(blog.content)[0:100]
		self.render('home.html',cookieName=self.current_user,blogs=blogs,pn=pn,blog=None)


class LoginHandler(BaseHandler):
	def get(self):
		self.render('login.html',msg=None)

	def post(self):
		username=self.get_argument('username',None)
		password=self.get_argument('password',None)
		rememberme=self.get_argument('rememberme',None)
		reg_user=User.objects(name=username) or User.objects(email=username)

		if reg_user:
			if reg_user[0].password==password:
				rememberme and self.set_secure_cookie("username", username)
				blogs=Blog.objects()
				self.redirect('/')
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
			blogs=Blog.objects()
			#self.set_secure_cookie("username", username)
			self.render('home.html',cookieName=username,blogs=blogs,blog=None,pn=None)

class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("username")
		self.redirect("/")

def translate(md):
	for i in whiteList:
		if i[0] in md:
			md=md.replace(i[0],i[1])
	md2=html.escape(md)
	data=markdown2.markdown(md2)
	for i in whiteList:
		if i[1] in data:
			data=data.replace(i[1],i[0])
	return data

class BlogeditHandler(BaseHandler):
	def get(self,method=None,blogid=None):
		if method=='blog' and blogid is not None:
			blog=Blog.objects(blogid=blogid)[0]
			blog.content=markdown.markdown(blog.content)
			blog and self.render('home.html',cookieName=self.current_user,blog=blog,pn=None,blogs=None)
		elif method=='edit' and blogid is not None:
			blog=Blog.objects(blogid=blogid)[0]
			blog.content=blog.content
			blog and self.render('editblog.html',cookieName=self.current_user,blog=blog,pn=None,blogs=None)			
		else:
			self.render('editblog.html',cookieName=self.current_user,blogs=None,blog=None)

	def post(self):
		category=self.get_argument('category',None)
		blogtitle=self.get_argument('blogtitle',None)
		blogcontent=self.get_argument('blogcontent',None)
		blogauthor=self.get_argument('blogauthor',None)
		if blogtitle and blogcontent and blogauthor:
			blogid=int(Blog.objects.exec_js('getNextSequence("id")'))
			blog=Blog(blogid=blogid,title=blogtitle,content=blogcontent,author=blogauthor,category=category)
			blog.save()
		self.render('editblog.html',cookieName=self.current_user,blogs=None,blog=None)

class MangeblogHandler(BaseHandler):
	def get(self):
		blogs=Blog.objects(author=self.current_user)
		for blog in blogs:
			blog.content=blog.content[0:90]
		self.render('mangeblog.html',cookieName=self.current_user,blogs=blogs)
		

		