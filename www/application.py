#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
核心任务是完成tornado.web.Application()的实例化
'''

from url import url 

import tornado.web
import os

setting = dict(
    template_path=os.path.join(os.path.dirname(__file__),"template"),
    static_path=os.path.join(os.path.dirname(__file__),"static"),
    cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    #xsrf_cookies=True,
    login_url= "/",
    debug = True,
    )

application = tornado.web.Application(
    handlers=url,
    **setting
    )