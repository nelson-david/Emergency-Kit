from app import app
from flask import redirect, url_for, request, jsonify
from flask_login import current_user
from app.models import Incidence, Safe

@app.route("/mark_safe")
def mark_safe():
	incidence = Incidence.query.filter_by(id=request.form['id']).first()
	current_user.like(incidence)
	db.session.commit()

	return jsonify({'success':'true'})

@app.route("/mark_unsafe")
def mark_unsafe():
	incidence = Incidence.query.filter_by(id=request.form['id']).first()
	current_user.unlike(incidence)
	db.session.commit()

	return jsonify({'success':'true'})