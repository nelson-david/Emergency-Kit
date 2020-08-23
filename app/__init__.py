from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

login_manager.login_view = "login"

from app.routes.verify import *
from app.routes.user import *
from app.routes.asyn import *
from app.routes.message_routes import *

