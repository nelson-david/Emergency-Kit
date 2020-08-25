from app import app, db
from flask import redirect, url_for, request, jsonify
from flask_login import current_user
from app.models import Incidence, Safe, User, Notifications

from datetime import datetime
import secrets
import os
from PIL import Image

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
		all_user = User.query.all()
		for users in all_user:
			new_notify = Notifications(carrier_name=current_user.name, carrier_id=current_user.id,\
				reciever_id=users.id,\
				action_type="incidence")
			db.session.add(new_notify)
			db.session.commit()
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

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
	i = Image.open(form_picture)
	i.save(picture_path)
	return picture_fn

@app.route("/update_photo",  methods=['POST'])
def update_photo():
	picture_file = save_picture(request.files.get('file'))
	print(picture_file)
	current_user.profile_image = picture_file
	db.session.commit()

	return jsonify({'success' : 'true', 'like_num' : 3})

@app.route("/remove_photo",  methods=['POST'])
def remove_photo():
	current_user.profile_image = "default.jpg"
	db.session.commit()
	return jsonify({'success' : 'true', 'like_num' : 3})