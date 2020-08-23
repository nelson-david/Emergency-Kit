from app import app, pusher_client
from app.models import User

from flask import render_template, request, jsonify

@app.route("/message/<id>", methods=["POST", "GET"])
def single_message(id):
	user = User.query.get_or_404(id)
	return render_template("messages/chat.html", user=user)

@app.route('/sending', methods=['POST'])
def sending():
	message = request.form['message']
	pusher_client.trigger('chat-channel', 'new-message', {'message': message})
	print(pusher_client)
	return jsonify({'result':'success'})