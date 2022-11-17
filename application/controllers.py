from wsgiref.util import request_uri
from flask import Flask, request ,url_for,redirect
from flask import render_template
from flask import current_app as app
#from .models import *
from .database import db
from sqlalchemy.exc import IntegrityError

@app.route("/login",methods = ["GET","POST"])
def login():
    if method == "GET":
        return render_template("home.html")