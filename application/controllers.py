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



@app.route('/', methods=['GET','POST'])
def index():
    return render_template('sitimHome.html')


@app.route('/<string:userid>/<string:username>/home', methods=['GET'])
@login_required
def home(userid,username):
    if('m' in userid):
        return render_template('profile.html',userid = userid,username = username)
    elif('r' in userid):
        return render_template('retailerprofile.html',userid = userid,username = username)
    elif('w' in userid):
        return render_template('wholesalerprofile.html',userid = userid,username  = username)


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
                    userid = Manufacturer.query.with_entities(Manufacturer.mid).filter_by(username = username).one()[0]
                    
                    
                    return redirect(url_for('home',username = username,userid = userid, **request.args))
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
                    userid = Retailer.query.with_entities(Retailer.rid).filter_by(username = username).one()[0]
                    return redirect(url_for('home',username = username,userid = userid, **request.args))
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
                    userid = Wholesaler.query.with_entities(Wholesaler.wid).filter_by(username = username).one()[0]
                    return redirect(url_for('home',username = username,userid = userid, **request.args))
                else:
                    flash("Incorrect-password")
                    return redirect(url_for('login'))
            else:
                flash("Wholesaler not found.Please Sign up!!")
                return redirect(url_for('login'))
        
    else:
        return render_template('sitimLogin.html')
    

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
                        flash("Wholesaler already exists!")
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
#this will display all the items that can be added into the cart.
@app.route("/<string:userid>/<string:username>/order-bookings",methods = ['GET','POST'])
def order(username,userid):
    
    if request.method == "GET":
        products = Products.query.all()
        return render_template("order.html",username = username,userid = userid)
    if request.method == "POST":
        cartstore = {}
        products = ['Tablet','SmartPhone1','Earphones','Watches','Laptop1','TV','Charger','PowerBank','SmartPhone2','SmartPhone3','Headphones','Laptop2']
        
        for i in products:
            if(i not in (cartstore.keys())):
                if(request.form[i] != 0):
                
                    cartstore[i] = int(request.form[i])
            
        
        for product in cartstore.keys():
        
            if(cartstore[product] != 0):
                pid = Products.query.with_entities(Products.pid).filter_by(pname = product).one()[0]
            
                price = Products.query.with_entities(Products.price).filter_by(pname = product).one()[0]
                added_to_cart = Orders.query.with_entities(Orders.pid).filter_by(userid = userid,pid = pid).first()
                if(added_to_cart):
                    update_product = Orders.query.filter_by(pid = pid,userid = userid).first()
                    update_product.quantity = cartstore[product]#updating the value in the database
                    # return render_template("sample.html",pid = update_product)
                else:
                    new_order = Orders(
                        userid = userid,
                        pid =   pid,
                        quantity = cartstore[product],
                        price = price
                    )
                    db.session.add(new_order)
                    db.session.commit()
                
        return redirect(url_for('cart',userid = userid,username = username))
        

#Cart page
#the items in the order page has to be displayed here for further process

@app.route("/<string:userid>/<string:username>/cart",methods = ['GET','POST'])
def cart(username,userid):
    if request.method == "GET":
        orders = Request.query.filter_by(senduserid = userid,status = "Accepted").all()
        sum = 0
        for i in orders:
            sum+=(i.price*i.quantity)
        return render_template("samplecart.html",userid = userid,username = username,orders = orders,total = sum)


@app.route('/<string:userid>/<string:username>/<int:pid>/delete',methods = ['GET','POST'])
def delete(userid,username,pid):
    if request.method == "GET":
        item_to_delete = Request.query.filter_by(senduserid=userid,pid = pid).first()
        # return render_template("sample.html",orders = item_to_delete)
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('cart',username = username,userid = userid))

@app.route('/<string:userid>/<string:username>/owned_products',methods = ["GET","POST"])
def owned(username,userid):
    #common for both retialer and the wholesaler
    products = Owned.query.filter_by(userid = userid).all()
    return render_template("myproducts.html",username = username,userid = userid,products = products)

@app.route('/<string:userid>/<string:username>/request-product',methods = ['GET','POST'])
def make_request(username,userid):
    if "r" in userid:
        likeString = "'%" + "w" + "%'"
        owned_products = db.session.query(Owned).filter(Owned.userid.ilike("%"+ "w" +"%")).all()
    # print(owned_products[0])
    elif "w" in userid:
        likeString = "'%" + "m" + "%'"
        owned_products = db.session.query(Owned).filter(Owned.userid.ilike("%"+ "m" +"%")).all()
    
    listing = []
    for owned in owned_products:
        listing.append(owned)
    
    if request.method == "GET":  
        pidlist = []
        displayid = []
        products_to_display = []  
        product_req = Request.query.filter_by(senduserid = userid).all()
        
        if len(product_req) == 0:
            products_to_display = owned_products
        else:
            for i in product_req:
                for j in owned_products:
                    if i.pid == j.pid:
                        pidlist.append(i)
                    else:
                        displayid.append(j)
            products_to_display = displayid
               
        return render_template("placerequest.html",userid = userid, username =username,owned_products = products_to_display)
    elif request.method == "POST":
        # product = owned_products[1].pname
        # got = request.form[product]
        # return render_template("sample.html",got=got,name = product)
        for owned in owned_products:
            try:
                if int(request.form[owned.pname]) != 0:
                    new_request = Request(
                        senduserid = userid,
                        recuserid = owned.userid,
                        pid = owned.pid,
                        pname = owned.pname,
                        quantity = request.form[owned.pname],
                        price = owned.price,
                    )
                    db.session.add(new_request)
                    db.session.commit()
            except:
                continue
        return redirect(url_for('make_request',userid = userid,username = username,**request.args))
#to check what products need to be accepted in pending

@app.route('/<string:userid>/<string:username>/checking-request',methods = ['GET','POST'])
def pending(userid,username):
    pending = Request.query.filter_by(recuserid = userid,status = "Pending").all()
    if request.method == "GET":
        #on the receiver end the pending requests will be posted here
        return render_template("status.html",username = username,userid = userid,pendings = pending)
    if request.method == "POST":
        accepted = request.form['product']
        update_request = Request.query.filter_by(pid = accepted,recuserid = userid).first()
        update_request.status = "Accepted"
        new_order = Orders(
            userid = update_request.senduserid,
            pid = accepted,
            quantity = update_request.quantity,
            price = update_request.price
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('pending',username = username,userid = userid,**request.args))