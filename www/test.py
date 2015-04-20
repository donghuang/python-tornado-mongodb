#!/usr/bin/env python
# -*- coding: utf-8 -*-
#============================================
# @Date        : 2015-01-06 20:12:48
# @Author      : dh (huang081112@126.com)
# @Link        : https://github.com/donghuang
# @Version     : 1.1
# @Description :
#============================================

import tornado.httpserver   
import tornado.ioloop   
import tornado.options   
import tornado.web   
from tornado.options import define, options   
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):   
    def get(self):   
        greeting = self.get_argument('greeting', 'Hello')
        fuck = self.get_argument('fuck', 'love')      
        self.write(greeting + ', friendly user!  ' + fuck)

if __name__ == "__main__":   
    tornado.options.parse_command_line()   
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])   
    http_server = tornado.httpserver.HTTPServer(app)   
    http_server.listen(options.port)   
    tornado.ioloop.IOLoop.instance().start()