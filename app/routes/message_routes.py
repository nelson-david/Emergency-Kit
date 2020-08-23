from app import socketio, app
from flask_socketio import send
from app.models import User

from flask import render_template

@socketio.on("message")
def handleMessage(msg):
	print("Message:", msg)
	send(msg, broadcast=True)

@app.route("/message/<id>", methods=["POST", "GET"])
def single_message(id):
	user = User.query.get_or_404(id)
	return render_template("messages/chat.html", user=user)