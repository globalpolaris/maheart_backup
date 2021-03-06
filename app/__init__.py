from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_fontawesome import FontAwesome

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
Migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
fa = FontAwesome(app)

from app import routes, models, error_handler

def getApp():
    return app