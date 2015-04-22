#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
记录项目中所有URL和映射的类，即完成handlers=[...]的功能
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from handler.base import *

url=[
    (r'/',HomeHandler),
    (r'/page/([0-9]+)',HomeHandler),
    (r'/login',LoginHandler),
    (r'/register',RegisterHandler),
    (r'/logout',LogoutHandler),
    (r'/add',BlogeditHandler),
    (r'/(edit|blog|del|update)/([0-9]+)',BlogeditHandler),
    (r'/mangeblog',MangeblogHandler),
    (r'/categorys/([a-z]+)',CategorygHandler),
    (r'/categorys/([a-z]+)/([0-9]+)',CategorygHandler),
    (r'/posts/comments/([0-9]+)',CommentHandler),
    ]
