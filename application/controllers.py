from wsgiref.util import request_uri
from flask import Flask, request ,url_for,redirect
from flask import render_template
from flask import current_app as app
#from .models import *
from .database import db
from sqlalchemy.exc import IntegrityError

@app.route("/",methods = ["GET","POST"])
def login():
    if request.method == "GET":
        print("inside get method")
        return render_template("login.html")

    elif request.method == "POST":
        
        return render_template("sample.html")
    else:
        print("Not working")
        return render_template("sample.html")
