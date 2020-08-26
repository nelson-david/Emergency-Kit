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
	message = request.form['message']
	new_msg = Message(author=current_user, body=message)
	db.session.add(new_msg)
	db.session.commit()
	try:
		pusher_client.trigger('chat-channel', 'new-message', {'message': message})
		print(pusher_client)
		return jsonify({'success':'true'})
	except Exception as exc:
		print(exc)
		return jsonify({'success':'false'})

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