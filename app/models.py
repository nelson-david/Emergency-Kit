from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

class Marking(db.Model):
	__tablename__ = "marking"
	marker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	marked_id = db.Column(db.Integer, db.ForeignKey('incidence.id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(), nullable=False)
	number = db.Column(db.Integer(), nullable=False)
	gender = db.Column(db.String(), nullable=False)
	password = db.Column(db.String(), nullable=False)
	profile_image = db.Column(db.String(), nullable=False, default="default.jpg")
	user_type = db.Column(db.String(), nullable=False, default="citizen")
	location = db.Column(db.String(), nullable=True)
	date_joined = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
	account_pend = db.Column(db.Boolean(), nullable=True)
	date_pended = db.Column(db.DateTime(), nullable=True)
	incidence = db.relationship("Incidence", backref="author", lazy=True)
	safe = db.relationship("Safe", backref="marker", lazy=True)
	comment = db.relationship("Comment", backref="comm_ent", lazy=True)
	message_sent = db.relationship("Message", backref="author", lazy=True)

	marked = db.relationship('Marking', foreign_keys=[Marking.marker_id],\
		backref=db.backref('liker', lazy='joined'), lazy='dynamic',\
		cascade='all, delete-orphan')

	notify_carrier = db.relationship('Notifications',\
		foreign_keys='Notifications.carrier_id',\
		backref='n_carrier', lazy='dynamic')
	notify_reciever = db.relationship('Notifications',\
		foreign_keys='Notifications.reciever_id',\
		backref='n_reciever', lazy='dynamic')

	def __repr__(self):
		return f" {self.name}, {self.number}, {self.profile_image}, {self.date_joined}"

	def mark(self, user):
		if not self.is_marking(user):
			f = Marking(marker=self, marked=user)
			db.session.add(f)

	def unmark(self, user):
		f = self.marked.filter_by(marked_id=user.id).first()
		if f:
			db.session.delete(f)

	def is_marking(self, user):
		return self.marked.filter_by(
			marked_id=user.id).first() is not None

class Incidence(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(), nullable=False)
	location = db.Column(db.String(), nullable=False)
	date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	safes = db.relationship("Safe", backref="marked_incidence", lazy=True)
	comments = db.relationship("Comment", backref="commenter", lazy=True)

	markers = db.relationship('Marking', foreign_keys=[Marking.marked_id],\
		backref=db.backref('marked', lazy='joined'), lazy='dynamic',\
		cascade='all, delete-orphan')

	def is_marked_by(self, pst):
		return self.markers.filter_by(
			marker_id=pst.id).first() is not None

	def __repr__(self):
		return f" {self.name}, {self.date_added}"

class Safe(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	incidence_id = db.Column(db.Integer, db.ForeignKey('incidence.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)


class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	def __repr__(self):
		return f'<Message {self.body}>'


class Notifications(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	carrier_name = db.Column(db.String(50))
	carrier_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	reciever_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	action_type = db.Column(db.String(140))
	date_carried = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	incidence_id = db.Column(db.Integer, db.ForeignKey('incidence.id'), nullable=False)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return f'<Message {self.body}>'