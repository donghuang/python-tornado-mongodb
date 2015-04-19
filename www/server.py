#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
项目的入口文件，里面包含if __name__ == "__main__"，从这里启动项目和服务
'''
import sys
import tornado.ioloop
import tornado.options
import tornado.httpserver

from application import application
from tornado.options import define,options
from mongoengine import *

define("port",default=8000,help="run on th given port",type=int)


#define("MogoClietn",default=connect(db='blogdb',alias='blogdb',host='192.168.182.80',port=27017,username='blogetl',password='blogetl'))
MogoClient=connect(db='blogdb',alias='blogdb',host='192.168.182.80',port=27017,username='blogetl',password='blogetl')

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print 'Development server is running at http://127.0.0.1:%s/' % options.port
    print 'Quit the server with Control-C'
    tornado.ioloop.IOLoop.instance().start()

if __name__=="__main__":
    main()