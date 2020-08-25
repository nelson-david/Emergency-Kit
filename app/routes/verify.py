from app import app, bcrypt, db
from app.models import User
from flask import render_template, jsonify, request, redirect, url_for

from flask_login import login_user, current_user, logout_user

@app.route('/login', methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	return render_template("verify/login.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	return render_template("verify/register.html")

@app.route('/add_user', methods=['POST'])
def add_user():
	name = request.form["name"]
	number = request.form["number"]
	password = request.form["password"]
	gender = request.form["gender"]
	account_type = request.form['account_type']

	new_user = User(name=name, number=number, password=password, gender=gender)

	hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
	new_user = User(name=name, number=number, password=hash_password, user_type=account_type,\
		gender=gender)
	db.session.add(new_user)
	db.session.commit()

	return jsonify({'success':'ok'})

@app.route('/auth_user', methods=['POST'])
def auth_user():
	number = request.form["number"]
	password = request.form["password"]

	user = User.query.filter_by(number=number).first()
	if user and bcrypt.check_password_hash(user.password, password):
		if user.account_pend == 1:
			return jsonify({'error':'pending_account'})
		else:
			login_user(user, remember=True)
			return jsonify({'error':'no'})
	print("Error function")
	return jsonify({'error':'main_error'})


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))