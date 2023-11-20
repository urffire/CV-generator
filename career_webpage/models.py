import json

from flask_login import UserMixin
from sqlalchemy import JSON

from career_webpage import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_data = db.Column(JSON, nullable=True)

    roles = db.relationship('Role', secondary='user_roles')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.roles}')"

    def set_profile_data(self, profile_data):
        self.profile_data = json.dumps(profile_data)

    def get_profile_data(self):
        return json.loads(self.profile_data) if self.profile_data else {}

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
