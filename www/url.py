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
    (r'/',IndexHandler),
    (r'/login',LoginHandler),
    (r'/register',RegisterHandler),
    (r'/logout',LogoutHandler),
    ]
