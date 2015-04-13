#!/usr/bin/env python
# -*- coding: utf-8 -*-
#============================================
# @Date        : 2015-01-06 20:12:48
# @Author      : dh (huang081112@126.com)
# @Link        : https://github.com/donghuang
# @Version     : 1.1
# @Description :
#============================================

from mongoengine.context_managers import switch_db
from mongoengine import *
from mongoengine.connection import connect,get_db
connect(db='blogdb',alias='blogdb',host='192.168.182.80',port=27017,username='blogetl',password='blogetl')
connect(db='blogdb',alias='xx',host='192.168.182.80',port=27017,username='blogetl',password='blogetl')
import datetime

class Page(DynamicDocument):  
    title = StringField(max_length=200, required=True)
    meta = {"db_alias": "blogdb"}



page = Page(title='wu dongqi')  

with switch_db(Page, 'xx') as Page:
    page1=Page(title='gao hui')  
page.save()
page1.save()
print '=====ok======'


class User(Document):
    name = StringField(max_length=50, required=True)
    password = StringField()
    email = StringField()
    avatar = StringField()
    signature = StringField()
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    meta = {'db_alias': 'blogdb'}

user=User(name='ddd')
user.save()