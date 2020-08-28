from app import app, db
from flask import redirect, url_for, render_template, request, jsonify, flash
from flask_login import current_user, logout_user

from app.models import Incidence, User, Notifications
from datetime import datetime
import secrets

@app.route('/')
def home():
	if current_user.is_authenticated:
		if current_user.account_pend == True:
			logout_user()
			flash("This account has been suspended for 15 days By an Admin, for \
				Reasons best known to him, Please comply.")
			return redirect(url_for('login'))
		citizens = User.query.filter_by(user_type="citizen").order_by(User.date_joined.desc())\
			.all()
		admins = User.query.filter_by(user_type="it_admin").order_by(User.date_joined.desc())\
			.all()
		incidence = Incidence.query.order_by(Incidence.date_added.desc()).all()
		return render_template('user/home.html', incidence=incidence, citizens=citizens,\
			admins=admins)
	else:
		return redirect(url_for('login'))


@app.route('/profile')
def profile():
	if current_user.is_authenticated:
		return render_template('user/profile.html')
	else:
		return redirect(url_for('login'))

@app.route('/edit/profile')
def edit_profile():
	if current_user.is_authenticated:
		return render_template('user/edit_profile.html')
	else:
		return redirect(url_for('login'))

@app.route('/u/<id>'+'wsdfni')
def others_profile(id):
	if current_user.is_authenticated:
		user = User.query.get_or_404(id)
		if user == current_user:
			return redirect(url_for('profile'))
		users_post = Incidence.query.filter_by(author=user).all()
		return render_template('user/others_profile.html', user=user, users_post=users_post)
	else:
		return redirect(url_for('login'))

@app.route('/post/<id>')
def single_post(id):
	if current_user.is_authenticated:
		incidence = Incidence.query.get_or_404(id)
		return render_template('posts/single_post.html', incidence=incidence)
	else:
		return redirect(url_for('login'))


@app.route('/alerts')
def alerts():
	notify = Notifications.query.filter_by(reciever_id=current_user.id).all()
	return render_template('alert/notify.html', notify=notify)