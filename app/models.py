from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    registrations = db.relationship('EventRegistration', back_populates='event', lazy='dynamic')


class EventRegistration(db.Model):
    registration_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    event = db.relationship('Event', back_populates='registrations')


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    registrations = db.relationship("EventRegistration", backref="user", lazy=True)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Flask-Login integration
    @property
    def is_active(self):
        # Assuming all users are active
        return True

    @property
    def is_authenticated(self):
        # Assuming all logged-in users are authenticated
        return True

    @property
    def is_anonymous(self):
        # False, as anonymous users aren't supported
        return False

    def get_id(self):
        return self.user_id
