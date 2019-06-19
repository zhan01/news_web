from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = 'x\xc7\xbcf!\x12\xdd\x1ce\xcb\x8e(e\xbb\xf7t\xf5q\
                            xbb|\xd7\xa2\xd0\xbb\x99\xb0\xd9\xe3t\x99\x10\x9a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
ma = Marshmallow(app)

from alchemy_web import views
