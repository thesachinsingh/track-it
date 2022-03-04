from .database import db

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

class Trackers(db.Model):
    __tablename__ = 'trackers'
    tracker_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)
    tracker_name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    tracker_type = db.Column(db.String, nullable = False)
    values = db.Column(db.String)
    user = db.relationship("Users", backref = "tracker", secondary = "tracker_logs")


class TrackerLogs(db.Model):
    __tablename__ = 'tracker_logs'
    user_id = db.Column(db.Integer,   db.ForeignKey("users.user_id"), nullable=False)
    tracker_id = db.Column(db.Integer,  db.ForeignKey("trackers.tracker_id"), nullable=False) 
    log_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    when = db.Column(db.DateTime)
    value = db.Column(db.String)

