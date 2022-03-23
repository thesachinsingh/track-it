from email import message
import os, sys
from flask import current_app as app, redirect
from flask import request, session, render_template, flash
from application.database import db
from application.models import Users, Trackers, TrackerLogs
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
#list of working routes
wroutes = ['/', '/sign_up', '/logout', '/create_tracker', '/tracker/<int:tracker_id>', '/tracker/<int:tracker_id>/create_log']
tracker_type = ['numerical', 'string', 'MCQ']
@app.route('/sign_up', methods = ['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        if "username" in session:
            return redirect('/')
        else:
            return render_template('sign_up.html')
    elif request.method == 'POST':
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        user = Users.query.filter_by(username = username).first()
        if user:
            return render_template("404.html", alert = "Choose another username, This username already exists")
        user = Users(username = username, password = password)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        session['user_id'] =  user.user_id
        return redirect('/')



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
        return render_template("user_home.html", user=user, user_trackers=user_trackers, wroutes = wroutes)
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
        return redirect('/')
    if "username" in session:
        user = Users.query.filter_by(username = session['username']).first()
        return render_template("create_tracker.html", user = user)
    return "You are not Logged In, Log In to continue"

@app.route('/tracker/<int:tracker_id>')
def load_tracker(tracker_id):
    if "username" in session:
        # if os.path.exists(f"graph_{tracker_id}.png"):
        #     print("file found")
        #     os.remove(f"graph_{tracker_id}.png")
        user = Users.query.filter_by(username=session['username']).first()
        tracker = Trackers.query.get(tracker_id)
        logs = TrackerLogs.query.filter_by(tracker_id = tracker_id, user_id = user.user_id)
        print(f"logs : {logs}")
        if tracker:
            logs_data = TrackerLogs.query.filter_by(tracker_id = tracker_id).order_by(TrackerLogs.when.desc())
            time_data = []
            val_data = []
            for x in logs_data:
                time_data.append(x.when)
                # print(f'type of time_data = {type(x.when)}')
                val_data.append(x.value)
                # print(f'type of val_data = {type(int(x.value))}')
            #generating graph
            matplotlib.use('Agg')
            ypoints = val_data
            xpoints = time_data
            plt.plot(xpoints, ypoints, marker = 'o')
            # print(time_data)
            # print(val_data)
            plt.xlabel("Time")
            plt.ylabel("Values")
            # plt.show()
            #Two  lines to make our compiler able to draw:
            plt.savefig(f'static/graph_{tracker_id}.png')
            plt.clf()
            graph_file = f'/static/graph_{tracker_id}.png'
            
            return render_template('tracker_page.html', user = user, tracker = tracker, logs = logs, graph_file = graph_file)
        return render_template("404.html")
    return render_template("404.html", alert = "You're Not Logged In")

@app.route('/tracker/<int:tracker_id>/create_log', methods = ['POST', 'GET'])
def create_log(tracker_id):
    if "username" in session:
        if request.method == 'POST':
            when = request.form.get("when", None)
            when = datetime.strptime(when, '%Y-%m-%dT%H:%M')
            val = request.form.get("val", None)
            notes = request.form.get("notes", "")
            log_data = TrackerLogs(user_id = session['user_id'], tracker_id = tracker_id, when = when, value = val, notes = notes)
            db.session.add(log_data)
            #to update last_tracked in trackers table
            latest_update = TrackerLogs.query.filter_by(tracker_id = tracker_id).order_by(TrackerLogs.when.desc()).first()
            print(type(latest_update.when))
            tracker_update = Trackers.query.get(tracker_id)
            tracker_update.last_tracked = latest_update.when if latest_update.when > when else when
            db.session.commit()
 
            print("Posted data successfully") 
            return redirect(f'/tracker/{tracker_id}') 
        tracker = Trackers.query.filter_by(tracker_id = tracker_id, user_id = session["user_id"]).first()
        t_type = tracker.tracker_type
        if t_type == 'numerical':
            t = "number"
        elif t_type == 'string':
            t = "text"  
        return render_template('create_log.html', tracker = tracker, user=session, t = t)
    else:
        return render_template("404.html")


@app.route('/tracker/<int:tracker_id>/delete')
def del_tracker(tracker_id):
    if "username" in session:
        t = Trackers.query.filter_by(user_id = session['user_id'], tracker_id = tracker_id).first()
        if t:
            TrackerLogs.query.filter_by(tracker_id = tracker_id).delete()
            Trackers.query.filter_by(user_id = session['user_id'], tracker_id = tracker_id).delete()
            # db.session.delete(t)
            db.session.commit()
            return redirect('/')

        # db.session.delete(t)
        
        return render_template('404.html', alert = 'The tracker you want to delete does not exist')

@app.route('/tracker/<int:tracker_id>/<int:log_id>/delete')
def del_log(tracker_id, log_id):
    if "username" in session:
        t = TrackerLogs.query.filter_by(user_id = session['user_id'], tracker_id = tracker_id, log_id = log_id).first()
        if t:
            TrackerLogs.query.filter_by(user_id = session['user_id'], tracker_id = tracker_id, log_id = log_id).delete()
            # db.session.delete(t)
            db.session.commit()
            return redirect(f'/tracker/{ tracker_id }')

        # db.session.delete(t)
        
        return render_template('404.html', alert = 'The log you want to delete does not exist')

@app.route('/logout')
def logout():
    session.pop("username")
    session.pop("user_id")
    return redirect('/')