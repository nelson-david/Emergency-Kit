from app import app, pusher_client, db
from app.models import User, Message, Notifications

from flask import render_template, request, jsonify
from flask_login import current_user

@app.route("/message", methods=["POST", "GET"])
def single_message():
	messages = Message.query.all()
	return render_template("messages/chat2.html", messages=messages)

@app.route('/sending', methods=['POST'])
def sending():
	new_msg = Message(author=current_user, body=request.form['message'])
	pusher_client.trigger('my-channel', 'my-event', {'message': request.form['message']})
	db.session.add(new_msg)
	db.session.commit()
	return jsonify({'success':'true'})

@app.route('/check_typing', methods=['POST'])
def check_typing():
	pusher_client.trigger('typing-channel', 'new-typing', {'typing': request.form['id'],\
		'username':current_user.name})
	print(request.form['id'], current_user.name)
	return jsonify({'result':'success'})

@app.route('/alerts')
def alerts():
	notify = Notifications.query.filter_by(reciever_id=current_user.id).all()
	return render_template('alert/notify.html', notify=notify)