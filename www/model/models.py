# -*- coding: utf-8 -*-
import datetime
from mongoengine import *
from bson import ObjectId

class User(Document):
    name = StringField(max_length=50, required=True)
    password = StringField()
    email = StringField()
    avatar = StringField()
    signature = StringField()
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    meta = {'db_alias': 'blogdb'}

class Comments(Document):
    content = StringField(required=True)
    username = StringField(max_length=120, required=True)
    publish_time = DateTimeField(default=datetime.datetime.now, required=True)
    meta = {
        'db_alias': 'blogdb',
        'ordering': ['-publish_time']
    }

class Blog(Document):
    blogid=IntField(primary_key=True)
    title = StringField(required=True)
    content = StringField()
    summary = StringField()
    html = StringField()
    category = StringField(default=u'unknow')
    categorydesc = StringField(default=u'未分类')
    user=ReferenceField(User)
    author = StringField()
    tags = SortedListField(StringField())
    comments = ListField(ReferenceField(Comments))
    #comments = SortedListField(EmbeddedDocumentField('Comments'))
    publish_time = DateTimeField(default=datetime.datetime.now, required=True)
    update_time = DateTimeField(default=datetime.datetime.now, required=True)
    meta = {'db_alias': 'blogdb',
            'ordering': ['-publish_time']
            }


