from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

from datetime import datetime

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(), nullable=False)
	number = db.Column(db.Integer(), nullable=False)
	gender = db.Column(db.String(), nullable=False)
	password = db.Column(db.String(), nullable=False)
	profile_image = db.Column(db.String(), nullable=False, default="default.jpg")
	date_joined = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
	incidence = db.relationship("Incidence", backref="author", lazy=True)
	safe = db.relationship("Safe", backref="marker", lazy=True)

	def __repr__(self):
		return f" {self.name}, {self.number}, {self.profile_image}, {self.date_joined}"

class Incidence(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(), nullable=False)
	location = db.Column(db.String(), nullable=False)
	date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	safes = db.relationship("Safe", backref="marked_incidence", lazy=True)

	def __repr__(self):
		return f" {self.name}, {self.date_added}"

class Safe(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	incidence_id = db.Column(db.Integer, db.ForeignKey('incidence.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)