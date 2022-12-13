from flask import Flask, request,Blueprint, redirect,url_for,flash,json,jsonify

from flask_login import LoginManager, login_user, login_required, logout_user

from flask import render_template
from flask import current_app as app
from .database import db
from .models import *
from .models import login_manager
from werkzeug.security import check_password_hash
from application.models import Users,Manufacturer,Retailer,Wholesaler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

#requierments

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('sitimHome.html')
# home = Blueprint('home', __name__, template_folder='../templates')
# #login_manager = LoginManager(app)
# login_manager.init_app(home)
# login_manager.login_view = 'users.login'

@app.route('/<string:username>/home', methods=['GET'])
@login_required
def home(username):
    return render_template('profile.html',username = username)


#index


#login
# login = Blueprint('login', __name__, template_folder='../templates')
# login_manager.init_app(login)
# login_manager.login_view = 'login'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        organization = request.form['organization']

        if organization == 'Manufacturer':
            manufacturer = Manufacturer.query.filter_by(username = username).first()
            if manufacturer:
                if check_password_hash(manufacturer.password, password):
                    login_user(manufacturer)
                    return redirect(url_for('home',username = username, **request.args))
                else:
                    flash("Incorrect-password")
                    return redirect(url_for('login'))
            else:
                flash("Manufacturer not found.Please Sign up!!")
                return redirect(url_for('login'))
        
        elif organization == 'Retailer':
            retailer = Retailer.query.filter_by(username = username).first()
            if retailer:
                if check_password_hash(retailer.password, password):
                    login_user(retailer)
                    return redirect(url_for('home',username = username, **request.args))
                else:
                    flash("Incorrect-password")
                    return redirect(url_for('login'))
            else:
                flash("Retailer not found.Please Sign up!!")
                return redirect(url_for('login'))

        elif organization == 'Wholesaler':
            wholesaler = Wholesaler.query.filter_by(username = username).first()
            if Wholesaler:
                if check_password_hash(wholesaler.password, password):
                    login_user(wholesaler)
                    return redirect(url_for('home',username = username, **request.args))
                else:
                    flash("Incorrect-password")
                    return redirect(url_for('login'))
            else:
                flash("Wholesaler not found.Please Sign up!!")
                return redirect(url_for('login'))
        
        
        
        # user = Users.query.filter_by(username=username).first()

        # if user:
        #     if check_password_hash(user.password, password):
        #         login_user(user)
        #         return redirect(url_for('home',username = username, **request.args))
        #     else:
        #         flash("Incorrect-password")
        #         return redirect(url_for('login') + '?error=incorrect-password')
        # else:
        #     flash("User not found.Please Sign up!!")
        #     return redirect(url_for('login') + '?error=user-not-found')
    else:
        return render_template('sitimLogin.html')
    
    



        

# register = Blueprint('register', __name__, template_folder='../templates')
# login_manager.init_app(register)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        cname = request.form['cname']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        organization = request.form['organization']

        if username and email and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(
                    password, method='sha256')

                if organization == "Manufacturer":
                    number_of_users = Manufacturer.query.count()
                    mid = "m" + str(number_of_users)
                    try:
                        new_manufacturer = Manufacturer(
                            mid = mid,
                            username = username,
                            email = email,
                            cname = cname,
                            password = hashed_password,
                        )
                        db.session.add(new_manufacturer)
                        db.session.commit()
                    except IntegrityError:
                        flash("Manufacturer already exists!")
                        return redirect(url_for('register'))
                elif organization == "Wholesaler":
                    number_of_users = Wholesaler.query.count()
                    wid = "w" + str(number_of_users)
                    try:
                        new_wholesaler = Wholesaler(
                            wid = wid,
                            username = username,
                            email = email,
                            cname = cname,
                            password = hashed_password,
                        )
                        db.session.add(new_wholesaler)
                        db.session.commit()
                    except IntegrityError:
                        flash("Wholesaler already exits!")
                        return redirect(url_for('register'))
                elif organization == "Retailer":
                    number_of_users = Retailer.query.count()
                    rid = "r" + str(number_of_users)
                    try:
                        new_retailer = Retailer(
                            rid = rid,
                            username = username,
                            email = email,
                            cname = cname,
                            password = hashed_password,
                        )
                        db.session.add(new_retailer)
                        db.session.commit()
                    except IntegrityError:
                        flash("Retailer already exists!")
                        return redirect(url_for('register'))
                # try:
                #     new_user = Users(
                #         username=username,
                #         email=email,
                #         cname=cname,
                #         password=hashed_password,
                #     )

                #     db.session.add(new_user)
                #     db.session.commit()
                    
                # except IntegrityError:
                #     return redirect(url_for('register') + '?error=user-or-email-exists')

                return redirect(url_for('login') + '?success=account-created')
            else:
                flash("Both the passwords should match!!")
                return redirect(url_for('register'))
        else:
            flash("Please fill/select in all the fields")
            return redirect(url_for('register') + '?error=missing-fields')
    else:
        return render_template('sitimSign.html')

#Order page
@app.route("/<string:username>/order-bookings",methods = ['GET','POST'])
def order(username):
    if request.method == "GET":
        return render_template("order.html",username = username)
    if request.method == "POST":
        cartstore = {}
        products = ['Tablet','Smartphone','Earphones','Watches','Laptop','TV','Charger','Powerbank','Smartphone2','Smartphone3','Headphones','Laptop2']
        # Tablet = request.form['Tablet']
        # Smartphone1 = request.form['Smartphone1']
        # Earphones = request.form['Earphones']
        # Watches = request.form['Watches']
        # Laptop1 = request.form['Laptop1']
        # TV = request.form['TV']
        # Charger = request.form['Charger']
        # Powerbank = request.form['Powerbank']
        # Smartphone2 = request.form['Smartphone2']
        # Smartphone3 = request.form['Smartphone3']
        # Headphones = request.form['Headphones']
        # Laptop2 = request.form['Laptop2']

        for product in products:
            if product not in cartstore.keys():
                cartstore[product] = 0
                cartstore[product] = request.form[product]
            else:
                cartstore[product] = request.form[product]
        
        for i in cartstore.keys():
            print(i + ":" + cartstore[i])
        cartstorejson = (json.dumps(cartstore))
        # l = [username,cartstorejson]
        return redirect(url_for('cart',username = username,cartstore = cartstorejson, **request.args))
        

#Cart page

@app.route("/<string:username>/cart/<string:cartstore>",methods = ['GET','POST'])
def cart(username,cartstore):
    if request.method == "GET":
        # username = arguments[0]
        
        products_to_buy = json.loads(cartstore)
        # typeinfo = type(products_to_buy)
        total = 0
        for product in products_to_buy.keys():
            if(products_to_buy[product] != 0):
                total += products_to_buy[product]
        return render_template("cart.html",total = total)

    