from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

class Like(db.Model):
	__tablename__ = "likes"
	liker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	liked_id = db.Column(db.Integer, db.ForeignKey('incidence.id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(), nullable=False)
	number = db.Column(db.Integer(), nullable=False)
	gender = db.Column(db.String(), nullable=False)
	password = db.Column(db.String(), nullable=False)
	profile_image = db.Column(db.String(), nullable=False, default="default.jpg")
	user_type = db.Column(db.String(), nullable=False, default="citizen")
	date_joined = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
	incidence = db.relationship("Incidence", backref="author", lazy=True)
	safe = db.relationship("Safe", backref="marker", lazy=True)

	liked = db.relationship('Like', foreign_keys=[Like.liker_id],\
		backref=db.backref('liker', lazy='joined'), lazy='dynamic',\
		cascade='all, delete-orphan')

	def __repr__(self):
		return f" {self.name}, {self.number}, {self.profile_image}, {self.date_joined}"

	def like(self, user):
		if not self.is_liking(user):
			f = Like(liker=self, liked=user)
			db.session.add(f)

	def unlike(self, user):
		f = self.liked.filter_by(liked_id=user.id).first()
		if f:
			db.session.delete(f)

	def is_liking(self, user):
		return self.liked.filter_by(
			liked_id=user.id).first() is not None

class Incidence(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(), nullable=False)
	location = db.Column(db.String(), nullable=False)
	date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	safes = db.relationship("Safe", backref="marked_incidence", lazy=True)

	likers = db.relationship('Like', foreign_keys=[Like.liked_id],\
		backref=db.backref('liked', lazy='joined'), lazy='dynamic',\
		cascade='all, delete-orphan')

	def is_liked_by(self, pst):
		return self.likers.filter_by(
			liker_id=pst.id).first() is not None

	def __repr__(self):
		return f" {self.name}, {self.date_added}"

class Safe(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	incidence_id = db.Column(db.Integer, db.ForeignKey('incidence.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)