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
        if "m" in user_id:
            return Manufacturer.query.get(user_id)
        elif "r" in user_id:
            return Retailer.query.get(user_id)
        elif "w" in user_id:
            return Wholesaler.query.get(user_id)
        # return Users.query.get(user_id)
    except:
        return None


class Users(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    cname = db.Column(db.String(40),nullable = False)
    password = db.Column(db.String)

class Manufacturer(db.Model, UserMixin):
    __tablename__ = "manufacturer"
    mid = db.Column(db.String(40),primary_key = True)
    email = db.Column(db.String(50), unique=True)
    cname = db.Column(db.String(40),nullable = False)
    username = db.Column(db.String(40),unique = True)
    password = db.Column(db.String)
    def get_id(self):
        return (self.mid)

class Retailer(db.Model, UserMixin):
    __tablename__ = "retailer"
    rid = db.Column(db.String(40),primary_key = True)
    cname = db.Column(db.String(40),nullable = False)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(40),unique = True)
    password = db.Column(db.String)

class Wholesaler(db.Model, UserMixin):
    __tablename__ = "wholesaler"
    wid = db.Column(db.String(40),primary_key = True)
    
    username = db.Column(db.String(40))
    password = db.Column(db.String)

class Products(db.Model, UserMixin):
    __tablename__ = "products"
    pid = db.Column(db.Integer,primary_key = True)
    pname = db.Column(db.String(40),nullable = False,unique = True)
    price = db.Column(db.Integer,nullable = False)
    manufacturer = db.Column(db.String(100),nullable = False)
    available = db.Column(db.Integer)

class Orders(db.Model, UserMixin):
    __tablename__ = "orders"
    userid = db.Column(db.String(40))
    pid = db.Column(db.Integer, db.ForeignKey('products.pid'),primary_key = True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer,nullable = False)