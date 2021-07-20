from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .dash_part.fullboards import create_dash_app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # This line creates our database with the name blog.db
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page" # To redirect our user if he isn't logged in
login_manager.login_message_category = "info"
create_dash_app(app)

from blog import routes