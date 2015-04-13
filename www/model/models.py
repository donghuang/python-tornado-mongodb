# -*- coding: utf-8 -*-
import datetime
from mongoengine import *

class User(Document):
    name = StringField(max_length=50, required=True)
    password = StringField()
    email = StringField()
    avatar = StringField()
    signature = StringField()
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    meta = {'db_alias': 'blogdb'}


class Diary(Document):
    title = StringField(required=True)
    old_id = IntField()
    content = StringField()
    summary = StringField()
    html = StringField()
    category = StringField(default=u'未分类')
    author = ReferenceField(User)
    tags = SortedListField(StringField())
    comments = SortedListField(EmbeddedDocumentField('CommentEm'))
    publish_time = DateTimeField(default=datetime.datetime.now, required=True)
    update_time = DateTimeField(default=datetime.datetime.now, required=True)

    meta = {'allow_inheritance': True}


class Photo(Document):
    url = StringField(required=True)
    title = StringField(required=True)
    album_name = StringField(default=u'未分类')
    description = StringField()
    publish_time = DateTimeField(default=datetime.datetime.now, required=True)


class Tag(Document):
    name = StringField(max_length=120, required=True)
    diaries = SortedListField(ReferenceField(Diary))
    publish_time = DateTimeField(default=datetime.datetime.now, required=True)


class Category(Document):
    name = StringField(max_length=120, required=True)
    diaries = SortedListField(ReferenceField(Diary))
    publish_time = DateTimeField(default=datetime.datetime.now, required=True)


class Comment(Document):
    content = StringField(required=True)
    author = StringField(max_length=120, required=True)
    email = EmailField()
    diary = ReferenceField(Diary)
    publish_time = DateTimeField(default=datetime.datetime.now, required=True)


class Page(Document):
    url = StringField(required=True, unique=True)
    title = StringField(required=True)
    content = StringField()
    summary = StringField()
    html = StringField()
    author = ReferenceField(User)
    comments = SortedListField(EmbeddedDocumentField('CommentEm'))
    publish_time = DateTimeField(default=datetime.datetime.now, required=True)
    update_time = DateTimeField(default=datetime.datetime.now, required=True)

    meta = {'allow_inheritance': True}


class StaticPage(Page):
    pass


class CommentEm(EmbeddedDocument):
    content = StringField(required=True)
    author = StringField(max_length=120, required=True)
    email = EmailField()
    publish_time = DateTimeField(default=datetime.datetime.now, required=True)

if __name__ == '__main__':
    user=User(name='dh',created_at='aa')
