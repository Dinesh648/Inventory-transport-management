from flask import Flask, request,Blueprint, redirect,url_for    
from flask_login import LoginManager, login_user, login_required, logout_user

from flask import render_template
from flask import current_app as app
from .database import db
from .models import *
from .models import login_manager
from werkzeug.security import check_password_hash
from application.models import Users
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

#users


home = Blueprint('home', __name__, template_folder='../templates')
#login_manager = LoginManager(app)
login_manager.init_app(home)
login_manager.login_view = 'users.login'

@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html')


#index
'''index = Blueprint('index', __name__, template_folder='../templates')
@app.route('/', methods=['GET','POST'])
def index():
    return redirect('login')'''

#login
login = Blueprint('login', __name__, template_folder='../templates')
login_manager.init_app(login)
login_manager.login_view = 'login'
@app.route('/', methods=['GET', 'POST'])

def login():
    if request.method == "GET":
        print("inside get method")
        return render_template("login.html")
    elif request.method == "POST":
        
        
        username = request.form['username']
        password = request.form['password']
        
        user = Users.query.filter_by(username=username).first()
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect( url_for('home') )
            else:
                return redirect(url_for('login') + '?error=incorrect-password')
        else:
            print("user authentication failed")
            return redirect(url_for('login') + '?error=user-not-found')
    
    



        

register = Blueprint('register', __name__, template_folder='../templates')
login_manager.init_app(register)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if username and email and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(
                    password, method='sha256')
                try:
                    new_user = Users(
                        username=username,
                        email=email,
                        password=hashed_password,
                    )

                    db.session.add(new_user)
                    db.session.commit()
                except IntegrityError:
                    return redirect(url_for('register') + '?error=user-or-email-exists')

                return redirect(url_for('login') + '?success=account-created')
        else:
            return redirect(url_for('register') + '?error=missing-fields')
    else:
        return render_template('register.html')