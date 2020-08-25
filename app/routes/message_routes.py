from app import app, pusher_client, db
from app.models import User, Message

from flask import render_template, request, jsonify
from flask_login import current_user

@app.route("/message", methods=["POST", "GET"])
def single_message():
	return render_template("messages/chat.html")

@app.route('/sending', methods=['POST'])
def sending():
	user = User.query.filter_by(id=request.form['id']).first_or_404()
	message = request.form['message']
	new_msg = Message(author=current_user, recipient=user, body=message)
	db.session.add(new_msg)
	db.session.commit()
	pusher_client.trigger('chat-channel', 'new-message', {'message': message})
	print(pusher_client)
	return jsonify({'result':'success'})