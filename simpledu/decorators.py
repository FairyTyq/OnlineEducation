from flask import abort
from flask_login import current_user
from functools import wraps
from simpledu.models import User

def role_required(role):
	"""
	only the specified role can visit the route that be decorated by this decorator
	Example:
		@role_required(User.ADMIN)
		def admin():
			pass
	"""
	def decorator(func):
		@wraps(func)
		def wrapper(*args,**kwrargs):
			# user who did not login or be the wrong role trigger 404
			if not current_user.is_authenticated or current_user.role < role:
				abort(404)
			return func(*args,**kwrargs)
		return wrapper
	return decorator

# 
staff_required = role_required(User.ROLE_STAFF)
admin_required = role_required(User.ROLE_ADMIN)