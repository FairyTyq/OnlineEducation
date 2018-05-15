# coding:utf-8

import re
import json

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms import TextAreaField,IntegerField
from wtforms.validators import Length,Email,EqualTo,Required,URL,NumberRange
from wtforms import ValidationError
from simpledu.models import User,Course,Live,db
from .handlers.ws import redis

class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[Required(),Length(3,24)])
    email = StringField('邮箱',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    submit = SubmitField('提交')
    
    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')
        if not re.match(r'^[a-zA-Z0-9]{3,24}$',field.data):
            raise ValidationError('请输入3至24位字母或者数字')

    
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

        
class LoginForm(FlaskForm):
    #email = StringField('邮箱',validators=[Required(),Email()])
    username = StringField('Username',validators=[Required(),Length(3,24)])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')
    
    def validate_email(self,field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名不存在')

    def validate_password(self,field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class CourseForm(FlaskForm):
    name = StringField('Course Name',validators=[Required(),Length(5,32)])
    description = TextAreaField('Course Introduction',validators=[Required(),Length(20,256)])
    image_url = StringField('Cover Image',validators=[Required(),URL()])
    author_id = IntegerField('Author ID',validators=[Required(),NumberRange(min=1,message='Invalid ID')])
    submit = SubmitField('Submit')

    def validate_author_id(self,field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('User does not exist')

    def create_course(self):
        course = Course()
        # fill course object with courseform data
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self,course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course


class UserForm(FlaskForm):
    username = StringField('User Name',validators=[Required(),Length(3,24)])
    email = StringField('Email',validators=[Required(),Email()])
    password = StringField('PassWord',validators=[Required(),Length(3,24)])
    job = StringField('Job',validators=[Required(),Length(3,64)]) 
    role = IntegerField('Role',validators=[Required(),NumberRange(min=10,max=30,message='Invalid role')])
    submit = SubmitField('Submit')

    def update_user(self,user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


class LiveForm(FlaskForm):
    name = StringField('Live Name',validators=[Required(),Length(3,24)])
    user_id = IntegerField('User ID',validators= [Required(),NumberRange(min=1,message="ïnvalid ID")])
    submit = SubmitField('Submit')

    def update_live(self,live):
        pass

    def create_live(self):
        live = Live()
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live



class MessageForm(FlaskForm):
    msg = TextAreaField('System Message',validators=[Required(),Length(1,256)])
    submit = SubmitField('Submit')

    def send_msg(self):
        redis.publish(
            'chat',
            json.dumps(dict(
            username='System',
            text=str(self.msg.data)
            )))
