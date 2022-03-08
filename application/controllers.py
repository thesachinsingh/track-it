from flask import current_app as app
from flask import request, session, render_template
from application.database import db
from application.models import Users, Trackers, TrackerLogs

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
            return render_template("user_home.html", user=user)
        return "Incorrect Credentials", 404
    if "username" in session:
        user = Users.query.filter_by(username = session["username"]).first()
        return render_template("user_home.html", user=user)
    return render_template("login.html")

@app.route('/create_tracker', methods = ['GET', 'POST'])
def create_tracker():
    if request.method == 'POST':
        tracker_name = request.form.get("tracker_name")
        description = request.form.get("tracker_description")
        tracker_type = request.form.get("type")
        settings = request.form.get("settings", None)
        user_id = session["user_id"]
        tracker = Trackers(user_id = user_id, tracker_name = tracker_name, description = description, tracker_type=tracker_type, values = settings)
        db.session.add(tracker)
        db.session.commit()
        return "Values Recieved Successfully"
    if "username" in session:
        user = Users.query.filter_by(username = session['username']).first()
        return render_template("create_tracker.html", user = user)
    return "You are not Logged In, Log In to continue"

@app.route('/log_values')
def log_values():
    if ("username" in session) and ("tracker") :
        pass