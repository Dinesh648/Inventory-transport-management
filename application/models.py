from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .controllers import LoginManager
from flask import current_app as app


login_manager = LoginManager(app)

login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    try:
        return Users.query.get(user_id)
    except:
        return None

class Users(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String)