from flask import current_app as app
from flask import request, session, render_template, flash
from application.database import db
from application.models import Users, Trackers, TrackerLogs
from datetime import datetime

#list of working routes
wroutes = ['/', '/create_tracker', '/tracker/<int:tracker_id>', '/tracker/<int:tracker_id>/create_log']

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
            user_trackers = Trackers.query.filter_by(user_id = user.user_id)
            #last_modified = TrackerLogs.query.order_by(TrackerLogs.when).last()
            return render_template("user_home.html", user=user, user_trackers=user_trackers, wroutes = wroutes)
        return "Incorrect Credentials", 404
    if "username" in session:
        user = Users.query.filter_by(username = session["username"]).first()
        user_trackers = Trackers.query.filter_by(user_id = user.user_id)
        return render_template("user_home.html", user=user, user_trackers=user_trackers)
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

@app.route('/tracker/<int:tracker_id>')
def load_tracker(tracker_id):
    if "username" in session:
        user = Users.query.filter_by(username=session['username']).first()
        tracker = Trackers.query.get(tracker_id)
        logs = TrackerLogs.query.filter_by(tracker_id = tracker_id, user_id = user.user_id)
        return render_template('tracker_page.html', user = user, tracker = tracker, logs = logs)

@app.route('/tracker/<int:tracker_id>/create_log', methods = ['POST', 'GET'])
def create_log(tracker_id):
    if "username" in session:
        if request.method == 'POST':
            when = request.form.get("when", None)
            when = datetime.strptime(when, '%Y-%m-%dT%H:%M')
            val = request.form.get("val", None)
            notes = request.form.get("notes", "")
            log_data = TrackerLogs(user_id = session['user_id'], tracker_id = tracker_id, when = when, value = int(val), notes = notes)
            db.session.add(log_data)
            tracker_update = Trackers.query.get(tracker_id)
            tracker_update.last_tracked = when
            db.session.commit()
            print("Posted data successfully") 
            return "Done" 
        tracker = Trackers.query.filter_by(tracker_id = tracker_id, user_id = session["user_id"]).first()  
        return render_template('create_log.html', tracker = tracker, user=session)
    else:
        return "You're Not Logged In"
        