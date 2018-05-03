# coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringFiled,PasswordField,SubmitField,BooleanField
from wtforms.validators import Length,Email,EqualTo,Required

class RegisterForm(FlaskForm):
    username = StringField('�û���',validators=[Required(),Length(3,24)])
    email = StringField('����',validators=[Required(),Email()])
    password = PasswordField('����',validators=[Required(),Length(6,24)])
    repeat_password = PasswordField('�ظ�����',validators=[Required(),EquaTo('password')])
    submit = SubmitField('�ύ')


class LoginForm(FlaskForm):
    email = StringField('����',validators=[Required(),Email()])
    password = PasswordField('����',validators=[Required(),Length(6,24)])
    remember_me = BooleanField('��ס��')
    submit = SubmitField('�ύ')

