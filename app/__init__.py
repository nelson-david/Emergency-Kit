import pusher
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)

login_manager.login_view = "login"

pusher_client = pusher.Pusher(
	app_id='1061860',
	key='d301eb00c00912993892',
	secret='7eac33b7b64a5b368277',
	cluster='eu',
	ssl=True
)

from app.routes.verify import *
from app.routes.user import *
from app.routes.asyn import *
from app.routes.message_routes import *

