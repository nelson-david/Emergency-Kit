from app import app, db
from flask import redirect, url_for, request, jsonify
from flask_login import current_user
from app.models import Incidence, Safe, User

from datetime import datetime

@app.route("/mark_safe", methods=["POST"])
def mark_safe():
	incidence = Incidence.query.filter_by(id=request.form['incidence_id']).first()
	current_user.like(incidence)
	db.session.commit()

	return jsonify({'success':'true'})

@app.route("/mark_unsafe", methods=["POST"])
def mark_unsafe():
	incidence = Incidence.query.filter_by(id=request.form['incidence_id']).first()
	current_user.unlike(incidence)
	db.session.commit()

	return jsonify({'success':'true'})

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

@app.route('/suspend_user', methods=['POST'])
def suspend_user():
	if current_user.is_authenticated:
		user = User.query.get_or_404(request.form['user_id'])
		user.account_pend = True
		user.date_pended = datetime.utcnow()
		db.session.commit()
		return jsonify({'successs':'true'})
	else:
		return redirect(url_for('login'))

@app.route('/relieve_user', methods=['POST'])
def relieve_user():
	if current_user.is_authenticated:
		user = User.query.get_or_404(request.form['user_id'])
		user.account_pend = False
		db.session.commit()
		return jsonify({'successs':'true'})
	else:
		return redirect(url_for('login'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
	if current_user.is_authenticated:
		current_user.name = request.form['name']
		current_user.number = request.form['number']
		current_user.location = request.form['location']
		db.session.commit()
		return jsonify({'success':'true'})
	else:
		return redirect(url_for('login'))