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


define('port',default=8000,help="run on the given port",type=int)

class LoginHandler(web.RequestHandler):
	def get(self):
		#self.write('xxxx')
		self.render('test.html',action='action',redirect='redirect')



class VueModule(web.UIModule):
	def render(self):
		return self.render_string('test.html')



if __name__ == '__main__':
	options.parse_command_line()
	app = web.Application(
		handlers=[(r'/',LoginHandler),],
		static_path=os.path.join(os.path.dirname(__file__),'static'),
		template_path=os.path.join(os.path.dirname(__file__),'template'),
		ui_modules={'vuemodule': VueModule},
		autoescape=None,
		debug=True
		)
	httpserver.HTTPServer(app).listen(options.port)
	ioloop.IOLoop.instance().start()