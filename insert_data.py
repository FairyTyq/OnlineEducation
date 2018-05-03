from simpledu.models import db,User,Course

def insert():
    db.create_all()
    user = User(username='admin')
    course1 = Course(name='python course',author=user)
    course2 = Course(name='flask course',author=user)
    db.session.add(user)
    db.session.add(course1)
    db.session.add(course2)
    db.session.commit()
