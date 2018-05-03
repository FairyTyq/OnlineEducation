# coding =utf-8

from flask import Blueprint,render_template
from simpledu.models import Course,User

user = Blueprint('user',__name__,url_prefix='/user')

@user.route('/<user_name>')
def index(user_name):
    usr = User.query.filter(User.username==user_name).first()
    return render_template('user.html',usr=usr)


