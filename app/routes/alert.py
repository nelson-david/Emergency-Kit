from app import app, db
from flask import render_template, request, jsonify

from app.models import User, Notifications
from flask_login import current_user

@app.route('/alerts')
def alerts():
	notify = Notifications.query.filter_by(reciever_id=current_user.id).all()
	return render_template('alert/notify.html', notify=notify)


"""
@app.route('/add_notify', methods=['POST'])
def add_notify():
	user = User.query.filter_by(id=request.form['id']).first_or_404()
	message = request.form['message']
	new_msg = Message(author=current_user, recipient=user, body=message)
	db.session.add(new_msg)
	db.session.commit()
	pusher_client.trigger('chat-channel', 'new-message', {'message': message})
	print(pusher_client)
	return jsonify({'result':'success'})"""