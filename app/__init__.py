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
	app_id='1059936',
	key='2281811cac7fdcfac988',
	secret='ede1e7c4e52ea80c4adf',
	cluster='us2',
	ssl=True
)

from app.routes.verify import *
from app.routes.user import *
from app.routes.asyn import *
from app.routes.message_routes import *

