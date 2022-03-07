from flask import Flask, request, render_template, redirect, session
# from flask_restful import Resource, Api, reqparse
from requests import get, post 
from application.models import Users, Trackers, TrackerLogs
from application.database import db
import os

app = Flask(__name__)
app.secret_key = "super secret key"    
db.init_app(app)
app.app_context().push()

basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_DB_DIR = os.path.join(basedir, "./db_directory")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        user = Users.query.filter_by(username = username, password = password).first()
        if user:
            session['username'] = username
            session['user_id'] =  user.user_id
            print("User verified successfully")
            return render_template("user_home.html")
        return "Incorrect Credentials", 404
    if "username" in session:
        return render_template("user_home.html")
    return render_template("login.html")

@app.route('/create_tracker', methods = ['GET', 'POST'])
def create_tracker():
    if request.method == 'POST':
        pass
    return render_template("create_tracker.html")


if __name__ == '__main__':
    app.run(debug=True)


        


# #
# import os
# from flask import Flask
# from application import config
# from application.config import LocalDevelopmentConfig
# from application.database import db
# import logging
# logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# app = None

# def create_app():
#     app = Flask(__name__, template_folder="templates")
#     if os.getenv('ENV', "development") == "production":
#       app.logger.info("Currently no production config is setup.")
#       raise Exception("Currently no production config is setup.")
#     else:
#       app.logger.info("Staring Local Development.")
#       print("Staring Local Development")
#       app.config.from_object(LocalDevelopmentConfig)
#     db.init_app(app)
#     app.app_context().push()
#     app.logger.info("App setup complete")
#     return app

# app = create_app()

# # Import all the controllers so they are loaded
# from application.controllers import *

# if __name__ == '__main__':
#   # Run the Flask app
#   app.run(host='0.0.0.0',port=8080)

