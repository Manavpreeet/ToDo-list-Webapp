from app.__inti__ import db, login
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(240),index=True, unique=True)
    password_hash = db.Column(db.String(128))
    task = db.relationship('Task', backref='user', lazy='dynamic')
    # completed_task =  db.relationship('CompletedTask', backref='user', lazy='dynamic')

    def __repr__(self):
        return ' <User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def addTask(self, tasks):
        self.task.append(tasks)

    def removeTask(self, tasks):
        self.task.remove(tasks)
    #
    # def completeTask(self, tasks):
    #     self.completed_task.append(tasks)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_complete = db.Column(db.Boolean)

    # def __repr__(self):
    #     return '{}'.format(self.task)
#
# class CompletedTask(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     completed_task = db.Column(db.String(240))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '{}'.format(self.completed_task)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))