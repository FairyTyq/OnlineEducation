# coding:utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# 注意这里不再传app了，为什么？
# 因为要根据配置动态创建Flask app，官方推荐做法是使用一个工厂函数专门负责创建app
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True,index=True,nullable=False)
    publish_courses = db.relationship('Course')
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),unique=True,index=True,nullable=False)
    # ondelete='CASCASE' 表示如果用户被删除了，那么作者是他的课程也会被及联删除
    author_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    author = db.relationship('User',uselist=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow())
    updated_at = db.Column(db.DateTime,default=datetime.utcnow(),onupdate=datetime.utcnow)
