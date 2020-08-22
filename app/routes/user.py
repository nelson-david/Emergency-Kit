from app import app, db
from flask import redirect, url_for, render_template, request, jsonify
from flask_login import current_user

from app.models import Incidence, User

@app.route('/')
@app.route('/home')
def home():
	if current_user.is_authenticated:
		citizens = User.query.filter_by(user_type="citizen").order_by(User.date_joined.desc()).all()
		admins = User.query.filter_by(user_type="it_admin").order_by(User.date_joined.desc()).all()
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

@app.route('/update_profile', methods=['POST'])
def update_profile():
	if current_user.is_authenticated:
		current_user.name = request.form['name']
		current_user.number = request.form['number']
		db.session.commit()
		return jsonify({'success':'true'})
	else:
		return redirect(url_for('login'))

@app.route('/add_incidence', methods=['POST'])
def add_incidence():
	if current_user.is_authenticated:
		new_incidence = Incidence(name=request.form['name'], location=request.form['location'],\
			author=current_user)
		db.session.add(new_incidence)
		db.session.commit()
		return jsonify({'successs':'true'})
	else:
		return redirect(url_for('login'))