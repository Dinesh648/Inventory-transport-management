import os
import pyrebase
from flask import Flask
import time
time.clock = time.time
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

firebase_cofig = {
  "apiKey": "AIzaSyBtwQOZv1OHJAKWD51OFhu0-FjGZeR7iKA",
  "authDomain": "sitim-facfa.firebaseapp.com",
  "databaseURL": "https://sitim-facfa-default-rtdb.firebaseio.com",
  "projectId": "sitim-facfa",
  "storageBucket": "sitim-facfa.appspot.com",
  "messagingSenderId": "22985188766",
  "appId": "1:22985188766:web:3936d37f3e54c4b09b628f",
  "measurementId": "G-Y683ZNF7KZ"
}

firebase = pyrebase.initialize_app(firebase_cofig)
dab = firebase.database()

app = None

def create_app():
  app = Flask(__name__, template_folder="templates")
  app.secret_key = 'supersecretdbms'
  if os.getenv('ENV', "development") == "production":
    raise Exception("Currently no production config is setup.")
  else:
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
  db.init_app(app)
  app.app_context().push()
  return app

app = create_app()

# Import all the controllers so they are loaded
from application.controllers import *

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=5000)