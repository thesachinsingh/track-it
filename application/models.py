from .database import db

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable = False)
    password = db.Column(db.String, nullable = False)
    trackers = db.relationship("Trackers", backref = "user", cascade="all, delete", passive_deletes=True)
    # email = db.Column(db.String, unique=True)
    #trackers with Trackers
    def __repr__(self):
        return '<User %r>' % self.username

class Trackers(db.Model):
    __tablename__ = 'trackers'
    tracker_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable = False)
    tracker_name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    tracker_type = db.Column(db.String, nullable = False)
    values = db.Column(db.String)
    # user = db.relationship("Users", backref = "trackers")
    logs = db.relationship("TrackerLogs", backref = "tracker", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return '<Tracker %r>' % f'{self.user_id}_{self.tracker_name}'


class TrackerLogs(db.Model):
    __tablename__ = 'tracker_logs'
    user_id = db.Column(db.Integer,   db.ForeignKey("users.user_id"), nullable=False)
    tracker_id = db.Column(db.Integer,  db.ForeignKey("trackers.tracker_id", ondelete="CASCADE"), nullable=False) 
    log_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    when = db.Column(db.DateTime, nullable = False)
    value = db.Column(db.String, nullable=False)
    notes = db.Column(db.String)
    #tracker with Trackers

    def __repr__(self):
        return '<Logs %r>' % self.tracker.tracker_name
