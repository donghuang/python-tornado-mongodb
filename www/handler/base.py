#!/usr/bin/env python
#coding:utf-8

import sys,re,markdown
reload(sys)
sys.setdefaultencoding('utf-8') 
from tornado import web
from model.models import *
from mongoengine import *

_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')


Categorys=dict(
	bigdata='大数据',
	datadev='数据开发',
	python='Python',
	shell='Shell',
	spitslot='吐槽',
	)
ITNUM=3

class BaseHandler(web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("username")

class HomeHandler(BaseHandler):
	def get(self,pn=1):
		pn=int(pn)
		search = self.get_argument('search',None)
		if search:
			pn=int(self.get_argument('page',1))
			blogs=Blog.objects(Q(title__contains=search)|Q(content__contains=search))
			searchcnt=len(blogs)
			blogs=blogs[(pn-1)*ITNUM:(pn-1)*ITNUM+ITNUM]
			for blog in blogs:
				blog.content=markdown.markdown(blog.content)[0:100]
			self.render('search.html',cookieName=self.current_user,blogs=blogs,pn=pn,search=search,searchcnt=searchcnt)
		else:
			blogs=Blog.objects()[(pn-1)*ITNUM:(pn-1)*ITNUM+ITNUM]
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
		self.set_secure_cookie("username", username)
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
			self.set_secure_cookie("username", username)
			self.redirect('/')

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
			blog and self.render('editblog.html',cookieName=self.current_user,blog=blog,pn=None,blogs=None)
		elif method=='del' and blogid is not None:
			blog=Blog.objects(blogid=blogid)[0]
			blog.delete()
			self.redirect('/mangeblog')
		else:
			self.render('editblog.html',cookieName=self.current_user,blogs=None,blog=None)

	def post(self,method=None,blogid=None):
		category=self.get_argument('category',None)
		categorydesc=Categorys[category]
		blogtitle=self.get_argument('blogtitle',None)
		blogcontent=self.get_argument('blogcontent',None)
		blogauthor=self.get_argument('blogauthor',None)
		if not blogauthor:
			blogauthor=self.current_user
		if method=='update':
			blog=Blog.objects(blogid=blogid)[0]
			blog.title=blogtitle
			blog.content=blogcontent
			blog.author=blogauthor
			blog.category=category
			blog.categorydesc=categorydesc
			blog.update_time=datetime.datetime.now
			blog.save()
			self.redirect('/mangeblog')
		else:
			if blogtitle and blogcontent:
				blogid=int(Blog.objects.exec_js('getNextSequence("id")'))
				blog=Blog(blogid=blogid,
					title=blogtitle,
					content=blogcontent,
					author=blogauthor,
					category=category,
					categorydesc=categorydesc
					)
				user=User.objects(name=self.current_user)[0]
				blog.user=user
				blog.save()
				self.redirect("/")
		self.render('editblog.html',cookieName=self.current_user,blogs=None,blog=None)

class MangeblogHandler(BaseHandler):
	def get(self):
		user=User.objects(name=self.current_user)[0]
		blogs=Blog.objects(user=user.id)
		for blog in blogs:
			blog.content=blog.content[0:90]
		self.render('mangeblog.html',cookieName=self.current_user,blogs=blogs)

class CategorygHandler(BaseHandler):
	def get(self,category=None,pn=1):
		pn=int(pn)
		if category is None:
			self.redirect('/')
		if category in Categorys:
			blogs=Blog.objects(category=category)[(pn-1)*ITNUM:(pn-1)*ITNUM+ITNUM]
			for blog in blogs:
				blog.content=markdown.markdown(blog.content)[0:100]
			self.render('category.html',cookieName=self.current_user,blogs=blogs,pn=pn,category=category)
		else:
			self.render('category.html',cookieName=self.current_user,blogs=None,pn=pn,category=category)

class CommentHandler(BaseHandler):
	def post(self,blogid=None):
		blog=Blog.objects(blogid=blogid)[0]
		commentcontent=self.get_argument('commentcontent',None)
		username = self.current_user or '路人'
		if not username or not commentcontent:
			self.redirect('/blog/'+blogid)
		comment=Comments(content=commentcontent,username=username)
		comment.save()
		blog.comments.insert(0,comment)
		blog.save()
		self.redirect('/blog/'+blogid)