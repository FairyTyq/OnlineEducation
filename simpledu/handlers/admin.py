# coding=utf-8

from flask import Blueprint,render_template
from flask import redirect,url_for,flash
from flask import request,current_app
from simpledu.decorators import admin_required
from simpledu.models import Course,User,Live
from simpledu.forms import CourseForm,UserForm,LiveForm,db

admin = Blueprint('admin',__name__,url_prefix='/admin')

# 注意路由和函数名的变化
@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/courses')
@admin_required
def courses():
	page = request.args.get('page',default=1,type=int)
	pagination = Course.query.paginate(
			page = page,
			per_page = current_app.config['ADMIN_PER_PAGE'],
			error_out = False
		)
	return render_template('admin/courses.html',pagination=pagination)

@admin.route('/course/create',methods=['GET','POST'])
@admin_required
def create_course():
	form = CourseForm()
	if form.validate_on_submit():
		form.create_course()
		flash('Create course successfully','success')
		return redirect(url_for('admin.courses'))
	return render_template('admin/create_course.html',form=form)

@admin.route('/course/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
	course = Course.query.get_or_404(course_id)
	db.session.delete(course)
	db.session.commit()
	flash('Delete course successfully','success')
	return redirect(url_for('admin.courses'))

@admin.route('/courses/<int:course_id>/edit',methods=['GET','POST'])
@admin_required
def edit_course(course_id):
	course = Course.query.get_or_404(course_id)
	form = CourseForm(obj=course)
	if form.validate_on_submit():
		form.update_course(course)
		flash('Update Course Successfully!','success')
		return redirect(url_for('admin.courses'))
	return render_template('admin/edit_course.html',form=form,course=course)

@admin.route('/users')
@admin_required
def users():
	page = request.args.get('page',default=1,type=int)
	pagination = User.query.paginate(
			page = page,
			per_page = current_app.config['ADMIN_PER_PAGE'],
			error_out = False
		)
	return render_template('admin/users.html',pagination=pagination)

@admin.route('/users/create',methods=['GET','POST'])
@admin_required
def create_user():
	form = UserForm()
	if form.validate_on_submit():
		form.create_user()
		flash('Create User Successfully','success')
		return redirect(url_for('admin.users'))
	return render_template('admin/create_users.html',form=form)

@admin.route('/users/<int:user_id>/edit',methods=['GET','POST'])
@admin_required
def edit_user(user_id):
	user = User.query.get_or_404(user_id)
	form = UserForm(obj=user)
	if form.validate_on_submit():
		form.update_user(user)
		flash('Update User Successfully!','success')
		return redirect(url_for('admin.users'))
	return render_template('admin/edit_user.html',form=form,user=user)

@admin.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
	user = User.query.get_or_404(user_id)
	db.session.delete(user)
	db.session.commit()
	flash('Delete User Successfully!','success')
	return redirect(url_for('admin.users'))


@admin.route('/live')
@admin_required
def lives():
	page = request.args.get('page',default=1,type=int)
	pagination = Live.query.paginate(
			page = page,
			per_page = current_app.config['ADMIN_PER_PAGE'],
			error_out = False
		)
	return render_template('admin/lives.html',pagination=pagination)

@admin.route('/live/create',methods=['GET','POST'])
@admin_required
def create_live():
	form = LiveForm()
	if form.validate_on_submit():
		form.create_live()
		flash('Create Live Successfully!','success')
		return redirect(url_for('admin.lives'))
	return render_template('admin/create_live.html',form=form)


@admin.route('/live/<int:live_id>/edit',methods=['GET','POST'])
@admin_required
def edit_live(live_id):
	pass

@admin.route('/live/<int:live_id>/delete')
@admin_required
def delete_live(live_id):
	pass