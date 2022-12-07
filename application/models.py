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
    cname = db.Column(db.String)
    password = db.Column(db.String)

class Manufacturer(db.Model, UserMixin):
    __tablename__ = "manufacturer"
    mid = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(40),unique = True)
    password = db.Column(db.String)

class Retialer(db.Model, UserMixin):
    __tablename__ = "retailer"
    rid = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(40),unique = True)
    password = db.Column(db.String)

class Wholesaler(db.Model, UserMixin):
    __tablename__ = "wholesaler"
    wid = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(40),unique = True)
    password = db.Column(db.String)

class Products(db.Model, UserMixin):
    __tablename__ = "products"
    pid = db.Column(db.Integer,primary_key = True)
    pname = db.Column(db.String(40),nullable = False,unique = True)
    mdate = db.Column(db.String(40))
    price = db.Column(db.Numeric,nullable = False)

class Orders(db.Model, UserMixin):
    __tablename__ = "orders"
    userid = db.Column(db.Integer,nullable = False,primary_key = True)
    type = db.Column(db.String(40),primary_key = True)
    pid = db.Column(db.Integer,unique = True)
    quantity = db.Column(db.Integer)